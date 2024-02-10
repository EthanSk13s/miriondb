import json
import os

from typing import List

from sqlalchemy.orm import Mapped

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

    @property
    def serialize(self):
        return {
            'name': enums.SKILL_TYPES.get(self.effect_id),
            'description': self.tl_desc
        }

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
        elif self.id >= 20000:
            first_cond = enums.CENTER_AFFECTION_BOOST.format(value)
        else:
            value_2 = self.value_2
            first_cond = enums.CENTER_BOOST_STRING.format(value_2,
                                                          attribute,
                                                          value)

        if self.song_type is not None:
            attr_2 = enums.TYPES.get(self.song_type)
            value_2 = self.value_2
            second_cond = enums.SONG_STRING.format(attr_2)

            if (self.id % 1000) >= 420 and (self.id % 1000) < 500:
                third_cond = enums.CENTER_SWING_STRING.format(idol_type.capitalize(),
                                                        value_2)
                return f"{first_cond}. {second_cond} {third_cond}"
            else:
                third_cond = enums.CENTER_IDOL_BOOST_STRING.format(value_2)
                return f"{first_cond}. {second_cond} {third_cond}"
        else:
            return first_cond

    @property
    def serialize(self):
        return {
            'id': self.id,
            'description': self.tl_desc
        }

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
        except:
            return None
        for resc_id in costumes:
            if BASE_URL == "https://storage.matsurihi.me/mltd":
                urls.append(f"{BASE_URL}/costume_icon_ll/{resc_id}.png")
            else:
                urls.append(f"{BASE_URL}/costumes/{resc_id}.png")

        if not urls:
            return None

        return urls

    @property
    def serialize(self):
        try:
            costumes = json.loads(self.costume_resc_ids.replace('\'', '"'))
        except:
            costumes = None
        return costumes

    def __repr__(self):
        return '<Costumes {}>'.format(self.resc_id)


class Event(db.Model):
    id = db.Column(db.Integer, index=True, primary_key=True)
    event_type = db.Column(db.Integer, index=True)
    name = db.Column(db.Text)
    begin = db.Column(db.DateTime(timezone=True))
    end = db.Column(db.DateTime(timezone=True))

    @property
    def serialize(self):
        return {
            'id': self.id,
            'eventType': self.event_type,
            'name': self.name,
            'begin': self.begin,
            'end': self.end
        }

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
    release = db.Column(db.DateTime(timezone=True), index=True, default=None)
    event_id = db.Column(db.Integer, db.ForeignKey(Event.id), index=True, default=None)
    event: Mapped["Event"] = db.relationship('Event', foreign_keys='Card.event_id', lazy='joined')

    skill_id = db.Column(db.Integer, db.ForeignKey(Skill.id), default=None)
    center_skill_id = db.Column(db.Integer, db.ForeignKey(CenterSkill.id), default=None)

    skill: Mapped["Skill"] = db.relationship('Skill', foreign_keys='Card.skill_id', lazy='joined')
    center_skill: Mapped["CenterSkill"] = db.relationship('CenterSkill', foreign_keys='Card.center_skill_id', lazy='joined')

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

    costumes: Mapped[List["Costume"]] = db.relationship('Costume', foreign_keys='Card.resc_id', lazy='joined')

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
        if self.rarity == 4 and self.ex_type not in [5, 7, 10, 13, 16]:
            return f"{BASE_URL}/card_bg/{self.resc_id}_0.png"
        else:
            return None

    @property
    def awake_bg_url(self):
        if self.rarity == 4 and self.ex_type not in [5, 7, 10, 13, 16]:
            return f"{BASE_URL}/card_bg/{self.resc_id}_1.png"
        else:
            return None

    @property
    def serialize(self):
        return {
            'id': self.id,
            'rescId': self.resc_id,
            'idolId': self.idol_id,
            'cardName': self.card_name,
            'rarity': self.rarity,
            'idolType': self.idol_type,
            'exType': self.ex_type,
            'release': self.release,
            'event': self.event.serialize if self.event is not None else None,
            'skill': self.skill.serialize if self.skill is not None else None,
            'centerSkill': self.center_skill.serialize if self.center_skill is not None else None,
            'stats': {
                'life': self.life,
                'vocal': self.vocal,
                'dance': self.dance,
                'visual': self.visual,
                'maxVocal': self.max_vocal,
                'maxDance': self.max_dance,
                'maxVisual': self.max_visual,
                'awakeVocal': self.awake_vocal,
                'awakeDance': self.awake_dance,
                'awakeVisual': self.awake_visual,
                'maxAwakeVocal': self.max_awake_vocal,
                'maxAwakeDance': self.max_awake_dance,
                'maxAwakeVisual': self.max_awake_visual,
                'maxMasterRank': self.max_master_rank,
                'vocalRankBonus': self.vocal_rank_bonus,
                'danceRankBonus': self.dance_rank_bonus,
                'visualRankBonus': self.visual_rank_bonus
            },
            'costumes': self.costumes.serialize if self.costumes is not None else None
        }

    @property
    def mini_serialize(self):
        return {
            'id': self.id,
            'rescId': self.resc_id,
            'cardName': self.card_name,
            'rarity': self.rarity,
            'idolType': self.idol_type,
            'release': self.release,
            'event': self.event.serialize if self.event is not None else None
        }

    def __repr__(self):
        return '<Card {}>'.format(self.card_name)
