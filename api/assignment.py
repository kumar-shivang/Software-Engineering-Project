from flask import Blueprint, jsonify

from database.tables import Assignment

from . import api

assignment_blueprint = Blueprint("assignment", __name__, url_prefix="/assignment")


# NOTE: get single assignment
@assignment_blueprint.route("/<assignment_id>", methods=["GET"])
def get_assignment(assignment_id):
    assignment = Assignment.objects(id=assignment_id).first()
    if assignment is None:
        return jsonify({"error": "Assignment not found"}), 404
    return assignment.to_json(), 200


api.register_blueprint(assignment_blueprint)
