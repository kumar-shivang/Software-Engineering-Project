from datetime import datetime, timedelta
import logging

from .tables import Course, Lecture, Question, Student, Week, ProgrammingAssignment

logging.info("Generating data")


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
            logging.info(f"Created student {student.name} with id {student.id}")


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
            logging.info(f"Created course {course.name} with id {course.id}")


def generate_enrollments():
    students = Student.objects()
    courses = Course.objects()
    for student in students:
        for course in courses:
            if student not in course.students and course not in student.courses:
                student.enroll(course.id)
        logging.info(f"Enrolled student {student.name} in all courses")


def generate_weeks():
    for course in Course.objects():
        for i in range(1, 11):
            if i not in [week.number for week in course.weeks]:
                course.add_week(i)


def generate_lectures():
    video_link1 = "https://www.youtube.com/watch?v=Kss13U-hvPk"
    video_link2 = "https://youtu.be/PhfbEr2btGQ?si=QzJHMZx_sYeNDJwE"
    transcript1 = """
Despite what you might have thought, math is not just meaningless formulas that popped out of nowhere.
Even though you might not be able to see it, it's everywhere in our universe.
Among the realm of mathematics, there's one particular field described by the Nobel winning physicist Richard Feynman as a language of God.
Calculus, scary huh? Well, it's basically just a description of changes in our ever-changing universe.
Normally when we talk about changes and stuff, we talk about the difference in the amount of stuff after the change.
Well, we can also talk about how fast something changes, the rate of change, how much something changes in a period of time.
To find the rate of change of the height of this bean sprout, we found out how much it has grown within the period of time, dividing the height by the time gives you the rate of change, twelve hundred and fifty meters per second, easy right?
But if you're a good observer, you're probably notice that most things don't change at a constant rate.
So the method I just mentioned doesn't really indicate the variations and the rate of change throughout the entire motion.
Perhaps we can chop the motion up according to its speed, like fast period and slow period. Yeah, but it's perhaps still not precise enough.
How about dividing it into smaller chunks like tracking a change in the distance every second, milliseconds, nanosecond, or even zero seconds.
Wait, what? Nothing and change within zero seconds where time doesn't even pass.
Well, even a powerful subject like math can't change something absurd into something sensible.
What we can do is to record a change within an infinitely small period of time, almost zero seconds but not exactly zero.
We call this small period of time Delta X. As Delta X decreases, you see the rate of change approaching a certain value and from there we can approximate the rate of change at a specific moment.
This process is called differentiation. What's so amazing about calculus is that not only we can use it to find out the instantaneous rate of change but also to do the reverse.
Given how quickly something changes, we can know how much something has changed.
To find out the distance traveled from the speed, we can multiply its speed and a change in time.
But what if the speed is not constant? Well, we can chop its motional into very small periods Delta X and then add all the distances travel within each small period up to get the total change in the distance throughout the entire motion.
As Delta X decreases approaching zero, you can see the total change in distance approaching a certain value.
This process is called integration. You might ask why do we care about calculus.
Apart from nailing exams, well many people do care. Scientists use it to describe the changes in our natural world.
Engineers use to optimize their designs and economists use to optimize problems.
Even if there isn't any point in your life that you have to apply calculus and real life problems, well isn't the ability to see the world in another language pretty amazing."""

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
            "name": "Intro to calculus",
            "video_link": video_link1,
            "transcript": transcript1,
            # "index":1
        },
        {
            "name": "Eigonvalues and eigenvectors",
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
        logging.info(f"Created lectures for course {course.name}")


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


def generate_programming_assignments():
    programming_assignments = [
        {
            "name": "Programming Assignment 1",
            "description": "Print hello world",
        },
        {
            "name": "Programming Assignment 2",
            "description": "Write a function with name `add` to add two numbers",
            "starter_code": """
a = int({})
b = int({})
""",
            "runner_code": """
print(add(a, b))""",
        },
        {
            "name": "Programming Assignment 3",
            "description": "Write a function named `factorial` to find the factorial of a number",
            "starter_code": """
a = int({})
""",
            "runner_code": """
print(factorial(a))""",
        },
    ]
    for course in Course.objects():
        week = Week.objects(course=course.id, number=1).first()
        for pa in programming_assignments:
            if not ProgrammingAssignment.objects(
                week=week.id, description=pa["description"]
            ):
                week.add_programming_assignment(
                    name=pa["name"],
                    description=pa["description"],
                    starter_code=pa.get("starter_code", ""),
                    runner_code=pa.get("runner_code", ""),
                )
        week.save()

    test_cases_p1 = [
        {
            "input": "",
            "output": "Hello, World!",
        }
    ]
    test_cases_p2 = [
        {
            "input": "2\n3",
            "output": "5",
        },
        {
            "input": "5\n7",
            "output": "12",
        },
    ]

    test_cases_p3 = [
        {
            "input": "5",
            "output": "120",
        },
        {
            "input": "3",
            "output": "6",
        },
    ]

    for assignment in ProgrammingAssignment.objects():
        if assignment.name == "Programming Assignment 1":
            for test_case in test_cases_p1:
                if len(assignment.test_cases) < len(test_cases_p1):
                    assignment.add_test_case(
                        input=test_case["input"], output=test_case["output"]
                    )
        elif assignment.name == "Programming Assignment 2":
            for test_case in test_cases_p2:
                if len(assignment.test_cases) < len(test_cases_p2):
                    assignment.add_test_case(
                        input=test_case["input"], output=test_case["output"]
                    )
        elif assignment.name == "Programming Assignment 3":
            if len(assignment.test_cases) < len(test_cases_p3):
                for test_case in test_cases_p3:
                    assignment.add_test_case(
                        input=test_case["input"], output=test_case["output"]
                    )
        assignment.save()


def generate_all():
    generate_students()
    generate_courses()
    generate_enrollments()
    generate_weeks()
    generate_lectures()
    generate_assignments()
    generate_questions()
    generate_programming_assignments()

    print("Data generated successfully")
