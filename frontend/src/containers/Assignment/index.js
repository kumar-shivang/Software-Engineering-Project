import React, { useEffect, useState } from "react";
import AssignmentService from "../../services/Assignment/index";
import { toast } from "react-toastify";
import ChatBotService from "../../services/ChatBot";
import { LockClosedIcon } from "@heroicons/react/solid"; // Using Heroicons for the lock icon

const Assignment = ({ assignmentId }) => {
  const [answers, setAnswers] = useState({});
  const [assignmentData, setAssignmentData] = useState(null);
  const [isLoadingData, setIsLoadingData] = useState(false);
  const [result, setResult] = useState(null);
  const [feedback, setFeedback] = useState(null);
  const [submissionId, setSubmissionId] = useState(null);

  const currentDate = new Date();

  useEffect(() => {
    fetchAssignments();
  }, []);

  const fetchAssignments = async () => {
    setIsLoadingData(true);
    try {
      const { data } =
        (await AssignmentService.getAssignmetsById(assignmentId)) || {};
      setAssignmentData(data);
    } catch (error) {
      toast.error("Failed to load assignment data");
    } finally {
      setIsLoadingData(false);
    }
  };

  const isPastDueDate = () => {
    if (!assignmentData?.dueDate) return false;
    return new Date(assignmentData.dueDate) < currentDate;
  };

  const handleChange = (questionId, answer) => {
    setAnswers({
      ...answers,
      [questionId]: Array.isArray(answer) ? answer : [answer],
    });
  };

  const handleSubmit = async () => {
    if (
      !answers ||
      Object.keys(answers).length !== assignmentData?.questions?.length
    ) {
      toast.error("Please answer all questions");
      return;
    }

    const payload = { answers };
    setIsLoadingData(true);
    setResult(null);
    setAnswers({});
    try {
      const response = await AssignmentService.submitAssignment(
        assignmentId,
        payload
      );
      if (response) {
        toast.success("Assignment Submitted successfully");
        setSubmissionId(response.data.submission_id);
        const res = await AssignmentService.getResult(
          response.data.submission_id
        );
        let resultMap = {};
        res?.data?.forEach((resultInfo) => {
          resultMap[resultInfo?.id] = resultInfo;
        });
        setResult(resultMap);
      }
    } catch (error) {
      toast.error("Failed to submit assignment");
    }
    setIsLoadingData(false);
  };

  const getFeedback = async () => {
    if (!submissionId || isLoadingData) return;
    setIsLoadingData(true);
    try {
      const { data } = (await ChatBotService.getFeedback(submissionId)) || {};
      console.log(data);
      let feedbackMap = {};
      Object.keys(data)?.forEach((feedbackId) => {
        feedbackMap[feedbackId] = data[feedbackId];
      });

      console.log(feedbackMap);

      setFeedback(feedbackMap);
      setIsLoadingData(false);
    } catch (error) {
      toast.error("Failed to load feedback");
      setIsLoadingData(false);
    }
  };

  const getResult = (questionId) => {
    if (!result || isLoadingData) return;
    if (result[questionId]?.correct === 1) {
      return (
        <p className="text-green-600 mt-2">
          Correct answer: {result?.[questionId]?.answer?.join(", ")}
        </p>
      );
    }
    return (
      <>
        <p className="text-red-600 mt-2">
          Incorrect Answer: {result?.[questionId]?.answer?.join(", ")}
        </p>
      </>
    );
  };

  const getFeedbackContent = (questionId) => {
    if (!feedback || isLoadingData) return;
    return <p className="text-purple-600 mt-2">{feedback[questionId]}</p>;
  };

  if (isLoadingData) {
    return (
      <div className="flex flex-col justify-center items-center min-h-screen">
        <svg
          className="animate-spin h-8 w-8 text-blue-500 mb-4"
          xmlns="http://www.w3.org/2000/svg"
          fill="none"
          viewBox="0 0 24 24"
        >
          <circle
            className="opacity-25"
            cx="12"
            cy="12"
            r="10"
            stroke="currentColor"
            strokeWidth="4"
          ></circle>
          <path
            className="opacity-75"
            fill="currentColor"
            d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"
          ></path>
        </svg>
        <p className="text-gray-700">Loading assignment data...</p>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-100 py-8 px-4 sm:px-6 lg:px-8">
      <div className="bg-white shadow-lg rounded-lg p-6 max-w-3xl mx-auto">
        <div className="mb-6 flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-bold text-gray-900">
              {assignmentData?.name}
            </h1>
            {assignmentData?.dueDate && (
              <p
                className={`mt-2 ${
                  isPastDueDate() ? "text-red-600" : "text-gray-700"
                }`}
              >
                Due Date: {new Date(assignmentData?.dueDate).toString()}
              </p>
            )}
          </div>
          {isPastDueDate() && (
            <div className="flex items-center space-x-2">
              <LockClosedIcon className="h-8 w-8 text-red-500" />
              <p className="text-red-500 font-semibold">Submission Closed</p>
            </div>
          )}
        </div>
        {assignmentData?.questions.map((question, index) => (
          <div key={question.id} className="mb-8">
            <div className="flex justify-between items-center mb-4">
              <p className="text-gray-800 text-lg">{question.question}</p>
              <p className="text-sm font-semibold text-gray-600">
                {index + 1} point
              </p>
            </div>
            {question.type === "multiple_choice" && (
              <ul className="list-none">
                {question.answers.map((answer, i) => (
                  <li key={i} className="mb-2">
                    <label className="flex items-center">
                      <input
                        type="radio"
                        name={question.id}
                        value={answer}
                        onChange={() => handleChange(question.id, answer)}
                        className="mr-3 text-indigo-600 focus:ring-indigo-500"
                        disabled={isPastDueDate()}
                      />
                      <span className="text-gray-700">{answer}</span>
                    </label>
                  </li>
                ))}
                {getResult(question.id)}
                {getFeedbackContent(question.id)}
              </ul>
            )}
            {question.type === "multiple_answers" && (
              <ul className="list-none">
                {question.answers.map((answer, i) => (
                  <li key={i} className="mb-2">
                    <label className="flex items-center">
                      <input
                        type="checkbox"
                        name={`${question.id}-${i}`}
                        value={answer}
                        onChange={(e) =>
                          handleChange(
                            question.id,
                            e.target.checked
                              ? [...(answers[question.id] || []), answer]
                              : answers[question.id].filter((a) => a !== answer)
                          )
                        }
                        className="mr-3 text-indigo-600 focus:ring-indigo-500"
                        disabled={isPastDueDate()} // Disable input if the result is available or due date has passed
                      />
                      <span className="text-gray-700">{answer}</span>
                    </label>
                  </li>
                ))}
                {getResult(question.id)}
                {getFeedbackContent(question.id)}
              </ul>
            )}
            {question.type === "range" && (
              <>
                <input
                  type="number"
                  min="0"
                  max="10"
                  onChange={(e) => handleChange(question.id, e.target.value)}
                  className="w-full p-2 border rounded mt-2"
                  disabled={isPastDueDate()} // Disable input if the result is available or due date has passed
                />
                {getResult(question.id)}
                {getFeedbackContent(question.id)}
              </>
            )}
          </div>
        ))}

        <div className="flex justify-end mt-8">
          <button
            className={`bg-blue-500 text-white px-6 py-2 rounded-md shadow-md focus:outline-none focus:ring-2 focus:ring-blue-300 focus:ring-opacity-75 ${
              isPastDueDate()
                ? "opacity-40 cursor-not-allowed"
                : "hover:bg-blue-600"
            }`}
            onClick={handleSubmit}
            disabled={isPastDueDate()} // Disable button if the result is available or due date has passed
          >
            Submit
          </button>
          {submissionId && !isPastDueDate() && (
            <button
              className="ml-4 bg-green-500 text-white px-6 py-2 rounded-md shadow-md hover:bg-green-600 focus:outline-none focus:ring-2 focus:ring-green-300 focus:ring-opacity-75"
              onClick={getFeedback}
            >
              Get Feedback
            </button>
          )}
        </div>
      </div>
    </div>
  );
};

export default Assignment;
