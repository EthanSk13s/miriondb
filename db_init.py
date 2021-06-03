from mirion import database, create_app
from mirion.utils import fetch

app = create_app('config.Config')

client = app.pryncess

if __name__ == "__main__":
    with app.app_context():
        cards = client.get_all_cards(tl=True)

        for card in cards:
            fetch.get_card(card, database.db)

        events = client.get_all_events()

        for event in events:
            fetch.get_events(event, database.db)

        database.db.session.commit()
