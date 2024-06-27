"""project setup endtry points"""

import os
import sqlite3

import dotenv


def main() -> None:
    """create database file"""
    env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../.env")
    if not os.path.exists(env_path):
        dotenv.set_key(
            dotenv_path=env_path,
            key_to_set="DEMO_DB",
            value_to_set="${PWD}/dbs/demo.db",
        )
    dotenv.load_dotenv()
    if not os.path.exists(os.path.dirname(os.environ["DEMO_DB"])):
        os.makedirs(os.path.dirname(os.environ["DEMO_DB"]))
    db_client = sqlite3.connect(os.environ["DEMO_DB"])
    with open(
        os.path.join(os.path.dirname(__file__), "schema.sql"), "r", encoding="utf-8"
    ) as schema:
        db_client.executescript(schema.read())
    db_client.close()
