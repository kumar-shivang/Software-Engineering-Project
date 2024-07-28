from flask import Blueprint, Flask

api = Blueprint("api", __name__, url_prefix="/api")


def init_api(app: Flask) -> None:
    from .student import student_blueprint
    from .course import course_blueprint
    from .week import week_blueprint
    from .llm import llm_blueprint
    app.register_blueprint(api)
    print("\033[92mAPI initialized successfully\033[0m")
