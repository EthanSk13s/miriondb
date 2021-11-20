import logging
import logging.handlers
import pryncess

from flask import Flask
from mirion import views, database, task
from config import Config


def create_app(config=Config):
    app = Flask(__name__)
    app.config.from_object(config)

    app.pryncess = pryncess.Pryncess("ja")

    app.static_folder = "static"

    # Setup Logging
    app.event_handler = logging.basicConfig(
        format='%(asctime)s %(message)s',
        datefmt='%m/%d/%Y %I:%M:%S %p',
        handlers=[logging.handlers.RotatingFileHandler(
                  'app.log', 'w', encoding='utf-8',
                  maxBytes=10485760, backupCount=5),
                  logging.StreamHandler()],
        level=logging.DEBUG
    )
    app.logger.addHandler(app.event_handler)

    # Setup Database
    database.init_app(app)

    # Setup asset server address
    app.assets_addr = (app.config['ASSETS_HOST'], int(app.config['ASSETS_PORT']))

    # Start Background tasks
    app.first_run = 0  # So tasks don't fire twice
    task.init_app(app)

    views.register_views(app)

    return app
