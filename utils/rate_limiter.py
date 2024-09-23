from flask_limiter import Limiter
from flask import jsonify
from flask_limiter.util import get_remote_address
import os

MONGO_URI = os.getenv("MONGO_URI")


def configure_limiter(app):
    limiter = Limiter(
        key_func=get_remote_address,
        app=app,
        storage_uri=os.getenv("MONGO_URI"))
    return limiter
