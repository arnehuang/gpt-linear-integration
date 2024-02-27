from flask import Blueprint

from api.core import logger

main = Blueprint("main", __name__)  # initialize blueprint


@main.route("/")
def index():
    return "<h1>Hello World!</h1>"


@main.route("/health")
def health_check():
    return "OK", 200
