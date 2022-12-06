import datetime
import dateutil.parser

from datetime import timezone
from mirion.models import Card, Event, CenterSkill, Skill, Costume


def get_card(card, db):
    # Same situation here as anniv skills, anniv cards share costumes
    entry_costume = Costume(resc_id=card.resc_id)
    if card.costume is not None:

        entry_costume.costume_resc_ids = [card.costume.resc_id]

        if card.bonus_costume is not None:
            entry_costume.costume_resc_ids.append(card.bonus_costume.resc_id)

        if card.rank_costume is not None:
            entry_costume.costume_resc_ids.append(card.rank_costume.resc_id)

        entry_costume.costume_resc_ids = str(entry_costume.costume_resc_ids)

        if db.session.query(Costume).filter(Costume.resc_id == entry_costume.resc_id).first():
            pass

    exists = Costume.query.filter(Costume.resc_id == entry_costume.resc_id).first()
    if exists is None:
        db.session.add(entry_costume)

    entry = Card(id=card.id,
                 resc_id=card.resc_id,
                 idol_id=card.idol_id,
                 card_name=card.name,
                 rarity=card.rarity,
                 idol_type=card.type,
                 ex_type=card.ex_type,
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
                 max_master_rank=card.max_master_rank,
                 vocal_rank_bonus=card.bonus_vocal,
                 dance_rank_bonus=card.bonus_dance,
                 visual_rank_bonus=card.bonus_visual)

    if card.add_date is not None:
        entry.release = datetime.datetime.fromtimestamp(dateutil.parser.isoparse(card.add_date).timestamp(), tz=timezone.utc)

    if card.event_id is not None:
        entry.event_id = card.event_id

    if card.skill is not None:
        entry.skill_id = card.skill.id
        skill_entry = Skill(id=card.skill.id,
                            effect_id=card.skill.effect,
                            evaluation=card.skill.evaluation,
                            evaluation2=card.skill.evaluation2,
                            evaluation3=card.skill.evaluation3,
                            duration=card.skill.duration,
                            interval=card.skill.interval,
                            probability=card.skill.probability,
                            value=card.skill.value)

        entry.center_skill_id = card.center_skill.id
        center_entry = CenterSkill(id=card.center_skill.id,
                                   idol_type=card.center_skill.type,
                                   attribute=card.center_skill.attribute,
                                   value=card.center_skill.value,
                                   song_type=card.center_skill.song_type,
                                   value_2=card.center_skill.value_2)

        # Since anniv cards have two versions of the same card
        # unique constraints fail, so we add the skills only once
        if db.session.query(Skill).filter(Skill.id == skill_entry.id).first():
            pass
        else:
            db.session.add(skill_entry)

        if db.session.query(CenterSkill).filter(CenterSkill.id == center_entry.id).first():
            pass
        else:
            db.session.add(center_entry)

    db.session.add(entry)


def get_events(event, db):
    entry = Event(id=event.id,
                  event_type=event.type,
                  name=event.name,
                  begin=datetime.datetime.fromtimestamp(dateutil.parser.isoparse(event.schedule.begin).timestamp(), tz=timezone.utc),
                  end=datetime.datetime.fromtimestamp(dateutil.parser.isoparse(event.schedule.end).timestamp(), tz=timezone.utc))

    db.session.add(entry)
