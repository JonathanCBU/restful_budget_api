"""Initialize my flask app"""

import os

import dotenv
from flask import Flask

from financify_api.blueprints import auth, home
from financify_api.library.db_connector import close_db, init_db_command


def create_app(test_config: str = "") -> Flask:
    """Set up app and configure

    :param test_config: path to config file if testing
    """
    # get secrets
    dotenv.load_dotenv()

    # instantiate app
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_mapping(
        SECRET_KEY=os.environ["API_KEY"], DATABASE=os.environ["DEMO_DB"]
    )
    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile("config.py", silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
    app.register_blueprint(auth.blueprint)
    app.register_blueprint(home.blueprint)

    return app
