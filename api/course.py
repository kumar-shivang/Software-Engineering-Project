from flask import jsonify, Blueprint

from database.tables import Course

from . import api

course_blueprint = Blueprint("course", __name__, url_prefix="/course")


@course_blueprint.route("/", methods=["GET"])
def get_courses():
    courses = Course.objects().to_json()
    return courses


@course_blueprint.route("/<course_id>", methods=["GET"])
def get_course(course_id):
    course = Course.objects(id=course_id).first()
    return course.to_json()


@course_blueprint.route("/students/<course_id>", methods=["GET"])
def get_students(course_id):
    course = Course.objects(id=course_id).first()
    students = course.students
    return jsonify({"students": [student.to_json() for student in students]})


@course_blueprint.route("/assignments/<course_id>", methods=["GET"])
def get_assignments(course_id):
    course = Course.objects(id=course_id).first()
    assignments = course.assignments
    return jsonify({"assignments": [assignment.to_json() for assignment in assignments]})


@course_blueprint.route("/weeks/<course_id>", methods=["GET"])
def get_weeks(course_id):
    course = Course.objects(id=course_id).first()
    weeks = course.weeks
    return jsonify({"weeks": [week.to_json() for week in weeks]})


api.register_blueprint(course_blueprint)
