from flask import Flask
from flask_cors import CORS

from app.extensions import api
from .endpoints import market
from .config import Config


def create_app(config=Config):
    app = Flask(__name__)
    app.config.from_object(config)

    CORS(app)
    api.init_app(app)
    api.add_namespace(market.ns)
    return app