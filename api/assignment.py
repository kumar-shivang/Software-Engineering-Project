from flask import Blueprint, request, jsonify

from database.tables import Week, Course, Assignment

from . import api

assignment_blueprint = Blueprint("assignment", __name__, url_prefix="/assignment")

@assignment_blueprint.route("/<week_id>", methods=["GET"])
def get_assignments(week_id):
    week = Week.objects(id=week_id).first()
    assignments = week.assignments
    return jsonify({"assignments": [assignment.to_json() for assignment in assignments]})

@assignment_blueprint.route("/<assignment_id>", methods=["GET"])
def get_assignment(assignment_id):
    assignment = Assignment.objects(id=assignment_id).first()
    return assignment.to_json()

api.register_blueprint(assignment_blueprint)