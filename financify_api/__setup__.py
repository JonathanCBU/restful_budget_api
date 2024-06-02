"""project setup endtry points"""

import argparse
import os
import sqlite3

import dotenv


def main() -> None:
    """create database file"""
    # dotenv.load_dotenv()
    args = get_args()
    env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../.env")
    if args.init_env or not os.path.exists(env_path):
        dotenv.set_key(
            dotenv_path=env_path,
            key_to_set="DEMO_DB",
            value_to_set="${HOME}/dbs/demo.db",
        )
    dotenv.load_dotenv()
    if not args.db:
        args.db = ["DEMO_DB", os.environ["DEMO_DB"]]
    if args.db[0] not in os.environ:
        dotenv.set_key(
            dotenv_path=env_path, key_to_set=args.db[0], value_to_set=args.db[1]
        )
    db_client = sqlite3.connect(args.db[1])
    with open(
        os.path.join(os.path.dirname(__file__), args.schema), "r", encoding="utf-8"
    ) as schema:
        db_client.executescript(schema.read())
    db_client.close()


def get_args() -> argparse.Namespace:
    """get command line args"""
    parser = argparse.ArgumentParser(
        description="command line arguments for setting up the database"
    )

    parser.add_argument(
        "--init_env",
        action="store_true",
        default=False,
        help="create or overwrite existing .env file",
    )
    parser.add_argument(
        "--db",
        nargs="+",
        help="'<NAME>, <db path>' databse to get from or add to .env",
    )
    parser.add_argument("--schema", default="schema.sql", help="path to schema file")
    args = parser.parse_args()
    return args
