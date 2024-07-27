from mongoengine import connect
from .tables import Student, Course, Week, Lecture, Question, Assignment, Submission

def init_db():
    connect(db="mydb", host="127.0.0.1", port=27017)
    print("database created")








