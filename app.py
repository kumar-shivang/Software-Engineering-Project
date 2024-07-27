from flask import Flask

from api import api
from api.student import *
from database import init_db
from database.generate_data import generate_all
from llm import llm


app = Flask(__name__)
app.register_blueprint(llm)
app.register_blueprint(api)
init_db()

generate_all()


def hello_world():
    return "Hello, World!"


print(app.url_map)
if __name__ == "__main__":
    app.run(debug=True)
