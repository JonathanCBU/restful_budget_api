"""core app entry point"""

from flask import Flask
from flask_restful import Api
import argparse
import dotenv
import os

def main() -> None:
    """main entrypoint for running flask server"""
    dotenv.load_dotenv()
    args = get_args()
    app = create_app(os.environ["DEMO_DB"], args.debug)
    api = create_api(app)
    for resource in api.resources:
        print(f"Added resource: {resource}")
    app.run(host=args.host, port=args.port)


def create_app(database: str, debug: bool) -> Flask:
    """generate the Flask object without starting the server
    
    :param database: absolute path to your db file
    :param debug: if True, configure server for debug mode
    """
    app = Flask(__name__)
    app.config["DATABASE"] = database
    app.config["DEBUG"] = debug
    return app
         

def create_api(app: Flask) -> Api:
    """create an Api and add resources with endpoints
    
    :param app: Flask object to build Api from
    """
    api = Api(app)
    return api


def get_args() -> argparse.Namespace:
    """parse server CLI"""
    parser = argparse.ArgumentParser(
        description=(
            "Command line args for starting the Financify backend server"
        )
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        default=False,
        help="Enable debug mode when running the app",
    )
    parser.add_argument(
        "--host",
        default=None,
        help="Specify server host. Will default to localhost if left None",
    )
    parser.add_argument("--port", default=None, help="Specify server port")
    args = parser.parse_args()
    return args