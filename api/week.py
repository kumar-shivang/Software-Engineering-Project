from flask import Blueprint, request, jsonify

from database.tables import Week, Course

from . import api

week_blueprint = Blueprint("week", __name__, url_prefix="/week")

@week_blueprint.route("/<course_id>", methods=["GET"])
def get_weeks(course_id):
    course = Course.objects(id=course_id).first()
    weeks = course.weeks
    return jsonify({"weeks": [week.to_json() for week in weeks]})

@week_blueprint.route("/<week_id>", methods=["GET"])
def get_week(week_id):
    week = Week.objects(id=week_id).first()
    return week.to_json()








api.register_blueprint(week_blueprint)