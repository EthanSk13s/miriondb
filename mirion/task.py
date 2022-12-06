from __future__ import annotations

import logging
import json
import datetime

import dateutil.parser

from datetime import timezone
from flask_apscheduler import APScheduler
from apscheduler.schedulers.background import BackgroundScheduler

from mirion.utils import fetch
from mirion.database import db
from mirion.models import Card, Event, Costume
from mirion.connection import ConnectionSocket

from pryncess.models.cards import Card as PryncessCard
from pryncess.models.events import Event as PryncessEvent

scheduler = APScheduler(scheduler=BackgroundScheduler(
    {'apscheduler.timezone': 'Asia/Tokyo'}))

def add_changes_cards(changes: list[PryncessCard]):
    changes.reverse()
    num_of_changes = 0
    for item in changes:
        add_date = None
        if item.add_date is not None:
            add_date = datetime.datetime.fromtimestamp(dateutil.parser.isoparse(item.add_date).timestamp(), tz=timezone.utc)         
        card_rows = Card.query.filter(Card.release == add_date).all()

        exists = [card.resc_id for card in card_rows]

        if item.resc_id not in exists:
            fetch.get_card(item, db)
            num_of_changes += 1
        else:
            if card_rows[0].release is not None:
                if card_rows[0].release <= add_date and item.type != 5:
                    break
                

    if num_of_changes > 0:
        logging.info(f"{num_of_changes} cards have been added")
    else:
        logging.info("No Changes found")

    db.session.commit()

def add_changes_events(db_list: list, changes: list[PryncessEvent]):
    # Works great, so fine to leave as is (for now)
    diff = len(changes) - len(db_list)
    num_of_changes = 0
    if diff > 0:
        for item in changes[-diff:]:
            fetch.get_events(item, db)
            num_of_changes += 1

    if num_of_changes > 0:
        logging.info(f"{num_of_changes} events have been added")
    else:
        logging.info("No Changes found")

    db.session.commit()

def check_for_master_ranks(changes: list[PryncessCard]):
    ssr_cards = [card for card in changes if card.rarity == 4]
    ssr_cards.sort(key=lambda x: x.id)

    cards = Card.query.filter(Card.rarity == 4).order_by(Card.id)

    for ssr_card, card in zip(ssr_cards, cards):
        if card.max_master_rank != ssr_card.max_master_rank:
            Card.query.filter(Card.id == ssr_card.id).update({'max_master_rank': ssr_card.max_master_rank})

            costume = Costume.query.filter(card.resc_id == Costume.resc_id).first()
            list_of_costumes = json.loads(costume.costume_resc_ids.replace('\'', '"'))

            # For whatever reason, this can cause an error when
            # starting up for the first time
            try:
                list_of_costumes.append(ssr_card.rank_costume.resc_id)
            except AttributeError:
                continue

            Costume.query.filter(Costume.resc_id == card.resc_id).update({"costume_resc_ids": (str(list_of_costumes).replace('"', '\''))})

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

        add_changes_events(Event.query.all(), client.get_all_events())
        add_changes_cards(card_changes)
        check_for_master_ranks(card_changes)

        db.session.commit()


def init_app(app):
    if app.first_run == 0:
        with app.app_context():
            scheduler.init_app(app)
            card_changes = app.pryncess.get_all_cards(tl=True)

            logging.info("Startup checking for new events...")
            add_changes_events(Event.query.all(), app.pryncess.get_all_events())

            logging.info("Startup checking for new cards...")
            add_changes_cards(card_changes)
            check_for_master_ranks(card_changes)

            app.first_run = 1
            scheduler.start()
    else:
        pass
