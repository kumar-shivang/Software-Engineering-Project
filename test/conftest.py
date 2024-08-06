import os
import sys

import mongomock
from flask import Flask
from mongoengine import connect, disconnect
from pytest import fixture

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from api import init_api


@fixture(scope="module")
def app():
    app = Flask(__name__)
    app.config["TESTING"] = True

    init_api(app)

    with app.app_context():
        yield app


@fixture(scope="module")
def client(app):
    return app.test_client()


@fixture(scope="module")
def init_db():
    connect(
        "test", host="mongodb://localhost", mongo_client_class=mongomock.MongoClient
    )
    yield
    disconnect()


@fixture(scope="module")
def runner(app):
    return app.test_cli_runner()

