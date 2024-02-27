import logging
import os

from dotenv import load_dotenv
from flask import Flask, request
from flask_cors import CORS
from flask_talisman import Talisman
from werkzeug.middleware.proxy_fix import ProxyFix

from api.config import config
from api.core import all_exception_handler
from api.routes import classifier_routes


class RequestFormatter(logging.Formatter):
    def format(self, record):
        record.url = request.url
        record.remote_addr = request.remote_addr
        return super().format(record)


def create_app():
    load_dotenv()
    app = Flask(__name__)
    app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_host=1, x_proto=1, x_port=1)
    Talisman(app)  # force https
    CORS(app)  # add CORS

    # check environment variables to see which config to load
    env = os.environ.get("FLASK_ENV", "dev")
    # for configuration options, look at api/config.py
    app.config.from_object(config[env])

    # logging
    formatter = RequestFormatter(
        "%(asctime)s %(remote_addr)s: requested %(url)s: %(levelname)s in [%(module)s: %(lineno)d]: %(message)s"
    )
    if app.config.get("LOG_FILE"):
        fh = logging.FileHandler(app.config.get("LOG_FILE"))
        fh.setLevel(logging.DEBUG)
        fh.setFormatter(formatter)
        app.logger.addHandler(fh)

    strm = logging.StreamHandler()
    strm.setLevel(logging.DEBUG)
    strm.setFormatter(formatter)

    app.logger.addHandler(strm)
    app.logger.setLevel(logging.DEBUG)

    root = logging.getLogger("core")
    root.addHandler(strm)

    # import and register blueprints
    from api.routes import main

    app.register_blueprint(main.main)
    app.register_blueprint(classifier_routes.classifier_routes)

    # register error Handler
    app.register_error_handler(Exception, all_exception_handler)

    return app
