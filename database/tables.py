from datetime import datetime
from mongoengine import Document, DateTimeField, StringField, IntField, ListField, DictField, BooleanField, ReferenceField

"""
    +---------------+               +---------------+
    |   Student     |               |    Course     |
    +---------------+               +---------------+
    | id            |               | id            |
    | name          |<------------->| name          |
    | email         |               | weeks         |
 +--| password      |               | students      |
 |  | courses       |               |               |
 |  | grades        |               +---------------+
 |  | submissions   |                     |
 |                                        |
 |  +---------------+                     |
 |                                        v
 |  +---------------+               +---------------+
 |  |  Lecture      |               |     Week      |
 |  +---------------+               +---------------+
 |  | id            |               | id            |
 |  | name          |               | number        |
 |  | week          |               | course        |
 |  | index         |               | assignments   |
 |  | week          |<------------->| lectures      |
 |  | url           |               +---------------+
 |  | transcript    |                        ^          
 |  +---------------+                        |           
 |                                           |               
 |                                           v            
 |  +---------------+               +---------------+
 |  |   Submission  |               |  Assignment   |
 |  +---------------+               +---------------+
 |  |  student      |               | id            |
 +->|  assignment   |<------------->| name          |
    |  answers      |               | week          |
    |  grade        |               | graded        |
    +---------------+               | questions     |
                                    | submissions   |
                                    +---------------+
                                           |
                                           |
                                           v
                                   +---------------+
                                   |   Question    |
                                   +---------------+
                                   | id            |
                                   | question      |
                                   | qtype         |
                                   | answers       |
                                   | correct_answer|
                                   | assignment    |
                                   +---------------+

                                """


class Student(Document):
    """
    Represents a student in the system.

    Attributes:
        id (int): The unique identifier for the student.
        name (str): The name of the student.
        email (str): The email address of the student.
        password (str): The password for the student's account.
        courses (List[Course]): The list of courses the student is enrolled in.
        grades (List[Dict[int, float]]): The list of grades for the student's assignments.
        submissions (List[Submission]): The list of submissions made by the student.

    Methods:
        enroll(course_id) -> None:
            Enrolls the student in a course with the given course_id.

        submit(assignment_id, answers: List[str]) -> None:
            Submits answers for an assignment with the given assignment_id.

    """
    name = StringField(required=True)
    email = StringField(required=True, unique=True)
    password = StringField(required=True)
    courses = ListField(ReferenceField("Course"))
    grades = ListField(DictField())  # {assignment_id: grade}
    submissions = ListField(ReferenceField("Submission")) #


    def enroll(self, course_id:str) -> None:
        """
        Enrolls the student in a course with the given course_id.

        Args:
            course_id (str) : The ID of the course to enroll in.
        Raises:
            ValueError: If the course with the given course_id is not found.
        """
        course = Course.objects(id=course_id).first()
        if course is None:
            raise ValueError("Course not found")
        if self in course.students and course in self.courses:
            raise ValueError("Student already enrolled in the course")
        else:
            course.students.append(self)
            self.courses.append(course)
            print(f"{self.name} successfully enrolled in {course.name}")
        self.save()
        course.save()

    def submit(self, assignment_id:str, answers: dict) -> None:
        """
        Submits answers for an assignment with the given assignment_id.

        Args:
            assignment_id (str): The ID of the assignment to submit.
            answers (List[str]): The list of answers for the assignment.

        Raises:
            ValueError: If the assignment with the given assignment_id is not found or if the student is not enrolled in the course.
        """
        # check if the assignment exists
        assignment = Assignment.objects(id=assignment_id).first()
        if assignment is None:  # if no assignment found
            raise ValueError("Assignment not found")
        elif (
            self not in assignment.course.students
        ):  # if student is not enrolled in the course
            raise ValueError("Student not enrolled in the course")

        submission = Submission(
            student=self,
            assignment=assignment.id,
            answers=answers,
        )
        submission.save()
        submission.grade_submission()
        self.submissions.append(submission)
        if assignment_id not in self.grades:
            self.grades.append({assignment_id: submission.grade})
        elif self.grades[assignment_id] < submission.grade:
            self.grades[assignment_id] = submission.grade
        self.save()


    


class Course(Document):
    """
    Represents a course in the database.
    """

    name = StringField(required=True)
    weeks = ListField(ReferenceField("Week"))
    students = ListField(ReferenceField(Student))

    def add_week(self, week_no: int):
        """
        Adds a new week to the course.

        Args:
            week_no (int): The week number.

        Returns:
            Week: The newly created Week object.
        """
        if week_no > 12:
            raise ValueError("Week number cannot be greater than 12")
        elif week_no in [week.number for week in self.weeks]:
            raise ValueError("Week already exists")
        week = Week(number=week_no, course=self)
        week.save()
        self.weeks.append(week)
        self.save()
        return week


class Week(Document):
    """
    Represents a week in the course.

    Methods:
        add_assignment(assignment_name: str, due_date: datetime) -> Assignment:
            Adds a new assignment to the week.

        add_lecture(lecture_name: str, url: str, transcript: str = None) -> Lecture:
            Adds a new lecture to the week.

        get_grades() -> List[Dict[str, float]]:
            Get the grades for all students in the week


    """

    number = IntField(required=True)
    course = ReferenceField(Course,required=True)
    assignments = ListField(ReferenceField("Assignment"))
    lectures = ListField(ReferenceField("Lecture"))


    def add_assignment(self, name: str, due_date: datetime,graded:bool) -> "Assignment":
        """
        Adds a new assignment to the week.

        Args:
            assignment_name (str): The name of the assignment.
            due_date (datetime): The due date of the assignment.
        
        Returns:
            Assignment: The newly created Assignment object.
        """
        assignment = Assignment(
            name=name,
            due_date=due_date,
            graded=graded,
            week=self,
        )
        assignment.save()
        self.assignments.append(assignment)
        self.save()
        return assignment

    def add_lecture(self, lecture_name: str, url: str, transcript: str = None):
        """
        Adds a new lecture to the week.

        Args:
            lecture_name (str): The name of the lecture.
            url (str): The URL of the lecture.
            transcript (str): The transcript of the lecture (optional).
            index (int): The index of the lecture in the week.

        Returns:
            Lecture: The newly created Lecture object.
            """
        lecture = Lecture(
            name=lecture_name,
            week=self,
            index=len(self.lectures) + 1,
            url=url,
            transcript=transcript,
        )
        lecture.save()
        self.lectures.append(lecture)
        self.save()
        return lecture



