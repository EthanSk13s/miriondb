from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()


def init_app(app):
    with app.app_context():
        db.init_app(app)
        db.create_all()
    migrate.init_app(app, db)
