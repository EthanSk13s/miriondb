import jinja2

from flask import Blueprint, jsonify, request, abort
from mirion.models import Card
from mirion.utils import enums


card_page = Blueprint("card", __name__)


@card_page.route("/card/<card_id>")
def card(card_id):
    card: Card = Card.query.filter_by(id=card_id).first()
    if card is not None:
        enums.set_enums(card)

        return jsonify({'data': card.serialize})
    else:
        return abort(404)


@card_page.route("/idol_query", methods=['POST'])
def handle_query():
    query = request.form.get('card-search').split(" ")
    release = None
    got_idol = 0
    got_rarity = 0

    if len(query) == 1:
        idol_id = enums.NAMES.get_id(query[0].lower())
        return jsonify({'data': {'idolId': idol_id}})

    for param in query:
        if param.isdigit():
            release = param
        if got_idol == 0:
            idol_id = enums.NAMES.get_id(param.lower())
            if idol_id is not None:
                got_idol = 1
            else:
                abort(404)
        else:
            pass
        if got_rarity == 0:
            rarity = enums.get_rarity(param.lower())
            if rarity is not False:
                got_rarity = 1
        else:
            pass

    if release is not None:
        allowed_types = [0, 1, 2, 3, 4, 6, 8, 9, 11, 12, 14, 19]
        i = int(release) - 1
        filters = [Card.idol_id == idol_id]

        if rarity is not False:
            filters.append(Card.rarity == rarity)

        filters.append(Card.ex_type.in_(allowed_types))

        try:
            card = Card.query.filter(*filters).order_by(Card.id.asc()).all()[i]
            return jsonify({'data': {'cardId': card.id}})
        except IndexError:
            abort(404)
    else:
        return jsonify({'data': {'idolId': idol_id, 'rarity': rarity}})


@card_page.route("/idol/<id>", methods=['GET'])
def idol(id):
    if len(request.args) != 0:
        rarity = request.args.get('rarity')
        cards = Card.query.filter_by(idol_id=id, rarity=rarity).order_by(Card.id.asc()).all()
    else:
        cards = Card.query.filter_by(idol_id=id).order_by(Card.id.asc()).all()

    for card in cards:
        enums.set_enums(card)

    try:
        return jsonify({'data': [card.serialize for card in cards]})
    except jinja2.exceptions.UndefinedError:
        abort(404)
