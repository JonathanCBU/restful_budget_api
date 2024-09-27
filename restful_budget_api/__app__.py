"""core app entry point"""

from flask import Flask
from flask_restful import Api
import argparse
import restful_budget_api.library.configs as configs
from restful_budget_api.library.db_context import make_db


def main() -> None:
    """main entrypoint for running flask server"""
    args = get_args()
    app = Flask(__name__)
    app.config.from_object(getattr(configs, args.config))
    make_db(app.config["DATABASE"], app.config["DB_SCHEMA"])
    api = Api(app)
    for resource in api.resources:
        print(f"Added resource: {resource}")
    app.run(host=args.host, port=args.port)


def get_args() -> argparse.Namespace:
    """parse server CLI"""
    parser = argparse.ArgumentParser(
        description=(
            "Command line args for starting the Financify backend server"
        )
    )
    parser.add_argument(
        "--config",
        default="Default",
        help="Specify server config",
    )
    parser.add_argument(
        "--host",
        default=None,
        help="Specify server host. Will default to localhost if left None",
    )
    parser.add_argument("--port", default=None, help="Specify server port")
    args = parser.parse_args()
    return args