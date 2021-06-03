from flask import Blueprint, render_template, request, redirect, abort
import jinja2

from mirion.models import Card
from mirion.utils import enums


card_page = Blueprint("card", __name__)


@card_page.route("/card/<card_id>")
def card(card_id):
    card = Card.query.filter_by(id=card_id).first()
    enums.set_enums(card)

    return render_template('card_view.html', card=card)


@card_page.route("/idol_query", methods=['POST'])
def handle_query():
    query = request.form.get('card-search').split(" ")
    release = None
    got_idol = 0
    got_rarity = 0

    if len(query) == 1:
        idol_id = enums.match_name(query[0].lower())
        return redirect(f"/idol/{idol_id}")

    for param in query:
        if param.isdigit():
            release = param
        if got_idol == 0:
            idol_id = enums.match_name(param.lower())
            if idol_id is not False:
                got_idol = 1
        else:
            pass
        if got_rarity == 0:
            rarity = enums.get_rarity(param.lower())
            if rarity is not False:
                got_rarity = 1
        else:
            pass

    if release is not None:
        i = int(release) - 1
        card = Card.query.filter_by(idol_id=idol_id, rarity=rarity).all()[i]

        return redirect(f"/card/{card.id}")
    else:
        return redirect(f"/idol/{idol_id}?rarity={rarity}")


@card_page.route("/idol/<id>", methods=['GET'])
def idol(id):
    if len(request.args) != 0:
        rarity = request.args.get('rarity')
        cards = Card.query.filter_by(idol_id=id, rarity=rarity).all()
    else:
        cards = Card.query.filter_by(idol_id=id).all()

    for card in cards:
        enums.set_enums(card)

    try:
        return render_template('idol_view.html', idol_cards=cards)
    except jinja2.exceptions.UndefinedError:
        abort(404)
