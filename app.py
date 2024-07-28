from flask import Flask

from api import init_api
# from api.student import student_blueprint
# from api.course import course_blueprint
from database import init_db
from database.generate_data import generate_all




app = Flask(__name__)
init_api(app)

init_db()

generate_all()


def hello_world():
    return "Hello, World!"


print(app.url_map)
if __name__ == "__main__":
    app.run(debug=True)
