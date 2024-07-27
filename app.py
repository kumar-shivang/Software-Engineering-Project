from flask import Flask
from llm import llm
from database import init_db
from database.generate_data import *
from api.student import *


app = Flask(__name__)
app.register_blueprint(llm)
app.register_blueprint(api)
init_db()


generate_students()
generate_courses()
generate_enrollments()
generate_weeks()
generate_lectures()
generate_assignments()
generate_questions()



def hello_world():
    return "Hello, World!"


print(app.url_map)
if __name__ == "__main__":
    app.run(debug=True)
