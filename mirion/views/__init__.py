from flask import Flask
from mirion.views import main, card


def register_views(app: Flask):
    app.register_blueprint(main.main_page, url_prefix="/api")
    app.register_blueprint(card.card_page, url_prefix="/api")
