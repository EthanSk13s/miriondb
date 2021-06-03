from mirion.views import main, card


def register_views(app):
    app.register_blueprint(main.main_page)
    app.register_blueprint(card.card_page)
