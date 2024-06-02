"""home resources"""

from typing import Any, Dict, Tuple

from flask_restful import Resource


class Home(Resource):  # type: ignore [misc]
    """home resource for testing"""

    def __init__(
        self,
    ) -> None:
        pass

    def get(self) -> Tuple[Dict[str, Any], int]:
        """Return hello world"""
        return ({"hello": "world"}, 200)
