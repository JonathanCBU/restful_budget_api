"""REST API app"""

import argparse
import os

import dotenv
from flask import Flask
from flask_restful import Api

from financify_api.resources.statements import Assets, Liabilities
from financify_api.resources.users import Users


def main() -> None:
    """Launch financify API server"""
    dotenv.load_dotenv()

    args = get_args()

    app = Flask(__name__)
    print(os.environ["DEMO_DB"])
    app.config.from_mapping(DATABASE=os.environ["DEMO_DB"], IS_ADMIN=args.admin)
    api = Api(app)
    api.add_resource(Assets, "/assets", "/assets/<int:record_id>")
    api.add_resource(Liabilities, "/liabilities", "/liabilities/<int:record_id>")
    api.add_resource(Users, "/users", "/users/<int:user_id>")
    app.run(debug=args.debug)


def get_args() -> argparse.Namespace:
    """Parse server CLI"""
    parser = argparse.ArgumentParser(
        description="Command line args for starting the Financify backend server"
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        default=False,
        help="Enable debug mode when running the app",
    )
    parser.add_argument(
        "--admin", action="store_true", default=False, help="Run app as admin"
    )

    args = parser.parse_args()
    return args
