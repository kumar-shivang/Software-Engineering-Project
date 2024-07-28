from flask import Blueprint, jsonify

from database.tables import Week, Assignment

from . import api

assignment_blueprint = Blueprint("assignment", __name__, url_prefix="/assignment")


# NOTE: get all assignments
@assignment_blueprint.route("/<week_id>", methods=["GET"])
def get_assignments(week_id):
    week = Week.objects(id=week_id).first()
    if week is None:
        return jsonify({"error": "Week not found"}), 404
    assignments = week.assignments
    return (
        jsonify({"assignments": [assignment.to_json() for assignment in assignments]}),
        200,
    )


# NOTE: get single assignment
@assignment_blueprint.route("/<assignment_id>", methods=["GET"])
def get_assignment(assignment_id):
    assignment = Assignment.objects(id=assignment_id).first()
    if assignment is None:
        return jsonify({"error": "Assignment not found"}), 404
    return assignment.to_json(), 200


api.register_blueprint(assignment_blueprint)
