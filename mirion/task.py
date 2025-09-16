from __future__ import annotations

import logging
import json

from flask_apscheduler import APScheduler
from apscheduler.schedulers.background import BackgroundScheduler
from sqlalchemy import select, update

from mirion.utils import fetch
from mirion.database import db
from mirion.models import Card, Event, Costume
from mirion.connection import ConnectionSocket

from pryncess.models.cards import Card as PryncessCard
from pryncess.models.events import Event as PryncessEvent

scheduler = APScheduler(scheduler=BackgroundScheduler(
    {'apscheduler.timezone': 'Asia/Tokyo'}))

def add_changes_cards(changes: list[PryncessCard]):
    card_ids = db.session.scalars(
        select(Card.id)
    ).all()
    changes_ids: list[tuple[int, int]] = [(i, card.id) for i, card in enumerate(changes)]

    # Simple list comprehension to check if we have any changes. If not in db, then it's new.
    differences: list[int] = [i for i, id in changes_ids if id not in card_ids]

    if len(differences) > 0:
        for diff in differences:
            fetch.get_card(changes[diff], db)
        logging.info(f"{len(differences)} cards have been added.")
    else:
        logging.info("No Changes found")

    db.session.commit()

def add_changes_events(changes: list[PryncessEvent]):
    event_ids = db.session.scalars(
        select(Event.id)
    ).all()

    changes_ids = [(i, event.id) for i, event in enumerate(changes)]
    differences: list[int] = [i for i, id in changes_ids if id not in event_ids]

    if len(differences) > 0:
        for diff in differences:
            fetch.get_events(changes[diff], db)
        logging.info(f"{len(differences)} events have been added.")
    else:
        logging.info("No Changes found")

    db.session.commit()

def check_for_master_ranks(changes: list[PryncessCard]):
    ssr_cards = [card for card in changes if card.rarity == 4]
    ssr_cards.sort(key=lambda x: x.id)

    cards = db.session.scalars(
        select(Card)
            .filter(Card.rarity == 4)
            .order_by(Card.id)
    ).all()

    for ssr_card, card in zip(ssr_cards, cards):
        if card.max_master_rank != ssr_card.max_master_rank:
            db.session.execute(
                update(Card)
                    .where(Card.id == ssr_card.id)
                    .values(max_master_rank=ssr_card.max_master_rank)
            )

            costume = db.session.scalar(
                select(Costume)
                    .filter(Costume.resc_id == card.resc_id)
            )

            if costume is None:
                logging.info(f"Costume for {card.id} is not present. Resource ID: {card.resc_id}.")
                continue

            list_of_costumes: list[str] = []
            if costume.costume_resc_ids is not None:
                list_of_costumes = json.loads(costume.costume_resc_ids.replace('\'', '"'))

            # For whatever reason, this can cause an error when
            # starting up for the first time
            try:
                list_of_costumes.append(ssr_card.rank_costume.resc_id)
            except AttributeError:
                continue

            db.session.execute(
                update(Costume)
                    .where(Costume.resc_id == card.resc_id)
                    .values(costume_resc_ids=(str(list_of_costumes).replace('"', '\'')))
            )

            logging.info(f"{card.card_name}'s master rank has been updated")

    app = scheduler.app
    if app.first_run == 1:
        s = ConnectionSocket(app.assets_addr)
        s.send_message("1", app)

    db.session.commit()

@scheduler.task('cron', id='check_changes', hour=15, minute=2)
@scheduler.task('cron', id='check_changes_midnight', hour=0, minute=2)
def add_to_database():
    app = scheduler.app
    with app.app_context():
        client = app.pryncess
        card_changes = app.pryncess.get_all_cards(tl=True)

        add_changes_events(client.get_all_events())
        add_changes_cards(card_changes)
        check_for_master_ranks(card_changes)

        db.session.commit()


def init_app(app):
    if app.first_run == 0:
        with app.app_context():
            scheduler.init_app(app)
            card_changes = app.pryncess.get_all_cards(tl=True)

            logging.info("Startup checking for new events...")
            add_changes_events(app.pryncess.get_all_events())

            logging.info("Startup checking for new cards...")
            add_changes_cards(card_changes)
            check_for_master_ranks(card_changes)

            app.first_run = 1
            scheduler.start()
