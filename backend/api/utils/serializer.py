from bson import ObjectId


def serialize_doc(doc):
    doc_dict = doc.to_mongo().to_dict()
    for key, value in doc_dict.items():
        if isinstance(value, ObjectId):
            doc_dict[key] = str(value)  # Convert ObjectId to string
        elif isinstance(value, dict):
            doc_dict[key] = serialize_doc(
                value
            )  # Recursive call for nested dictionaries
        elif isinstance(value, list):
            doc_dict[key] = [
                (
                    serialize_doc(v)
                    if isinstance(v, dict)
                    else str(v) if isinstance(v, ObjectId) else v
                )
                for v in value
            ]  # Handle lists
    return doc_dict


def serialize_assignment(assignment):
    return {
        "id": str(assignment.id),
        "name": assignment.name,
        "due_date": assignment.due_date.isoformat() if assignment.due_date else None,
        "graded": assignment.graded,
        "questions": [
            serialize_question(question) for question in assignment.questions
        ],
    }


def serialize_question(question):
    if question.qtype == "multiple_choice":
        return {
            "id": str(question.id),
            "question": question.question,
            "type": "multiple_choice",
            "correct_answer": question.correct_answer,
            "answers": question.answers,
        }
    elif question.qtype == "true_false":
        return {
            "id": str(question.id),
            "question": question.question,
            "type": "true_false",
            "correct_answer": question.correct_answer,
        }
    elif question.qtype == "numeric":
        return {
            "id": str(question.id),
            "question": question.question,
            "type": "numeric",
            "correct_answer": question.correct_answer,
        }
    elif question.qtype == "range":
        return {
            "id": str(question.id),
            "question": question.question,
            "type": "range",
            "correct_answer": question.correct_answer,
        }
    elif question.qtype == "multiple_answers":
        return {
            "id": str(question.id),
            "question": question.question,
            "type": "multiple_answers",
            "correct_answer": question.correct_answer,
            "answers": question.answers,
        }
    else:
        return {
            "id": str(question.id),
            "question": question.question,
            "type": "unknown",
        }


def serialize_answer(answer):
    return {"id": str(answer.id), "answer": answer.answer}


def serialize_submission(submission):
    return {
        "student_id": str(submission.student.id),
        "assignment_id": str(submission.assignment.id),
        "answers": submission.answers,
        "result": submission.result,
        "total_grade": submission.get_total_grade(),
    }


def serialize_course(course):
    return {
        "id": str(course.id),
        "name": course.name,
        "description": course.description,
        "weeks": [serialize_week(week) for week in course.weeks],
    }


def serialize_week(week):
    return {
        "id": str(week.id),
        "number": week.number,
        "lectures": [serialize_lecture(lecture) for lecture in week.lectures],
        "assignments": [
            serialize_assignment(assignment) for assignment in week.assignments
        ],
    }


def serialize_lecture(lecture):
    return {
        "id": str(lecture.id),
        "name": lecture.name,
        "url": lecture.url,
        "index": lecture.index,
    }

