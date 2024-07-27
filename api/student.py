import email
from . import api
from flask import request, jsonify
from database.tables import Student, Assignment, Submission

@api.route("/student",methods=["GET"])
def get_students():
    students = Student.objects().to_json()
    return students

@api.route("/submit",methods=["POST"])
def submit():
    data = request.json
    print(data)
    student = Student.objects(id=data["student_id"]).first()
    assignment = Assignment.objects(id=data["assignment_id"]).first()
    answers = data["answers"]
    student.submit(assignment.id,answers)
    return jsonify({"message":"Submitted"})







