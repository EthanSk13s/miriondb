import dateutil.parser

from mirion.models import Card, Event


def get_card(card, db):
    entry = Card(id=card.id,
                 idol_id=card.idol_id,
                 card_name=card.name,
                 rarity=card.rarity,
                 idol_type=card.type,
                 vocal=card.min_vocal,
                 visual=card.min_visual,
                 dance=card.min_dance,
                 max_vocal=card.max_vocal,
                 max_dance=card.max_dance,
                 max_visual=card.max_visual,
                 life=card.life,
                 awake_vocal=card.min_awake_vocal,
                 awake_visual=card.min_awake_visual,
                 awake_dance=card.min_awake_dance,
                 max_awake_vocal=card.max_awake_vocal,
                 max_awake_dance=card.max_awake_dance,
                 max_awake_visual=card.max_awake_visual,
                 card_url=card.get_image("card"),
                 awake_card_url=card.get_image("card", is_awaken=True),
                 icon=card.get_image("icon"))

    if card.add_date is not None:
        entry.release = dateutil.parser.parse(card.add_date)

    if card.event_id is not None:
        entry.event_id = card.event_id

    if card.skill is not None:
        entry.skill = card.skill.desc
        entry.skill_id = card.skill.effect
        entry.center_skill = card.center_skill.desc

    if card.costume is not None:
        entry.costume = card.costume.get_image()

    if card.bonus_costume is not None:
        entry.b_costume = card.bonus_costume.get_image()

    if card.rank_costume is not None:
        entry.r_costume = card.rank_costume.get_image()

    if card.rarity == 4:
        if card.ex_type not in (5, 7, 10):
            entry.bg_url = card.get_image("card_bg", bg=True)
            entry.awake_bg_url = card.get_image("card_bg", bg=True,
                                                is_awaken=True)

    db.session.add(entry)


def get_events(event, db):
    entry = Event(id=event.id,
                  event_type=event.type,
                  name=event.name,
                  begin=dateutil.parser.parse(event.schedule.begin),
                  end=dateutil.parser.parse(event.schedule.end))

    db.session.add(entry)
