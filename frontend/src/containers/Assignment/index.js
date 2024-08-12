import React, { useEffect, useState } from 'react';
import AssignmentService from '../../services/Assignment/index';
import { toast } from 'react-toastify';

const Assignment = ({ assignmentId }) => {
    const [questions, setQuestions] = useState([]);
    const [answers, setAnswers] = useState({});
    const [data, setData] = useState(null);
    const [isLoadingData, setIsLoadingData] = useState(false);
    const [result, setResult] = useState(null);
    const [submissionId, setSubmissionId] = useState(null);

    useEffect(() => {
        fetchAssignments();
    }, []);

    const fetchAssignments = async () => {
        setIsLoadingData(true);
        const data = await AssignmentService.getAssignmetsById(assignmentId);
        setData(data?.data);
        setQuestions(data?.data?.questions || []);
        setIsLoadingData(false);
    };

    const handleChange = (questionId, answer) => {
        setAnswers({
            ...answers,
            [questionId]: Array.isArray(answer) ? answer : [answer],
        });
    };

    const handleSubmit = async () => {
        const response = await AssignmentService.submitAssignment(assignmentId, { answers });
        if (response) {
            toast.success("Assignment Submitted successfully");
            setSubmissionId(response.data.submission_id); // Assuming the API returns a submissionId
            const res = await AssignmentService.getResult(response.data.submission_id); // Assuming this is the API call to get the results
                console.log(res)
                setResult(res.data); // Assuming the response contains the result data in response.data

        }
    };

    const getFeedback = async () => {
        // if (!submissionId) return;

    };

    if (isLoadingData) {
        return (
            <div className="flex justify-center items-center">
                <svg className="animate-spin h-8 w-8 text-blue-500" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"></path>
                </svg>
            </div>
        );
    }

    return (
        <div className="min-h-screen bg-gray-100">
            <div className="bg-white shadow-md rounded-lg p-6">
                <div className="mb-4">
                    <h1 className="text-2xl font-bold mb-1">{data?.name}</h1>
                    {data?.dueDate ? <p className="text-red-500">Due Date: {new Date(data?.dueDate).toString()}</p> : null}
                </div>
                {questions.map((question, index) => (
                    <div key={question.id} className="mb-6">
                        <div className="flex justify-between items-center mb-2">
                            <p className="text-gray-800">{question.question}</p>
                            <p className="text-s font-semibold">{index + 1} point</p>
                        </div>
                        {question.type === 'multiple_choice' && (
                            <ul className="list-none mb-4">
                                {question.answers.map((answer, i) => (
                                    <li key={i} className="mb-2">
                                        <label className={`flex items-center ${result && result[question.id]?.correct ? 'text-green-500' : 'text-red-500'}`}>
                                            <input
                                                type="radio"
                                                name={question.id}
                                                value={answer}
                                                onChange={() => handleChange(question.id, answer)}
                                                className="mr-2"
                                                disabled={!!result} // Disable input if the result is available
                                            />
                                            {answer}
                                        </label>
                                        {result && !result[question.id]?.correct && (
                                            <p className="text-red-500">Incorrect answer</p>
                                        )}
                                    </li>
                                ))}
                            </ul>
                        )}
                        {question.type === 'multiple_answers' && (
                            <ul className="list-none mb-4">
                                {question.answers.map((answer, i) => (
                                    <li key={i} className="mb-2">
                                        <label className={`flex items-center ${result && result[question.id]?.correct ? 'text-green-500' : 'text-red-500'}`}>
                                            <input
                                                type="checkbox"
                                                name={`${question.id}-${i}`}
                                                value={answer}
                                                onChange={(e) => handleChange(question.id, e.target.checked ? [...(answers[question.id] || []), answer] : answers[question.id].filter(a => a !== answer))}
                                                className="mr-2"
                                                disabled={!!result} // Disable input if the result is available
                                            />
                                            {answer}
                                        </label>
                                        {result && !result[question.id]?.correct && (
                                            <p className="text-red-500">Incorrect answer</p>
                                        )}
                                    </li>
                                ))}
                            </ul>
                        )}
                        {question.type === 'range' && (
                            <input
                                type="number"
                                min="0"
                                max="10"
                                onChange={(e) => handleChange(question.id, e.target.value)}
                                className={`w-full p-2 border rounded ${result && result[question.id]?.correct ? 'border-green-500' : 'border-red-500'}`}
                                disabled={!!result} // Disable input if the result is available
                            />
                        )}
                    </div>
                ))}

                <button
                    className="right-10 bg-blue-500 text-white px-4 py-2 rounded-md shadow-md hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-300 focus:ring-opacity-75"
                    onClick={handleSubmit}
                    disabled={!!result} // Disable button if the result is available
                >
                    Submit
                </button>
                {submissionId && (
                    <button
                        className="ml-4 bg-green-500 text-white px-4 py-2 rounded-md shadow-md hover:bg-green-600 focus:outline-none focus:ring-2 focus:ring-green-300 focus:ring-opacity-75"
                        onClick={getFeedback}
                    >
                        Get Feedback
                    </button>
                )}
            </div>
        </div>
    );
};

export default Assignment;
