from werkzeug.security import generate_password_hash, check_password_hash
from . import db

class Admin(db.Model):
    __tablename__ = 'admins'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    email = db.Column(db.String(50))
    password_hash = db.Column(db.String(128))

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')
    
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return '<Admin %r>' % self.name


class Student(db.Model):
    __tablename__ = 'students'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    email = db.Column(db.String(50))
    password_hash = db.Column(db.String(255))
    # courses = db.relationship('Course', secondary='enrollments', backref=db.backref('students', lazy='dynamic'))


    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')
    
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return '<Student %r>' % self.name
    

class Course(db.Model):
    __tablename__ = 'courses'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    description = db.Column(db.String(255))
    students = db.relationship('Student', secondary='enrollments', backref=db.backref('courses', lazy='dynamic'))

    def __init__(self,name,description):
        self.name = name
        self.description = description

    def __repr__(self):
        return '<Course %r>' % self.name


# Association table for many-to-many relationship between Student and Course

enrollments = db.Table('enrollments',
    db.Column('student_id', db.Integer, db.ForeignKey('students.id')),
    db.Column('course_id', db.Integer, db.ForeignKey('courses.id'))
)


class Week(db.Model):
    __tablename__ = 'weeks'
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.Integer)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'))
    course = db.relationship('Course', backref=db.backref('weeks', lazy='dynamic'))

    
    def __init__(self,number,course_id):
        self.number = number
        self.course_id = course_id

    def __repr__(self):
        return '<Week %r>' % self.number
    

    

class Lecture(db.Model):
    __tablename__ = 'lectures'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50))
    video_url = db.Column(db.String(255))
    week_id = db.Column(db.Integer, db.ForeignKey('weeks.id'))
    index = db.Column(db.Integer)
    week = db.relationship('Week', backref=db.backref('lectures', lazy='dynamic'))
    
    def __init__(self,title,video_url,week_id,index):
        self.title = title
        self.video_url = video_url
        self.week_id = week_id
        self.index = index

    def __repr__(self):
        return '<Lecture %r>' % self
    

    


class Assignment(db.Model):
    __tablename__ = 'assignments'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50))
    description = db.Column(db.String(255))
    due_date = db.Column(db.DateTime)
    graded = db.Column(db.Boolean)
    week_id = db.Column(db.Integer, db.ForeignKey('weeks.id'))
    week = db.relationship('Week', backref=db.backref('assignments', lazy='dynamic'))

    def __init__(self,title,description,due_date,graded,week_id):
        self.title = title
        self.description = description
        self.due_date = due_date
        self.graded = graded
        self.week_id = week_id
    
    def __repr__(self):
        return '<Assignment %r>' % self.title
    

class Question(db.Model):
    __tablename__ = 'questions'
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(255))
    assignment_id = db.Column(db.Integer, db.ForeignKey('assignments.id'))
    assignment = db.relationship('Assignment', backref=db.backref('questions', lazy='dynamic'))

    def __init__(self,question,type,assignment_id):
        self.question = question
        self.assignment_id = assignment_id
    
    def __repr__(self):
        return '<Question %r>' % self.question

class MultipleChoiceQuestion(Question):
    __tablename__ = 'multiple_choice_questions'
    id = db.Column(db.Integer, db.ForeignKey('questions.id'), primary_key=True)
    correct_answer = db.Column(db.Integer, db.ForeignKey('answers.id'))
    answers = db.relationship('Answer', backref=db.backref('multiple_choice_question', lazy='dynamic'))

    def __init__(self,question,type,assignment_id,correct_answer):
        super().__init__(question,type,assignment_id)
        self.correct_answer = correct_answer

    def __repr__(self):
        return '<MultipleChoiceQuestion %r>' % self.id

class TrueFalseQuestion(Question):
    __tablename__ = 'true_false_questions'
    id = db.Column(db.Integer, db.ForeignKey('questions.id'), primary_key=True)
    correct_answer = db.Column(db.Boolean)

    def __init__(self,question,type,assignment_id,correct_answer):
        super().__init__(question,type,assignment_id)
        self.correct_answer = correct_answer

    def __repr__(self):
        return '<TrueFalseQuestion %r>' % self.id


class NumericQuestion(Question):
    __tablename__ = 'numeric_questions'
    id = db.Column(db.Integer, db.ForeignKey('questions.id'), primary_key=True)
    correct_answer = db.Column(db.Float)

    def __init__(self,question,type,assignment_id,correct_answer):
        super().__init__(question,type,assignment_id)
        self.correct_answer = correct_answer

    def __repr__(self):
        return '<NumericQuestion %r>' % self.id

    

class Answer(db.Model):
    __tablename__ = 'answers'
    id = db.Column(db.Integer, primary_key=True)
    answer = db.Column(db.String(255))

    def __init__(self,answer,question_id):
        self.answer = answer
        self.question_id = question_id
    
    def __repr__(self):
        return '<Answer %r>' % self
    

class Submission(db.Model):
    __tablename__ = 'submissions'
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'))
    assignment_id = db.Column(db.Integer, db.ForeignKey('assignments.id'))
    submitted = db.Column(db.DateTime)
    graded = db.Column(db.Boolean)
    grade = db.Column(db.Float)
    student = db.relationship('Student', backref=db.backref('submissions', lazy='dynamic'))
    assignment = db.relationship('Assignment', backref=db.backref('submissions', lazy='dynamic'))

    def __init__(self,student_id,assignment_id,submitted,graded,grade):
        self.student_id = student_id
        self.assignment_id = assignment_id
        self.submitted = submitted
        self.graded = graded
        self.grade = grade
    
    def __repr__(self):
        return '<Submission %r>' % self.id
    



    


