from mirion.database import db


class Card(db.Model):
    db_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id = db.Column(db.Integer)
    idol_id = db.Column(db.Integer, index=True)
    card_name = db.Column(db.Text, index=True)
    rarity = db.Column(db.Integer, index=True)

    idol_type = db.Column(db.Integer, index=True)
    ex_type = db.Column(db.Integer, index=True)
    release = db.Column(db.DateTime, index=True, default=None)
    event_id = db.Column(db.Integer, index=True, default=None)

    skill = db.Column(db.Text, default=None)
    skill_id = db.Column(db.Integer, default=None)
    center_skill = db.Column(db.Text, default=None)

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

    card_url = db.Column(db.Text)
    bg_url = db.Column(db.Text, default=None)

    awake_card_url = db.Column(db.Text)
    awake_bg_url = db.Column(db.Text, default=None)

    costume = db.Column(db.Text, default=None)
    b_costume = db.Column(db.Text, default=None)
    r_costume = db.Column(db.Text, default=None)

    icon = db.Column(db.Text)

    def __repr__(self):
        return '<Card {}>'.format(self.card_name)


class Event(db.Model):
    db_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id = db.Column(db.Integer, index=True)
    event_type = db.Column(db.Integer, index=True)
    name = db.Column(db.Text)
    begin = db.Column(db.DateTime)
    end = db.Column(db.DateTime)

    def __repr__(self):
        return '<Event {}>'.format(self.name)
