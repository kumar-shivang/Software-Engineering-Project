from ast import Sub
import jwt
import datetime
from flask import Blueprint, jsonify, request, current_app, g
from werkzeug.security import check_password_hash
from functools import wraps

from yaml import serialize
from database.tables import Assignment, Student, Submission
from . import api, token_required
from api.utils.serializer import serialize_submission

student_blueprint = Blueprint("student", __name__, url_prefix="/student")


# NOTE: return all students
@student_blueprint.route("/", methods=["GET"])
@token_required
def get_students():
    students = Student.objects().to_json()
    return students


# NOTE: assignment submission
@student_blueprint.route("/submit", methods=["POST"])
@token_required
def submit():
    data = request.json
    print(data)
    student = g.current_user
    assignment = Assignment.objects(id=data["assignment_id"]).first()
    if assignment is None:
        return jsonify({"error": "Assignment not found"}), 404
    answers = data["answers"]
    submission_id = student.submit(assignment.id, answers)
    return jsonify(
        {"message": "Submitted", "data": {"submission_id": str(submission_id)}}
    )


@student_blueprint.route("/submit/programming/<assignment_id>", methods=["POST"])
@token_required
def submit_programming(assignment_id):
    data = request.json
    student = g.current_user
    assignment = Assignment.objects(id=assignment_id).first()
    if assignment is None:
        return jsonify({"error": "Assignment not found"}), 404
    code = data["code"]
    result = student.submit_programming(assignment.id, code)
    return jsonify({"message": "Submitted", "result": result})


# NOTE: get student by id
@student_blueprint.route("/<student_id>", methods=["GET"])
@token_required
def get_student(student_id):
    student = Student.objects(id=student_id).first()
    if student is None:
        return jsonify({"error": "Student not found"}), 404
    return student.to_json()


# NOTE: get courses by student id
@student_blueprint.route("/courses/<student_id>", methods=["GET"])
@token_required
def get_courses(student_id):
    student = Student.objects(id=student_id).first()
    if student is None:
        return jsonify({"error": "Student not found"}), 404
    courses = student.courses
    return jsonify({"courses": [course.to_json() for course in courses]})


# NOTE: get assignments by student id
@student_blueprint.route("/score", methods=["GET"])
@token_required
def get_score():
    data = request.json
    student = g.current_user
    assignment_id = data["assignment_id"]

    if not Assignment.objects(id=assignment_id).first():
        return jsonify({"error": "Assignment not found"}), 404
    return jsonify({"score": student.get_score(assignment_id)})


# NOTE: student login
@student_blueprint.route("/login", methods=["POST"])
def login():
    data = request.json
    print("data", data)
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"error": "Email and password are required"}), 400

    student = Student.objects(email=email, password=password).first()
    if student:
        print("student", student)
        token = jwt.encode(
            {
                "student_id": str(student.id),
                "exp": datetime.datetime.now() + datetime.timedelta(hours=1),
            },
            current_app.config["SECRET_KEY"],
            algorithm="HS256",
        )
        return jsonify({"message": "Login successful", "token": token})
    else:
        return jsonify({"error": "Invalid username or password"}), 401


@student_blueprint.route("/get_result/<submission_id>", methods=["GET"])
@token_required
def get_result(submission_id):
    submission = Submission.objects(id=submission_id).first()
    if not submission:
        return jsonify({"error": "Submission not found"}), 404
    print(submission.to_json())
    data = submission.get_result()
    return jsonify({"data": data})


api.register_blueprint(student_blueprint)
