from datetime import datetime
import io
import sys

from mongoengine import (
    BooleanField,
    DateTimeField,
    DictField,
    Document,
    IntField,
    ListField,
    ReferenceField,
    StringField,
)


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
    grades = DictField()  # {assignment_id: grade}
    submissions = ListField(ReferenceField("Submission"))
    programming_submissions = ListField(ReferenceField("ProgrammingSubmission"))

    def enroll(self, course_id: str) -> None:
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
        self.save()
        course.save()

    def submit(self, assignment_id: str, answers: dict) -> None:
        """
        Submits answers for an assignment with the given assignment_id.

        Args:
            assignment_id (str): The ID of the assignment to submit.
            answers (List[str]): The list of answers for the assignment.

        Raises: ValueError: If the assignment with the given assignment_id is not found or if the student is not
        enrolled in the course.
        """
        # check if the assignment exists
        assignment = Assignment.objects(id=assignment_id).first()
        if assignment is None:  # if no assignment found
            raise ValueError("Assignment not found")
        elif (
            self not in assignment.week.course.students
        ):  # if student is not enrolled in the course
            raise ValueError("Student not enrolled in the course")
        # print(answers)

        submission = Submission(
            student=self,
            assignment=assignment.id,
            answers=answers,
        )
        submission.save()
        submission.grade_submission()
        self.submissions.append(submission)
        assignment_id = str(assignment_id)
        if assignment_id not in self.grades.keys():
            self.grades[assignment_id] = submission.get_total_grade()
        elif self.grades[assignment_id] < submission.get_total_grade():
            self.grades[assignment_id] = submission.get_total_grade()
        self.save()
        return submission.id

    def submit_programming_assignment(self, assignment_id: str, code: str) -> None:
        """
        Submits a programming assignment with the given assignment_id.

        Args:
            assignment_id (str): The ID of the programming assignment to submit.
            code (str): The code to submit.

        Raises: ValueError: If the assignment with the given assignment_id is not found or if the student is not
        enrolled in the course.
        """
        # check if the assignment exists
        assignment = ProgrammingAssignment.objects(id=assignment_id).first()
        if assignment is None:
            raise ValueError("Programming Assignment not found")
        elif self not in assignment.week.course.students:
            raise ValueError("Student not enrolled in the course")

        submission = ProgrammingSubmission(
            student=self, assignment=assignment, code=code
        )
        submission.save()
        submission.grade_submission()
        self.programming_submissions.append(submission)
        assignment_id = str(assignment_id)
        if assignment_id not in self.grades.keys():
            self.grades[assignment_id] = submission.get_total_grade()
        elif self.grades[assignment_id] < submission.get_total_grade():
            self.grades[assignment_id] = submission.get_total_grade()
        self.save()
        return submission

    def get_score(self, assignment_id: str):
        """
        Get the score for the assignment with the given assignment_id.

        Args:
            assignment_id (str): The ID of the assignment to get the score for.

        Returns:
            float: The score for the assignment.
        """
        return self.grades[str(assignment_id)]


