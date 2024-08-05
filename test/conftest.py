from pytest import fixture
from app import app as flask_app
from mongoengine import connect, disconnect
import mongomock


@fixture(scope="module")
def app():
    flask_app.config.update(
        TESTING=True,
    )
    with flask_app.app_context():
        # connect("test",
        # host="mongodb://localhost",
        # mongo_client_class=mongomock.MongoClient)
        yield flask_app
    disconnect()


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
