"""REST API app"""

import argparse
import os
from typing import Any, Dict

import dotenv
from flask import Flask
from flask_restful import Api

from financify_api.resources.patterns import Patterns, PatternsById, PatternsByTitle
from financify_api.resources.statements import Assets, Liabilities, Reports
from financify_api.resources.users import Users
from financify_api.resources.utilities import Home


def main() -> None:
    """Launch financify API server"""
    dotenv.load_dotenv()

    args = get_args()
    args_dict = {"admin": args.admin, "database": args.db}
    app = create_app(args_dict)
    _ = create_api(app)
    app.run(debug=args.debug)


def create_app(args: Dict[str, Any]) -> Flask:
    """Create app object

    :param args: application setup args
    """
    app = Flask(__name__)
    app.config.from_mapping(DATABASE=args["database"], IS_ADMIN=args["admin"])
    return app


def create_api(app: Flask) -> Api:
    """Create api object and configure endpoints

    :param app: Flask app
    """
    api = Api(app)
    api.add_resource(Assets, "/assets", "/assets/<int:record_id>")
    api.add_resource(Liabilities, "/liabilities", "/liabilities/<int:record_id>")
    api.add_resource(Reports, "/reports", "/reports/<int:record_id>")
    api.add_resource(Users, "/users", "/users/<int:user_id>")
    api.add_resource(Patterns, "/patterns", "/patterns/")
    api.add_resource(PatternsByTitle, "/patterns/byTitle/<string:title>")
    api.add_resource(PatternsById, "/patterns/byId/<int:id_num>")
    api.add_resource(Home, "/home")
    return api


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
    parser.add_argument("--db", default=os.environ["DEMO_DB"], help="Select DB file")
    args = parser.parse_args()
    return args