class Course(Document):
    """
    Represents a course in the database.
    """

    name = StringField(required=True)
    description = StringField(required=True)
    weeks = ListField(ReferenceField("Week"))  # [week1,week2....]
    students = ListField(ReferenceField(Student))  # [student1,student2]

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
    course = ReferenceField(Course, required=True)
    assignments = ListField(ReferenceField("Assignment"))
    lectures = ListField(ReferenceField("Lecture"))
    programming_assignments = ListField(ReferenceField("ProgrammingAssignment"))

    def add_assignment(
        self, name: str, due_date: datetime, graded: bool
    ) -> "Assignment":
        """
        Adds a new assignment to the week.

        Args:
            name (str): The name of the assignment.
            due_date (datetime): The due date of the assignment.


        Returns:
            Assignment: The newly created Assignment object.
            :param due_date:
            :param name:
            :param graded:
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

    def add_programming_assignment(
        self, name, description, starter_code="", runner_code=""
    ) -> None:
        """
        Adds a new programming assignment to the week.

        Args:
            name (str): The name of the programming assignment.
            description (str): The description of the programming assignment.
            starter_code (str): The starter code for the programming assignment.
        """
        programming_assignment = ProgrammingAssignment(
            name=name,
            description=description,
            week=self,
            starter_code=starter_code,
            runner_code=runner_code,
        )
        programming_assignment.save()
        self.programming_assignments.append(programming_assignment)

        self.save()


class Assignment(Document):
    """
    Represents an assignment in the system.

    Attributes:
        name (str): The name of the assignment.
        due_date (datetime): The due date of the assignment.
        course (Course): The course the assignment belongs to.
        graded (bool): A flag indicating if the assignment has been graded.
        questions (List[Question]): The list of questions in the assignment.
        week (Week): The week the assignment belongs to.

    Methods:
        add_question(question: str, qtype: str, answers: List[str], correct_answer: str) -> Question:
            Adds a new question to The assignment.



    """

    name = StringField(required=True)
    due_date = DateTimeField(required=False)
    graded = BooleanField(default=False)
    questions = ListField(ReferenceField("Question"))  # [question1,question2....]
    week = ReferenceField(Week)  # week...
    course = ReferenceField(Course)

    def add_question(
        self, question: str, qtype: str, answers: list, correct_answer: str
    ) -> "Question":
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
            assignment=self,
        )
        question.save()
        self.questions.append(question)
        self.save()
        return question


class Submission(Document):
    """
    Represents a submission made by a student for an assignment.

    Attributes:
        student (Student): The student who made the submission.
        assignment (Assignment): The assignment the submission is for.
        answers (List[str]): The list of answers provided by the student.
        result (Dict[str, Any]): The result of the submission.

    Methods:
        grade_submission() -> Dict[str, float]:
            Grades the submission and returns the grade.

        get_result() -> List[Dict[str, Any]]: Returns the result of the submission as a list of dictionaries
        containing the question, answer, and correctness.

    """

    student = ReferenceField(Student)
    assignment = ReferenceField(Assignment)
    answers = DictField()  # {question_id:[answer]}
    result = DictField()  # {question_id:0,1}

    def grade_submission(self):
        """
        Grades the submission and returns the grade.

        Returns:
            Dict[str, float]: The grade for the submission.

        """
        for question_id, answer in self.answers.items():
            question = Question.objects(id=question_id).first()
            if question is None:
                raise ValueError("Question not found")
            if question.check_answer(answer):
                self.result[question_id] = 1
            else:
                self.result[question_id] = 0
        self.save()
        return self.result

    def get_total_grade(self):
        return sum(self.result.values())

    def get_result(self):
        result = []
        print(self.answers)
        for question_id, answer in self.answers.items():
            print(question_id)
            question = Question.objects(id=question_id).first()
            if question is None:
                raise ValueError("Question not found")
            result.append(
                {
                    "id": question_id,
                    "question": question.question,
                    "answer": answer,
                    "correct": self.result[question_id],
                }
            )
        return result


class Question(Document):
    """
    Represents a question in the system.

    Attributes:
        question (str): The text of the question.
        qtype (str): The type of question (e.g., multiple_choice, short_answer, range, fill_in_the_blank).
        answers (List[str]): The list of possible answers.
        correct_answer (str): The correct answer to the question.
        assignment (Assignment): The assignment the question belongs to.
        graded (bool): A flag indicating if the question is for practice or graded.
    """

    question = StringField(required=True)
    qtype = StringField(required=True)
    answers = ListField(StringField())  # ['animal','machine'....]
    correct_answer = ListField(StringField())  # ["animal"],[2,3,4]
    assignment = ReferenceField(Assignment)
    graded = BooleanField(default=False)

    def check_answer(self, answer: list) -> bool:
        """
        Checks if the given answer is correct.

        Args:
            answer (str): The answer to check.

        """
        if self.qtype == "multiple_choice":
            return answer == self.correct_answer
        elif self.qtype == "range":
            # when the answer is a range of numbers first and second element of the answer list represent the minimum
            # and maximum values respectively
            maximum = float(self.correct_answer[1])
            minimum = float(self.correct_answer[0])
            answer = float(answer[0])
            return minimum <= answer <= maximum
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


class ProgrammingAssignment(Document):
    """
    Represents a programming assignment in the system.

    Attributes:
        language (str): The programming language for the assignment.
        starter_code (str): The starter code for the assignment.
        test_cases (List[str]): The list of test cases for the assignment.

    """

    name = StringField(required=True)
    description = StringField(required=True)
    language = StringField(default="python")
    starter_code = StringField(required=False)
    runner_code = StringField(required=False)
    test_cases = ListField(DictField())  # {'input': 'output'}
    week = ReferenceField(Week)
    due_date = DateTimeField(required=False)
    graded = BooleanField(default=False)

    def add_test_case(self, input: str, output: str):
        d = {input: output}
        self.test_cases.append(d)
        self.save()


class ProgrammingSubmission(Document):
    """
    Represents a programming submission made by a student for a programming assignment.

    Attributes:
        code (str): The code submitted by the student.
        test_results (List[Dict[str, Any]]): The results of running the test cases on the code.

    Methods:
        grade_submission() -> Dict[str, float]:
            Grades the submission and returns the grade.

        get_test_results() -> List[Dict[str, Any]]:
            Returns the results of running the test cases on the code.

    """

    code = StringField(required=True)
    test_results = ListField(DictField())  # [{test_case: result}]
    student = ReferenceField(Student)
    assignment = ReferenceField(ProgrammingAssignment)

    @staticmethod
    def run_code(code):
        """
        Runs the code with preset variables and returns the result.

        Args:
            code (str): The code to run.
            preset_vars (dict, optional): Preset variables to be available during code execution.

        Returns:
            Dict[str, Any]: The result of running the code.
        """

        old_stdout = sys.stdout
        new_stdout = io.StringIO()
        sys.stdout = new_stdout
        try:
            exec(code, {})
        except Exception as e:
            result = {"error": str(e)}
        else:
            result = {"output": new_stdout.getvalue()}

        # Restore stdout
        sys.stdout = old_stdout

        return result

    def grade_submission(self):
        """
        Grades the submission and returns the grade.

        Returns:
            Dict[str, float]: The grade for the submission.
        """

        total_tests = len(self.assignment.test_cases)
        passed_tests = 0

        for test_case in self.assignment.test_cases:

            input_val, expected_output = list(test_case.items())[0]
            if "\n" in input_val:
                input_val = input_val.split("\n")

            if self.assignment.starter_code:
                code = (
                    self.assignment.starter_code.format(*input_val) + "\n" + self.code
                )
            else:
                code = self.code
            if self.assignment.runner_code:
                code += "\n" + self.assignment.runner_code

            result = self.run_code(code)
            if result.get("error"):
                self.test_results.append(
                    {
                        "input": input_val,
                        "output": result.get("error"),
                        "expected_output": expected_output,
                        "match": False,
                    }
                )
                continue
            if result.get("output").strip() == expected_output:
                passed_tests += 1

            self.test_results.append(
                {
                    "input": input_val,
                    "output": result.get("output"),
                    "expected_output": expected_output,
                    "match": result.get("output").strip() == expected_output,
                }
            )

        grade = (passed_tests / total_tests) * 100
        return {"grade": grade, "test_results": self.test_results}

    def get_total_grade(self):
        return sum([result["match"] for result in self.test_results])
