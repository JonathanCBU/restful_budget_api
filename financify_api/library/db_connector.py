"""API DB connection functions"""

import sqlite3
from typing import Union

import click
from flask import current_app, g


def get_db() -> sqlite3.Connection:
    """connect to db"""
    if "db" not in g:
        g.db = sqlite3.connect(
            current_app.config["DATABASE"], detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row
    if not isinstance(g.db, sqlite3.Connection):
        raise LookupError("Could not connect to database")
    return g.db


def init_db() -> None:
    """run schema sql file"""
    db = get_db()

    with current_app.open_resource("schema.sql") as f:
        db.executescript(f.read().decode("utf8"))


def close_db(err: Union[Exception, None] = None) -> None:
    """close db connection

    :param err: error message passed down to teardown
    """
    db = g.pop("db", None)

    if db is not None:
        db.close()
    if err:
        raise err


@click.command("init-db")
def init_db_command() -> None:
    """Clear the existing data and create new tables."""
    init_db()
    click.echo("Initialized the database.")
