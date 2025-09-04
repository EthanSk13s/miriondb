from flask import Blueprint, jsonify, request, abort
from sqlalchemy import select

from mirion.database import db
from mirion.models import Card
from mirion.utils import enums


card_page = Blueprint("card", __name__)


@card_page.route("/card/<card_id>")
def card(card_id: int):
    card = db.session.scalar(
        select(Card)
            .filter_by(id=card_id)
    )

    if card is not None:
        enums.set_enums(card)

        return jsonify({'data': card.serialize})
    else:
        return abort(404)


@card_page.route("/idol_query", methods=['POST'])
def handle_query():
    form = request.form.get("card-search")
    if not form:
        abort(404)

    query = form.split(" ")
    release = None
    rarity = None
    idol_id = 0

    if len(query) == 1:
        idol_id = enums.NAMES.get_id(query[0].lower())
        return jsonify({'data': {'idolId': idol_id}})

    for param in query:
        if param.isdigit():
            release = param
        if not idol_id:
            idol_id = enums.NAMES.get_id(param.lower())
            if not idol_id:
                abort(404)

        if not rarity:
            rarity = enums.get_rarity(param.lower())

    if release is not None:
        i = int(release) - 1
        filters = [Card.idol_id == idol_id]

        if rarity is not None:
            filters.append(Card.rarity == rarity)

        filters.append(Card.ex_type.notin_(enums.ANNIV_TYPES))

        try:
            card = db.session.scalars(
                select(Card)
                    .filter(*filters)
                    .order_by(Card.id.asc())
            ).all()[i]

            return jsonify({'data': {'cardId': card.id}})
        except IndexError:
            abort(404)
    else:
        return jsonify({'data': {'idolId': idol_id, 'rarity': rarity}})


@card_page.route("/idol/<id>", methods=['GET'])
def idol(id: int):
    rarity = request.args.get('rarity', type=int)

    kwargs = {"idol_id": id}
    if rarity:
        kwargs["rarity"] = rarity

    cards = db.session.scalars(
        select(Card)
            .filter_by(**kwargs)
            .order_by(Card.id.asc())
    ).all()

    if not cards:
        return abort(404)

    for card in cards:
        enums.set_enums(card)

    return jsonify({'data': [card.serialize for card in cards]})
