from flask import Blueprint,Flask

api = Blueprint("api", __name__, url_prefix="/api")


def init_api(app:Flask)->None:
    from .student import student_blueprint
    from .course import course_blueprint
    from .week import week_blueprint
    from .llm import llm_blueprint
    app.register_blueprint(api)
    # api.register_blueprint(student_blueprint)
    # api.register_blueprint(course_blueprint)
    # api.register_blueprint(llm_blueprint)
    print(app.url_map)

    
