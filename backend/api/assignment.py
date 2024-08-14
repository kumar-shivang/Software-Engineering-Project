from flask import Blueprint, jsonify, request, g
from database.tables import Assignment, Submission, ProgrammingAssignment
from mongoengine.errors import ValidationError
from . import api, token_required
from api.utils.serializer import serialize_assignment, serialize_submission, serialize_programming_assignment

assignment_blueprint = Blueprint("assignment", __name__, url_prefix="/assignment")


# NOTE: get programming assignment
@assignment_blueprint.route("/programming_assignments/<assignment_id>", methods=["GET"])
@token_required
def get_programming_assignments(assignment_id):
    assignment = ProgrammingAssignment.objects(id=assignment_id).first()
    if assignment is None:
        return jsonify({"error": "Programming Assignment not found"}), 404
    return jsonify({"data": serialize_programming_assignment(assignment)  })



# NOTE: get assignment
@assignment_blueprint.route("/<assignment_id>", methods=["GET"])
@token_required
def get_assignment(assignment_id):
    assignment = Assignment.objects(id=assignment_id).first()
    if assignment is None:
        return jsonify({"data": [], "error": "Assignments not found"}), 404
    return jsonify({"data": serialize_assignment(assignment)}), 200


# NOTE: Route for submitting answers for an assignment
@assignment_blueprint.route("/<assignment_id>/submit", methods=["POST"])
@token_required
def submit_assignment(assignment_id):
    data = request.json
    answers = data.get("answers")
    if not all([assignment_id, answers]):
        return jsonify({"error": "Missing required fields"}), 400
    try:
        student = g.current_user
        assignment = Assignment.objects(id=assignment_id).first()
        if not assignment:
            return jsonify({"error": "Assignment not found"}), 404
        if student not in assignment.week.course.students:
            return jsonify({"error": "Student not enrolled in the course"}), 403
        submission = Submission(student=student, assignment=assignment, answers=answers)
        submission.grade_submission()
        submission.save()
        student.submissions.append(submission)
        student.grades[str(assignment_id)] = submission.get_total_grade()
        student.save()
        return jsonify({"data": serialize_submission(submission)}), 200
    except ValidationError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500


api.register_blueprint(assignment_blueprint)
