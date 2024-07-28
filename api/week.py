from flask import Blueprint, jsonify

from database.tables import Week, Course

from . import api

week_blueprint = Blueprint("week", __name__, url_prefix="/week")


# @week_blueprint.route("/<course_id>", methods=["GET"])
# def get_weeks(course_id):
#     course = Course.objects(id=course_id).first()
#     weeks = course.weeks
#     return jsonify({"weeks": [week.to_json() for week in weeks]})


# NOTE: get single week
@week_blueprint.route("/<week_id>", methods=["GET"])
def get_week(week_id):
    week = Week.objects(id=week_id).first()
    if week is None:
        return jsonify({"error": "Week not found"}), 404
    return week.to_json()


api.register_blueprint(week_blueprint)
