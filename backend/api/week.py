from flask import Blueprint, jsonify
from database.tables import Week
from . import api
from api.utils.serializer import serialize_doc

week_blueprint = Blueprint("week", __name__, url_prefix="/week")

# NOTE: get single week
@week_blueprint.route("/<week_id>", methods=["GET"])
def get_week(week_id):
    courses = Course.objects()
    if not courses:
        return jsonify({"data": [], "message": "No courses found"}), 200
    courses_list = [serialize_doc(course) for course in courses]
    return jsonify({ "data": courses_list }), 200

    week = Week.objects(id=week_id).first()
    if week is None:
        return jsonify({"error": "Week not found"}), 404
    return week.to_json()


@week_blueprint.route("/assignments/<week_id>", methods=["GET"])
def get_assignments(week_id):
    week = Week.objects(id=week_id).first()
    if week is None:
        return jsonify({"error": "Week not found"}), 404
    assignments = week.assignments
    return (
        jsonify({"assignments": [assignment.to_json() for assignment in assignments]}),
        200,
    )


@week_blueprint.route("/lectures/<week_id>", methods=["GET"])
def get_lectures(week_id):
    week = Week.objects(id=week_id).first()
    if week is None:
        return jsonify({"error": "Week not found"}), 404
    lectures = week.lectures
    return (
        jsonify({"lectures": [lecture.to_json() for lecture in lectures]}),
        200,
    )


api.register_blueprint(week_blueprint)