class Assignment(Document):
    """
    Represents an assignment in the system.

    Attributes:
        id (int): The unique identifier for the assignment.
        name (str): The name of the assignment.
        due_date (datetime): The due date of the assignment.
        course (Course): The course the assignment belongs to.
        graded (bool): A flag indicating if the assignment has been graded.
        questions (List[Question]): The list of questions in the assignment.
        submissions (List[Submission]): The list of submissions for the assignment.
        week (Week): The week the assignment belongs to.

    Methods:
        add_question(question: str, qtype: str, answers: List[str], correct_answer: str) -> Question:
            Adds a new question to The assignment.



    """

    name = StringField(required=True)
    due_date = DateTimeField(required=False)
    graded = BooleanField(default=False)
    questions = ListField(ReferenceField("Question"))
    week = ReferenceField(Week)
    course = ReferenceField(Course)
    
    def add_question(
        self, question: str, qtype: str, answers: list, correct_answer: str
    )-> "Question":
        """
        Adds a new question to the assignment.

        Args:
            question (str): The question text.
            qtype (str): The type of question (e.g., multiple_choice, short_answer, range, fill_in_the_blank).
            answers (List[str]): The list of possible answers.
            correct_answer (str): The correct answer to the question.

        Returns:
            Question: The newly created Question object.
        """
        question = Question(
            question=question,
            qtype=qtype,
            answers=answers,
            correct_answer=correct_answer,
            assignment=self
        )
        question.save()
        self.questions.append(question)
        self.save()
        return question


class Submission(Document):
    """
    Represents a submission made by a student for an assignment.

    Attributes:
        id (int): The unique identifier for the submission.
        student (Student): The student who made the submission.
        assignment (Assignment): The assignment the submission is for.
        answers (List[str]): The list of answers provided by the student.
        grade (Dict[str, float]): The grade for the submission.

    Methods:
        grade_submission() -> Dict[str, float]:
            Grades the submission and returns the grade.

        get_result() -> List[Dict[str, Any]]:
            Returns the result of the submission as a list of dictionaries containing the question, answer, and correctness.

    """

    student = ReferenceField(Student)
    assignment = ReferenceField(Assignment)
    answers = ListField(DictField())
    grade = DictField()

    def grade_submission(self):
        """
        Grades the submission and returns the grade.

        Returns:
            Dict[str, float]: The grade for the submission.

        """
        assignment = self.assignment
        questions = assignment.questions
        grade = 0
        for i in range(len(questions)):
            question = questions[i]
            answer = self.answers[i]
            if question.check_answer(answer):
                grade += 1
        self.grade = {"grade": grade, "total": len(questions)}
        self.save()
        return self.grade

    def get_result(self): # 
        """
        Get the result of the submission.

        Returns:
            List[Dict[str, Any]]: A list of dictionaries containing the question, answer, and correctness.
        """
        assignment = self.assignment
        questions = assignment.questions
        result = []
        for i in range(len(questions)):
            question_id = questions[i].id
            question = questions[i]
            answer = self.answers[i]
            correct = question.check_answer(answer)
            result.append(
                {
                    "question_id": question_id,
                    "question": question.question,
                    "answer": answer,
                    "correct": correct,
                }
            )
        return result


class Question(Document):
    """
    Represents a question in the system.

    Attributes:
        id (int): The unique identifier for the question.
        question (str): The text of the question.
        qtype (str): The type of question (e.g., multiple_choice, short_answer, range, fill_in_the_blank).
        answers (List[str]): The list of possible answers.
        correct_answer (str): The correct answer to the question.
        assignment (Assignment): The assignment the question belongs to.
        graded (bool): A flag indicating if the question is for practice or graded.
        grades (List[Dict[str, Any]]): The list of grades for the question.
    """
    question = StringField(required=True)
    qtype = StringField(required=True)
    answers = ListField(StringField())
    correct_answer = ListField(StringField())
    assignment = ReferenceField(Assignment)
    graded = BooleanField(default=False)
    grades = ListField(DictField())

    def check_answer(self, answer: str) -> bool:
        """
        Checks if the given answer is correct.

        Args:
            answer (str): The answer to check.

        """
        if self.qtype == "multiple_choice":
            return answer == self.correct_answer[0]
        elif self.qtype == "range":
            # when the answer is a range of numbers first and second element of the answer list represent the minimum and maximum values respectively
            maximum = float(self.answers[1])
            minimum = float(self.answers[0])
            answer = float(answer)
            return minimum <= answer <= maximum
        elif self.qtype == "fill_in_the_blank":
            return answer in self.answers
        elif self.qtype == "multiple_answers":
            return set(answer) == set(self.correct_answer)
        else:
            return False


class Lecture(Document):

    name = StringField(required=True)
    week = ReferenceField(Week)
    index = IntField(required=True)
    url = StringField(required=True)
    transcript = StringField()
