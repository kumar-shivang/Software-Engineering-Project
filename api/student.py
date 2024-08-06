from flask import Blueprint, jsonify, request

from database.tables import Assignment, Student
from . import api

student_blueprint = Blueprint("student", __name__, url_prefix="/student")


# NOTE: return all students
@student_blueprint.route("/", methods=["GET"])
def get_students():
    students = Student.objects().to_json()
    return students


# NOTE: assignment submission
@student_blueprint.route("/submit", methods=["POST"])
def submit():
    data = request.json
    student = Student.objects(id=data["student_id"]).first()
    if student is None:
        return jsonify({"error": "Student not found"}), 404
    assignment = Assignment.objects(id=data["assignment_id"]).first()
    if assignment is None:
        return jsonify({"error": "Assignment not found"}), 404
    answers = data["answers"]
    student.submit(assignment.id, answers)
    return jsonify({"message": "Submitted"})


# NOTE: get student by id
@student_blueprint.route("/<student_id>", methods=["GET"])
def get_student(student_id):
    student = Student.objects(id=student_id).first()
    if student is None:
        return jsonify({"error": "Student not found"}), 404
    return student.to_json()


# NOTE: get courses by student id
@student_blueprint.route("/courses/<student_id>", methods=["GET"])
def get_courses(student_id):
    student = Student.objects(id=student_id).first()
    if student is None:
        return jsonify({"error": "Student not found"}), 404
    courses = student.courses
    return jsonify({"courses": [course.to_json() for course in courses]})


# NOTE: get assignments by student id
@student_blueprint.route("/score", methods=["GET"])
def get_score():
    data = request.json
    student_id = data["student_id"]
    assignment_id = data["assignment_id"]

    student = Student.objects(id=student_id).first()
    if student is None:
        return jsonify({"error": "Student not found"}), 404
    if not Assignment.objects(id=assignment_id).first():
        return jsonify({"error": "Assignment not found"}), 404
    return jsonify({"score": student.get_score(assignment_id)})


api.register_blueprint(student_blueprint)
