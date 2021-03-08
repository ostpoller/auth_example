import pathlib

import connexion

from . import config


def initialize_extensions(app):
    # extensions initialized/instantiated outside the app context and then bound to the app
    # context using their init_app() function
    from .models import db, migrate
    db.init_app(app)
    migrate.init_app(app, db)
    from .auth import login_manager
    login_manager.init_app(app)


def register_blueprints(app):
    with app.app_context():
        from . import views
        app.register_blueprint(views.bp, url_prefix='/')


def create_app(testing=False):
    # app does not exist at import time, so use current_app in other modules!
    cnx_app = connexion.App(__name__, specification_dir='.')
    cnx_app.add_api('openapi_specification.yaml', strict_validation=True, validate_responses=True)
    app = cnx_app.app
    if testing:
        app.config.from_object(config.TestingConfig)
    else:
        app.config.from_object(config.Config)
    initialize_extensions(app)
    register_blueprints(app)

    pathlib.Path(app.config["DATA_DIR"]).mkdir(parents=True, exist_ok=True)

    return app


if __name__ == '__main__':
    create_app().run(port=5000, ssl_context='adhoc')
