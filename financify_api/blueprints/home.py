"""home endpoint"""

from typing import Dict

from flask import Blueprint, g, session

blueprint = Blueprint("home", __name__, url_prefix="/home")


@blueprint.route("/")
def home() -> Dict[str, str]:
    """say hi"""
    return {"greeting": "Hello from Financify"}


@blueprint.route("/whoami", methods=["GET"])
def whoami() -> Dict[str, str]:
    """return current username and ID"""
    user_id = session.get("user_id")
    if user_id is None:
        return {"error": "no logged in user"}
    return {"user_id": user_id, "username": g.user["username"]}
