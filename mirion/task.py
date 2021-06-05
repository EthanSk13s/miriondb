import logging

from flask_apscheduler import APScheduler
from apscheduler.schedulers.background import BackgroundScheduler

from mirion.utils import fetch
from mirion.database import db
from mirion.models import Card, Event

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

        logging.info(f"{diff} added to Database")
    else:
        logging.info("No changes found")


@scheduler.task('cron', id='check_changes', hour=15, minute=2)
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
            db.session.commit()

            scheduler.init_app(app)
            app.first_run = 1
            scheduler.start()
    else:
        pass
