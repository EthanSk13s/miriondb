import sqlalchemy

from collections.abc import Sequence

from flask import Blueprint, jsonify, abort
from sqlalchemy import select

from mirion.database import db
from mirion.models import Card, Event
from mirion.utils import helpers

main_page = Blueprint("main", __name__)


@main_page.app_errorhandler(404)
def resource_not_found(e):
    return jsonify({'data': {'error': "Resource Not Found"}}), 404

@main_page.route("/latest")
def latest():
    recent_datetime = db.session.scalar(
        select(Card.release)
            .filter(Card.event_id == None,
                    Card.release != None,
                    Card.idol_type != 5)
            .order_by(Card.release.desc())
    )

    if recent_datetime is None:
        abort(404)
    
    recent_additions = db.session.scalars(
        select(Card)
            .filter(Card.release == recent_datetime,
                    Card.event_id == None)
            .order_by(Card.id.asc())
    ).all()

    current_event = db.session.scalar(
        select(Event)
            .order_by(Event.begin.desc())
    )

    if current_event is None:
        abort(404)

    event_cards: Sequence[Card] = []
    if current_event.event_type in (3, 4, 5, 9, 11, 13, 16):
        event_cards = db.session.scalars(
            select(Card)
                .filter(Card.event_id == current_event.id,
                        sqlalchemy.or_(Card.rarity.in_([3, 2])))
        ).all()

    previous_dates = db.session.scalars(
        select(Card.release)
            .filter(Card.release != recent_datetime,
                    Card.event_id == None)
            .order_by(Card.release.desc())
            .group_by(Card.release)
    ).all()[0:2]

    dates = [release for release in previous_dates]
    previous_additions = db.session.scalars(
        select(Card)
            .filter(Card.release.in_(dates))
            .order_by(Card.release.desc())
    ).all()

    sorted_additions: list[list[Card]] = helpers.list_grouper(previous_additions,
                                                              helpers.check_for_release)
    
    payload = {
        'currentEvent': 
            {
                'event': current_event.serialize,
            },
        'recentCards': [card.mini_serialize for card in recent_additions],
        'previousAdditions': []
    }

    if event_cards:
        payload['currentEvent']['cards'] = [card.mini_serialize for card in event_cards]
    else:
        payload['currentEvent']['cards'] = None

    prev_list = []
    for date in sorted_additions:
        prev_list.append([card.mini_serialize for card in date])

    payload['previousAdditions'] = prev_list

    return jsonify({'data': payload})

@main_page.route("/history/<int:page>")
def history(page: int):    
    dates = db.paginate(
        select(Card.release)
                .order_by(Card.release.desc())
                .group_by(Card.release),
        page = page,
        per_page = 10,
        error_out = False
    )

    # TODO: Properly separate event cards from regular cards
    paginated_cards = db.session.scalars(
        select(Card)
            .filter(Card.release.in_(dates))
            .order_by(Card.release.desc())
    ).all()

    sorted_history = helpers.list_grouper(paginated_cards,
                                          helpers.check_for_release)

    temp_list = []
    for date in sorted_history:
        temp_list.append([card.mini_serialize for card in date])

    return jsonify({'data': temp_list, 'hasNext': dates.has_next, 'hasPrev': dates.has_prev})
