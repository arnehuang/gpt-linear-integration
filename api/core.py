import logging
import traceback
from typing import List, Tuple

from flask import current_app, jsonify
from flask.wrappers import Response
from werkzeug.local import LocalProxy

# logger object for all routes to use
logger = LocalProxy(lambda: current_app.logger)
core_logger = logging.getLogger("core")


def create_response(
    data: dict = None, status: int = 200, message: str = ""
) -> Tuple[Response, int]:
    """Wraps response in a consistent format throughout the API.

    data must be a dictionary where:
    - the key is the name of the type of data
    - the value is the data itself

    :param data <str> optional data
    :param status <int> optional status code, defaults to 200
    :param message <str> optional message
    :returns tuple of Flask Response and int
    """
    if type(data) is not dict and data is not None:
        raise TypeError("Data should be a dictionary 😞")

    response = {"success": 200 <= status < 300, "message": message, "result": data}
    return jsonify(response), status


def serialize_list(items: List) -> List:
    """Serializes a list of SQLAlchemy Objects, exposing their attributes.

    :param items - List of Objects that inherit from Mixin
    :returns List of dictionaries
    """
    if not items or items is None:
        return []
    return [x.to_dict() for x in items]


def all_exception_handler(error: Exception) -> Tuple[Response, int]:
    """Catches and handles all exceptions, add more specific error Handlers.
    :param Exception
    :returns Tuple of a Flask Response and int
    """
    traceback.print_exc()
    logger.error(f"Exception: {error}")
    return create_response(message=str(error), status=500)
