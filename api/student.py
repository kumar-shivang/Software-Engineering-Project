from flask import Blueprint, jsonify, request

from database.tables import Assignment, Student

from . import api

student_blueprint = Blueprint("student", __name__, url_prefix="/student")



@student_blueprint.route("/", methods=["GET"])
def get_students():
    students = Student.objects().to_json()
    return students


@student_blueprint.route("/submit", methods=["POST"])
def submit():
    data = request.json
    print(data)
    student = Student.objects(id=data["student_id"]).first()
    assignment = Assignment.objects(id=data["assignment_id"]).first()
    answers = data["answers"]
    student.submit(assignment.id, answers)
    return jsonify({"message": "Submitted"})


@student_blueprint.route("/student_id>", methods=["GET"])
def get_student(student_id):
    student = Student.objects(id=student_id).first()
    return student.to_json()


@student_blueprint.route("/courses/<student_id>", methods=["GET"])
def get_courses(student_id):
    student = Student.objects(id=student_id).first()
    courses = student.courses
    return jsonify({"courses": [course.to_json() for course in courses]})


@student_blueprint.route("/score", methods=["GET"])
def get_score(student_id):
    data = request.json
    student_id = data["student_id"]
    assignment_id = data["assignment_id"]

    student = Student.objects(id=student_id).first()
    return jsonify({"score": student.get_score(assignment_id)})


api.register_blueprint(student_blueprint)



