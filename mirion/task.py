import logging
import json

from flask_apscheduler import APScheduler
from apscheduler.schedulers.background import BackgroundScheduler

from mirion.utils import fetch
from mirion.database import db
from mirion.models import Card, Event, Costume

scheduler = APScheduler(scheduler=BackgroundScheduler(
    {'apscheduler.timezone': 'Asia/Tokyo'}))


def add_changes(db_list: list, changes: list, is_event=False):
    diff = len(changes) - len(db_list)
    if diff > 0:
        if is_event is False:
            for item in changes[-diff:]:
                fetch.get_card(item, db)
        else:
            for item in changes[-diff:]:
                fetch.get_events(item, db)

        db.session.commit()

        fifo = open("theater/wake.fifo", "w")  # Let asset server know that there are images to be downloaded
        fifo.write("1")
        fifo.close()

        logging.info(f"{diff} added to Database")
    else:
        logging.info("No changes found")

    # Check for Master rank updates
    if is_event is False:
        if diff > 0:
            ssr_cards = [card for card in changes if card.rarity == 4]
            cards = Card.query.filter(Card.rarity == 4)

            for ssr_card, card in zip(ssr_cards, cards):
                if card.max_master_rank != ssr_card.max_master_rank:
                    if ssr_card.rank_costume is not None:
                        card.max_master_rank = ssr_card.max_master_rank
                        db.session.flush()

                        costume = Costume.query.filter(card.resc_id == Costume.resc_id).first()
                        list_of_costumes = json.loads(costume.costume_resc_ids.replace('\'', '"'))

                        list_of_costumes.append(ssr_card.rank_costume.resc_id)

                        costume.costume_resc_ids = str(list_of_costumes).replace('"', '\'')

                        db.session.flush()
                        logging.info(f"{card.card_name}'s master rank has been updated")

            db.session.commit()


@scheduler.task('cron', id='check_changes', hour=15, minute=2)
@scheduler.task('cron', id='check_changes_midnight', hour=0, minute=2)
def add_to_database():
    app = scheduler.app
    with app.app_context():
        client = app.pryncess
        add_changes(Card.query.all(), client.get_all_cards(tl=True))
        add_changes(Event.query.all(), client.get_all_events(), is_event=True)

        db.session.commit()


def init_app(app):
    if app.first_run == 0:
        with app.app_context():
            logging.info("Startup checking for new cards...")
            add_changes(Card.query.all(), app.pryncess.get_all_cards(tl=True))
            logging.info("Startup checking for new events...")
            add_changes(Event.query.all(), app.pryncess.get_all_events(),
                        is_event=True)

            scheduler.init_app(app)
            app.first_run = 1
            scheduler.start()
    else:
        pass
