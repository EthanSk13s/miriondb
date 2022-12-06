import sqlalchemy

from flask import Blueprint, jsonify, render_template

from mirion.models import Card, Event
from mirion.utils import helpers

main_page = Blueprint("main", __name__)


@main_page.app_errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@main_page.route("/latest")
def latest():
    recent_datetime = Card.query.filter(Card.ex_type != 13,
                                        Card.event_id == None,
                                        Card.idol_type != 5).order_by(Card.id.desc()).first().release
    recent_additions = Card.query.filter(recent_datetime == Card.release,
                                         Card.event_id == None, Card.ex_type != 13).order_by(Card.id.asc()).all()

    current_event: Event = Event.query.order_by(-Event.id).first()
    if current_event.event_type in (3, 4, 5, 9, 11, 13, 16):
        event_cards = Card.query.filter(Card.event_id == current_event.id,
                                        sqlalchemy.or_(Card.rarity == 3, Card.rarity == 2)).all()
    else:
        event_cards = None

    previous_dates = Card.query.with_entities(Card.release).filter(recent_datetime != Card.release,
                                                                   Card.ex_type != 13, Card.event_id == None).\
        order_by(Card.release.desc()).\
        group_by(Card.release)[0:2]

    dates = [card.release for card in previous_dates]

    previous_additions = Card.query.filter(Card.release.in_(dates)).all()

    sorted_additions = helpers.list_grouper(previous_additions,
                                            helpers.check_for_release)
    
    payload = {
        'currentEvent': 
            {
                'event': current_event.serialize,
                'cards': [card.serialize for card in event_cards] if event_cards is not None else event_cards
            },
        'recentCards': [card.serialize for card in recent_additions],
        'previousAdditions': []
    }

    temp_list = []
    for date in sorted_additions:
        temp_list.append([card.serialize for card in date])

    payload['previousAdditions'] = temp_list

    return jsonify({'data': payload})

@main_page.route("/history/<page>")
def history(page):
    # TODO: Probably should add a check if we've reached the end of the pages
    dates = Card.query.with_entities(Card.release).\
        order_by(Card.release.desc()).group_by(Card.release).\
        paginate(int(page), 10, False)

    # In docker, without making a copy of the dates list,
    # and specifying the release column
    # it throws a psycopg2 error (Can't adapt to type 'row')
    new_dates = [date.release for date in dates.items]

    # TODO: Properly separate event cards from regular cards
    paginated_cards = Card.query.filter(Card.release.in_(new_dates)).order_by(Card.release.desc()).all()
    sorted_history = helpers.list_grouper(paginated_cards,
                                          helpers.check_for_release)

    return render_template('history.html',
                           paginated_cards=sorted_history,
                           current_page=page)
