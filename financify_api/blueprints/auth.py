"""authentication endpoints"""

from typing import Dict, Union

from flask import Blueprint, g, request, session
from werkzeug.security import check_password_hash, generate_password_hash

from financify_api.library.db_connector import get_db

blueprint = Blueprint("auth", __name__, url_prefix="/auth")


# def login_required(view):
#     """wrapper for requiring an active user

#     :param view: """

#     @functools.wraps(view)
#     def wrapped_view(**kwargs):
#         if g.user is None:
#             return {"error": "user not logged in"}

#         return view(**kwargs)

#     return wrapped_view


@blueprint.before_app_request
def load_logged_in_user() -> None:
    """Set a global user object for the duration of the request"""
    user_id = session.get("user_id")

    if user_id is None:
        g.user = None
    else:
        g.user = (
            get_db().execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
        )


@blueprint.route("/register", methods=["POST"])
def register() -> Dict[str, Union[str, bool]]:
    """create new user record"""
    help_msg = (
        r"Post requires JSON object with structure: "
        r"{ username: <username>, password: <password> }"
    )
    username = request.json["username"]
    password = request.json["password"]
    db_client = get_db()
    error = None

    if not username:
        error = "Username is required."
    elif not password:
        error = "Password is required."

    if error is None:
        try:
            db_client.execute(
                "INSERT INTO users (username, password) VALUES (?, ?)",
                (username, generate_password_hash(password)),
            )
            db_client.commit()
        except db_client.IntegrityError:
            error = f"User {username} is already registered."
        else:
            return {"username": username, "registered": True}
    return {"error": error, "help": help_msg}


@blueprint.route("/login", methods=["POST"])
def login() -> Dict[str, Union[str, bool]]:
    """set user info for session if user exists"""
    help_msg = (
        r"Post requires JSON object with structure: "
        r"{ username: <username>, password: <password> }"
    )
    username = request.json["username"]
    password = request.json["password"]
    db_client = get_db()
    error = None
    user = db_client.execute(
        "SELECT username, password, id FROM users WHERE username = ?", (username,)
    ).fetchone()

    if user is None:
        error = "Incorrect username."
    elif not check_password_hash(
        user["password"], password
    ):  # type: ignore[no-untyped-call]
        error = "Incorrect password."

    if error is None:
        session.clear()
        session["user_id"] = user["id"]
        return {"username": user["username"], "logged_in": True}

    return {"error": error, "help": help_msg}


@blueprint.route("/logout")
def logout() -> Dict[str, Union[str, bool]]:
    """remove user from session"""
    session.clear()
    if session.get("user_id"):
        return {"error": "session not cleared"}
    return {"logged_out": True}
