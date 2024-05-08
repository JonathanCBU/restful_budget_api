"""home resources"""

from typing import Any, Dict, Tuple

from flask_restful import Resource, request

from financify_api.library.db_connector import db_fetchone

"flask.request.environ.get('werkzeug.server.shutdown')()"


class Home(Resource):  # type: ignore [misc]
    """home resource for testing"""

    def __init__(
        self,
    ) -> None:
        super().__init__()

    def get(self) -> Tuple[Dict[str, Any], int]:
        """Return hello world"""
        return ({"hello": "world"}, 200)


class Shutdown(Resource):  # type: ignore [misc]
    """shutdown signal to kill server"""

    def __init__(self) -> None:
        super().__init__()

    def post(self) -> Tuple[Dict[str, Any], int]:
        """Trigger server shutdown if user sends the god key"""
        god_key = db_fetchone("SELECT password from users where username = ?", ("god",))
        if request.json["api_key"] != god_key:
            return ({"error": "fire and brimstone shall rain down upon you"}, 403)
        return request.environ.get("werkzeug.server.shutdown")()
