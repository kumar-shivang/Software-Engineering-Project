from datetime import datetime, timedelta

from .tables import Course, Lecture, Question, Student, Week

def generate_students():
    students = [
        {"name": "Alice", "email": "alice@email.com", "password": "password123"},
        {"name": "Bob", "email": "bob@email.com", "password": "password123"},
        {"name": "Charlie", "email": "charlie@email.com", "password": "password123"},
    ]
    for student in students:
        if not Student.objects(email=student["email"]):
            student = Student(
                name=student["name"],
                email=student["email"],
                password=student["password"],
            )
            student.save()


def generate_courses():
    courses = [
        {
            "name": "Math",
            "description": "Math is the study of numbers, shapes, and patterns.",
        },
        {
            "name": "Science",
            "description": "Science is the study of the natural world.",
        },
        {
            "name": "History",
            "description": "History is the study of the past.",
        },
    ]
    for course in courses:
        if not Course.objects(name=course["name"]):
            course = Course(name=course["name"], description=course["description"])
            course.save()


def generate_enrollments():
    students = Student.objects()
    courses = Course.objects()
    for student in students:
        for course in courses:
            if student not in course.students and course not in student.courses:
                student.enroll(course.id)


def generate_weeks():
    for course in Course.objects():
        for i in range(1, 11):
            if i not in [week.number for week in course.weeks]:
                course.add_week(i)


def generate_lectures():
    video_link1 = "https://www.youtube.com/watch?v=020g-0hhCAU"
    video_link2 = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    transcript1 = """
Baby Shark, doo-doo, doo-doo, doo-doo
Baby Shark, doo-doo, doo-doo, doo-doo
Baby Shark, doo-doo, doo-doo, doo-doo
Baby Shark
Mommy Shark, doo-doo, doo-doo, doo-doo
Mommy Shark, doo-doo, doo-doo, doo-doo
Mommy Shark, doo-doo, doo-doo, doo-doo
Mommy Shark
Daddy Shark, doo-doo, doo-doo, doo-doo
Daddy Shark, doo-doo, doo-doo, doo-doo
Daddy Shark, doo-doo, doo-doo, doo-doo
Daddy Shark
Grandma Shark, doo-doo, doo-doo, doo-doo
Grandma Shark, doo-doo, doo-doo, doo-doo
Grandma Shark, doo-doo, doo-doo, doo-doo
Grandma Shark
Grandpa Shark, doo-doo, doo-doo, doo-doo
Grandpa Shark, doo-doo, doo-doo, doo-doo
Grandpa Shark, doo-doo, doo-doo, doo-doo
Grandpa Shark
Let's go hunt, doo-doo, doo-doo, doo-doo
Let's go hunt, doo-doo, doo-doo, doo-doo
Let's go hunt, doo-doo, doo-doo, doo-doo
Let's go hunt
Run away, doo-doo, doo-doo, doo-doo
Run away, doo-doo, doo-doo, doo-doo
Run away, doo-doo, doo-doo, doo-doo
Run away (ah!)
Safe at last, doo-doo, doo-doo, doo-doo
Safe at last, doo-doo, doo-doo, doo-doo
Safe at last, doo-doo, doo-doo, doo-doo
Safe at last (phew)
It's the end, doo-doo, doo-doo, doo-doo
It's the end, doo-doo, doo-doo, doo-doo
It's the end, doo-doo, doo-doo, doo-doo
It's the end"""

    transcript2 = """
We're no strangers to love
You know the rules and so do I
A full commitment's what I'm thinking of
You wouldn't get this from any other guy
I just wanna tell you how I'm feeling
Gotta make you understand
Never gonna give you up
Never gonna let you down
Never gonna run around and desert you

Never gonna make you cry
Never gonna say goodbye
Never gonna tell a lie and hurt you
We've known each other for so long
Your heart's been aching but you're too shy to say it
Inside we both know what's been going on
We know the game and we're gonna play it
And if you ask me how I'm feeling
Don't tell me you're too blind to see
Never gonna give you up
Never gonna let you down
Never gonna run around and desert you
Never gonna make you cry
Never gonna say goodbye
"""
    data = [
        {
            "name": "Baby Shark",
            "video_link": video_link1,
            "transcript": transcript1,
            # "index":1
        },
        {
            "name": "Never Gonna Give You Up",
            "video_link": video_link2,
            # "index":2
            "transcript": transcript2,
        },
    ]
    for course in Course.objects():
        week_number = 1
        # where course.id is the course id and week is the week number
        week = Week.objects(course=course.id, number=week_number).first()
        for lecture in data:
            if not Lecture.objects(week=week.id, name=lecture["name"]):
                week.add_lecture(
                    lecture_name=lecture["name"],
                    url=lecture["video_link"],
                    transcript=lecture["transcript"],
                )
        week.save()


def generate_assignments():
    week_number = 1
    assignments = [
        {
            "name": "Practice Assignment 1",
            "graded": 0,
            "due_date": None,
        },
        {
            "name": "Graded Assignment 1",
            "graded": 1,
            "due_date": datetime.now() + timedelta(days=7),
        },
    ]
    for course in Course.objects():
        week = Week.objects(course=course.id, number=week_number).first()
        for assignment in assignments:
            if assignment["name"] not in {
                _assignment.name for _assignment in week.assignments
            }:
                week.add_assignment(
                    name=assignment["name"],
                    graded=assignment["graded"],
                    due_date=assignment["due_date"],
                )
        week.save()


def generate_questions():
    data = [
        {
            "question": "What is 2+2?",
            "answers": ["4", "5", "6", "7"],
            "correct_answer": ["4"],
            "qtype": "multiple_choice",
        },
        {
            "question": "What is square root of 4?",
            "answers": ["-2", "2", "5", "15"],
            "correct_answer": ["2", "-2"],
            "qtype": "multiple_answers",
        },
        {
            "question": "What is sqrt(2)?",
            "answers": [],
            "correct_answer": ["1.41", "1.42"],
            "qtype": "range",
        },
    ]

    for course in Course.objects():
        week = Week.objects(course=course.id, number=1).first()
        for question in data:
            for assignment in week.assignments:
                if not Question.objects(
                    assignment=assignment.id, question=question["question"]
                ):
                    assignment.add_question(
                        question=question["question"],
                        answers=question["answers"],
                        correct_answer=question["correct_answer"],
                        qtype=question["qtype"],
                    )

        week.save()


def generate_all():
    generate_students()
    generate_courses()
    generate_enrollments()
    generate_weeks()
    generate_lectures()
    generate_assignments()
    generate_questions()
