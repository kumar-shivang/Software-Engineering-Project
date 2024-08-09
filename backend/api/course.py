from flask import jsonify, Blueprint
from database.tables import Course
from . import api
from api.utils.serializer import serialize_doc, serialize_course

course_blueprint = Blueprint("course", __name__, url_prefix="/course")


# NOTE: get all courses
@course_blueprint.route("/", methods=["GET"])
def get_courses():
    courses = Course.objects()
    if not courses:
        return jsonify({"data": [], "message": "No courses found"}), 200
    courses_list = [serialize_doc(course) for course in courses]
    return jsonify({"data": courses_list}), 200


# NOTE: get courses details by course id
@course_blueprint.route("/<course_id>", methods=["GET"])
def get_course(course_id):
    course = Course.objects(id=course_id).first()
    if course is None:
        return jsonify({"data": [], "error": "Course not found"}), 404
    return jsonify({"data": serialize_course(course)}), 200


# NOTE: get students by course id
@course_blueprint.route("/students/<course_id>", methods=["GET"])
def get_students(course_id):
    course = Course.objects(id=course_id).first()
    if course is None:
        return jsonify({"data": [], "error": "Course not found"}), 404
    students = course.students
    return {"data": [student.to_json() for student in students]}, 200


# NOTE: get assignments by course_id
@course_blueprint.route("/assignments/<course_id>", methods=["GET"])
def get_assignments(course_id):
    course = Course.objects(id=course_id).first()
    if not course:
        return jsonify({"data": [], "messaage": "Assignments not found"}), 200
    assignments = course.assignments
    return {"data": [assignment.to_json() for assignment in assignments]}, 200


# NOTE: get weeks by course_id
@course_blueprint.route("/weeks/<course_id>", methods=["GET"])
def get_weeks(course_id):
    course = Course.objects(id=course_id).first()
    if course is None:
        return jsonify({"data": [], "error": "Course not found"}), 404
    weeks = course.weeks
    return {"data": [week.to_json() for week in weeks]}, 200


api.register_blueprint(course_blueprint)
