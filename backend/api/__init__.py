from flask import Blueprint, Flask, request, jsonify, g
from bson import ObjectId  
from functools import wraps
from database.tables import  Student

import jwt

SECRET_KEY = 'Secret'
from flask_cors import CORS

api = Blueprint("api", __name__, url_prefix="/api")

def init_api(app: Flask) -> None:
    from .student import student_blueprint
    from .course import course_blueprint
    from .week import week_blueprint
    from .llm import llm_blueprint
    from .assignment import assignment_blueprint
    app.register_blueprint(api)
    app.config['SECRET_KEY'] = SECRET_KEY
    print("\033[92mAPI initialized successfully\033[0m")

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get("x-access-token")
        if not token:
            return jsonify({"error": "Token is missing!"}), 401
        try:
            data = jwt.decode(token,'Secret', algorithms=["HS256"])
            current_user = Student.objects(id=data["student_id"]).first()
            if current_user is None:
                raise ValueError("User not found")
            g.current_user = current_user
        except Exception as e:
            return jsonify({"error": str(e)}), 401
        return f(*args, **kwargs)
    return decorated