import json
import os
from json.decoder import JSONDecodeError

from mirion.database import db
from mirion.utils import enums

BASE_URL = os.environ.get("USE_ASSETS") if os.environ.get("USE_ASSETS") else "https://storage.matsurihi.me/mltd"


# Instead of relying on pryncess's TLs
# let's manually TL skills to save space on DB
class Skill(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    effect_id = db.Column(db.Integer)
    evaluation = db.Column(db.Integer)
    evaluation2 = db.Column(db.Integer)
    evaluation3 = db.Column(db.Integer)
    duration = db.Column(db.Integer)
    interval = db.Column(db.Integer)
    probability = db.Column(db.Integer)
    value = db.Column(db.JSON)

    @property
    def tl_desc(self):
        interval = self.interval
        probability = self.probability
        duration = self.duration

        interval_str = enums.INTERVAL_STRING.format(interval=interval,
                                                    probability=probability)
        duration_str = enums.DURATION_STRING.format(duration=duration)

        eff_id = self.effect_id

        if eff_id == 4:
            return f"{interval_str} {enums.EFFECTS.get(eff_id)} {duration_str}"

        eff_vals = {}
        if self.evaluation != 0:
            eff_vals['evaluation'] = enums.EVALUATIONS.get(self.evaluation)

        if len(list(self.value)) != 0:
            eff_vals['value'] = self.value

        if self.evaluation2 != 0:
            eff_vals['evaluation2'] = enums.EVALUATIONS.get(self.evaluation2)
        if self.evaluation3 != 0:
            eff_vals['evaluation3'] = enums.EVALUATIONS.get(self.evaluation3)

        try:
            effect_str = enums.EFFECTS.get(eff_id).format(**eff_vals)
        except AttributeError:
            return "No TL available"

        return f"{interval_str} {effect_str} {duration_str}"

    def __repr__(self):
        return '<Skill {}>'.format(self.id)


class CenterSkill(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    idol_type = db.Column(db.Integer)
    attribute = db.Column(db.Integer)
    value = db.Column(db.Integer)
    song_type = db.Column(db.Integer, default=None)
    value_2 = db.Column(db.Integer)

    @property
    def tl_desc(self):
        idol_type = enums.TYPES.get(self.idol_type)
        attribute = enums.ATTRIBUTES.get(self.attribute)
        value = self.value

        if any([idol_type, attribute]) is None:
            return "No TL available"

        if self.id <= 7000:
            first_cond = enums.CENTER_SKILL_STRING.format(idol_type.capitalize(),
                                                          attribute,
                                                          value)
        else:
            value_2 = self.value_2
            first_cond = enums.CENTER_BOOST_STRING.format(value_2,
                                                          attribute,
                                                          value)

        if self.song_type is not None:
            attr_2 = enums.TYPES.get(self.song_type)
            value_2 = self.value_2
            second_cond = enums.SONG_STRING.format(attr_2, value_2)
            return f"{first_cond}. {second_cond}"
        else:
            return first_cond

    def __repr__(self):
        return '<Center Skill {}>'.format(self.id)


class Costume(db.Model):
    resc_id = db.Column(db.Text, primary_key=True)
    costume_resc_ids = db.Column(db.Text, default=None)

    @property
    def url(self):
        urls = []

        try:
            costumes = json.loads(self.costume_resc_ids.replace('\'', '"'))
        except JSONDecodeError:
            return None
        for resc_id in costumes:
            if BASE_URL == "https://storage.matsurihi.me/mltd":
                urls.append(f"{BASE_URL}/costume_icon_ll/{resc_id}.png")
            else:
                urls.append(f"{BASE_URL}/costumes/{resc_id}.png")

        if not urls:
            return None

        return urls

    def __repr__(self):
        return '<Costumes {}>'.format(self.resc_id)


class Event(db.Model):
    id = db.Column(db.Integer, index=True, primary_key=True)
    event_type = db.Column(db.Integer, index=True)
    name = db.Column(db.Text)
    begin = db.Column(db.DateTime)
    end = db.Column(db.DateTime)

    def __repr__(self):
        return '<Event {}>'.format(self.name)


class Card(db.Model):
    db_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id = db.Column(db.Integer)
    resc_id = db.Column(db.Text, db.ForeignKey(Costume.resc_id))
    idol_id = db.Column(db.Integer, index=True)
    card_name = db.Column(db.Text, index=True)
    rarity = db.Column(db.Integer, index=True)

    idol_type = db.Column(db.Integer, index=True)
    ex_type = db.Column(db.Integer, index=True)
    release = db.Column(db.DateTime, index=True, default=None)
    event_id = db.Column(db.Integer, db.ForeignKey(Event.id), index=True, default=None)
    event = db.relationship('Event', foreign_keys='Card.event_id')

    skill_id = db.Column(db.Integer, db.ForeignKey(Skill.id), default=None)
    center_skill_id = db.Column(db.Integer, db.ForeignKey(CenterSkill.id), default=None)

    skill = db.relationship('Skill', foreign_keys='Card.skill_id', lazy='joined')
    center_skill = db.relationship('CenterSkill', foreign_keys='Card.center_skill_id', lazy='joined')

    vocal = db.Column(db.Integer)
    dance = db.Column(db.Integer)
    visual = db.Column(db.Integer)

    max_vocal = db.Column(db.Integer)
    max_dance = db.Column(db.Integer)
    max_visual = db.Column(db.Integer)
    life = db.Column(db.Integer)

    awake_vocal = db.Column(db.Integer)
    awake_dance = db.Column(db.Integer)
    awake_visual = db.Column(db.Integer)

    max_awake_vocal = db.Column(db.Integer)
    max_awake_dance = db.Column(db.Integer)
    max_awake_visual = db.Column(db.Integer)

    max_master_rank = db.Column(db.Integer)
    vocal_rank_bonus = db.Column(db.Integer)
    dance_rank_bonus = db.Column(db.Integer)
    visual_rank_bonus = db.Column(db.Integer)

    costumes = db.relationship('Costume', foreign_keys='Card.resc_id', lazy='joined')

    @property
    def icon(self):
        if BASE_URL == "https://storage.matsurihi.me/mltd":
            return f"{BASE_URL}/icon_l/{self.resc_id}_0.png"

        return f"{BASE_URL}/icons/{self.resc_id}_0.png"

    @property
    def card_url(self):
        if BASE_URL == "https://storage.matsurihi.me/mltd":
            return f"{BASE_URL}/card/{self.resc_id}_0_a.png"

        return f"{BASE_URL}/card/{self.resc_id}_0.png"

    @property
    def awake_card_url(self):
        if BASE_URL == "https://storage.matsurihi.me/mltd":
            return f"{BASE_URL}/card/{self.resc_id}_1_a.png"

        return f"{BASE_URL}/card/{self.resc_id}_1.png"

    @property
    def bg_url(self):
        if self.rarity == 4 and self.ex_type not in [5, 7, 10, 13]:
            return f"{BASE_URL}/card_bg/{self.resc_id}_0.png"
        else:
            return None

    @property
    def awake_bg_url(self):
        if self.rarity == 4 and self.ex_type not in [5, 7, 10, 13]:
            return f"{BASE_URL}/card_bg/{self.resc_id}_1.png"
        else:
            return None

    def __repr__(self):
        return '<Card {}>'.format(self.card_name)
