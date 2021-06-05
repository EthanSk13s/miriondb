from flask import Blueprint, render_template

from mirion.models import Card, Event

main_page = Blueprint("main", __name__)


@main_page.app_errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@main_page.route("/")
def index():
    recent_datetime = Card.query.order_by(-Card.db_id).first().release
    recent_additions = Card.query.filter(recent_datetime == Card.release,
                                         Card.event_id == None).all()

    current_event = Event.query.order_by(-Event.db_id).first()
    if current_event.event_type in (3, 4, 9):
        event_cards = Card.query.filter(
            Card.event_id == current_event.id
        ).all()
    else:
        event_cards = None

    return render_template('main.html', recent_additions=recent_additions,
                           event=current_event, event_cards=event_cards)
