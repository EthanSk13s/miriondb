import logging
import pryncess

from flask import Flask, render_template
from mirion import views, database, task


def create_app(config):

    app = Flask(__name__)
    app.config.from_object(config)

    app.pryncess = pryncess.Pryncess("ja")

    app.static_folder = "static"

    # Setup Logging
    app.event_handler = logging.basicConfig(
        filename='app.log', level=logging.DEBUG
    )
    app.logger.addHandler(app.event_handler)

    # Setup Database
    database.init_app(app)

    # Start Background tasks
    app.first_run = 0  # So tasks don't fire twice
    task.init_app(app)

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html'), 404

    views.register_views(app)

    return app
