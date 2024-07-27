from flask import Flask, request, jsonify
from models import db
from models.tables import Student
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token
from sqlalchemy.exc import SQLAlchemyError

app = Flask(__name__)
CORS(app, origins="*")

DATABASE_URL = 'sqlite:///test.sqlite'
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'your_jwt_secret_key'
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

db.init_app(app)

def add_dummy_data():
    try:
        students = [
            Student(name='Admin', email="admin@gmail.com", password_hash=bcrypt.generate_password_hash("123")),
        ]
        db.session.add_all(students)
        db.session.commit()
        print("Dummy Students added.")
    except SQLAlchemyError as e:
        print(f"An error occurred: {e}")

with app.app_context():
    db.create_all()
    add_dummy_data()
    print("Database created!")

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    
    if not email or not password:
        return jsonify({'message': 'Email and password are required'}), 400
    
    user = Student.query.filter_by(email=email).first()
    print(user)
    print(user.email)
    print(user.password_hash)
    print(bcrypt.check_password_hash(user.password_hash, password))
    if user and bcrypt.check_password_hash(user.password_hash, password):
        access_token = create_access_token(identity={'email': user.email})
        return jsonify({'access_token': access_token}), 200
    else:
        return jsonify({'message': 'Invalid credentials'}), 401

if __name__ == '__main__':
    app.run(port=5000, debug=True)
