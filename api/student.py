import email
from . import api
from flask import request, jsonify, Blueprint
from database.tables import Student, Assignment
student = Blueprint("student",__name__,url_prefix="/student")

api.register(student)

@student.route("/student",methods=["GET"])
def get_students():
    students = Student.objects().to_json()
    return students

@student.route("/submit",methods=["POST"])
def submit():
    data = request.json
    print(data)
    student = Student.objects(id=data["student_id"]).first()
    assignment = Assignment.objects(id=data["assignment_id"]).first()
    answers = data["answers"]
    student.submit(assignment.id,answers)
    return jsonify({"message":"Submitted"})

@student.route("/student_id>",methods=["GET"])
def get_student(student_id):
    student = Student.objects(id=student_id).first()
    return student.to_json()

@student.route("/courses/<student_id>",methods=["GET"])
def get_courses(student_id):
    student = Student.objects(id=student_id).first()
    courses = student.courses
    return jsonify({"courses":[course.to_json() for course in courses]})

@student.route("/score",methods=["GET"])
def get_score(student_id):
    data = request.json
    student_id = data["student_id"]
    assignment_id = data["assignment_id"]

    student = Student.objects(id=student_id).first()
    return jsonify({"score":student.get_score(assignment_id)})






