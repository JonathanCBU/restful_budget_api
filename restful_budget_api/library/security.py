"""security wrappers and auth checks"""

import functools
from typing import Any, Callable, Dict, Tuple, TypeVar, Union, cast

from flask import request
from flask_restful import current_app

from restful_budget_api.library.db_connector import db_fetchall, db_fetchone

F = TypeVar("F", bound=Callable[..., Any])


def admin_required(func: F) -> F:
    """decorator requiring server to be running in admin mode"""

    @functools.wraps(func)
    def decorator(*args: Any, **kwargs: Any) -> Union[F, Tuple[Dict[str, str], int]]:
        if current_app.config["IS_ADMIN"]:
            return cast(F, func(*args, **kwargs))
        return ({"error": "server not running in admin mode"}, 403)

    return cast(F, decorator)


def api_key_required(func: F) -> F:
    """require api_key passed with request json"""

    @functools.wraps(func)
    def decorator(*args: Any, **kwargs: Any) -> Union[F, Tuple[Dict[str, str], int]]:
        if not request.headers.get("Authorization"):
            return (
                {
                    "error": "Please provide an API key in the Authorization header of your request"
                },
                400,
            )
        user_key = request.headers.get("Authorization")
        api_keys = [
            api_key[0] for api_key in db_fetchall(sql="SELECT password FROM users")
        ]
        if user_key not in api_keys:
            return ({"error": "API key not valid"}, 401)
        return cast(F, func(*args, **kwargs))

    return cast(F, decorator)


def strict_verbiage(func: F) -> F:
    """require function names to match HTTP verbs being requested"""

    @functools.wraps(func)
    def decorator(*args: Any, **kwargs: Any) -> Union[F, Tuple[Dict[str, str], int]]:
        if func.__name__ != request.method.lower():
            return (
                {"error": f"user {request.method} verb with {func.__name__} method"},
                405,
            )
        return cast(F, func(*args, **kwargs))

    return cast(F, decorator)


def get_user() -> int:
    """get a user ID from an API key

    :param api_key: user's api key
    """
    user_id = db_fetchone(
        "SELECT id FROM users WHERE password = ?", (request.headers["Authorization"],)
    )
    return int(user_id[0])
