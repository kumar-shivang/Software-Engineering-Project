import React, { memo, useState, useEffect, useCallback } from "react";
import { toast } from "react-toastify";
import AssignmentService from "../../services/Assignment";
import ChatBotService from "../../services/ChatBot";
import AceEditor from "react-ace";
import "ace-builds/src-noconflict/mode-javascript";
import "ace-builds/src-noconflict/mode-python";
import "ace-builds/src-noconflict/theme-github";
import "ace-builds/src-noconflict/ext-language_tools";

const LoadingSpinner = () => (
  <div className="flex justify-center items-center">
    <svg
      className="animate-spin h-8 w-8 text-blue-500"
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
  </div>
);

const ProgrammingAssignment = ({ assignmentId }) => {
  const [loading, setLoading] = useState(false);
  const [assignmentData, setAssignmentData] = useState(null);
  const [testResults, setTestResults] = useState(null);
  const [feedback, setFeedback] = useState(null);
  const [submissionId, setSubmissionId] = useState(null);
  const [code, setCode] = useState("");

  useEffect(() => {
    fetchAssignment();
  }, [assignmentId]);

  const fetchAssignment = async () => {
    try {
      setLoading(true);
      const { data } = await AssignmentService.getPrograamingAssignmetById(assignmentId);
      setAssignmentData(data);
    } catch (error) {
      toast.error("Failed to load assignment data");
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = useCallback(async () => {
    if (!code) {
      toast.error("Please enter code for the programming assignment");
      return;
    }

    try {
      setSubmissionId(null);
      setTestResults(null);
      const response = await AssignmentService.submitProgrammingAssignment(assignmentId, code);
      if (response) {
        toast.success("Programming Assignment Submitted successfully");
        setTestResults(response.data.test_results || []);
        setSubmissionId(response.data.submission_id);
      }
    } catch (error) {
      toast.error("Submission failed");
    }
  }, [assignmentId, code]);

  const handleGetFeedback = useCallback(async () => {
    if (!submissionId || loading) return;

    try {
      const data = await ChatBotService.getProgrammingFeedback(submissionId);
      setFeedback(data || null);
    } catch (error) {
      toast.error("Failed to retrieve feedback");
    }
  }, [submissionId, loading]);

  if (loading) return <LoadingSpinner />;

  return (
    <div className="flex flex-col lg:flex-row lg:space-x-4 p-4">
      <div className="lg:w-1/3">
        {assignmentData && (
          <>
            <h2 className="text-3xl font-bold mb-4">{assignmentData.name}</h2>
            <p className="font-bold mb-2">Task :</p>
            <p className="mb-4">{assignmentData.description}</p>
            {testResults && testResults[0] && (
              <div className="mt-3">
                <p className={`${testResults[0].match ? 'text-green-500' : 'text-red-500'}`}>
                  Output: {testResults[0].output}
                </p>
                {!testResults[0].match && (
                  <p className="text-blue-500">Expected Output: {testResults[0].expected_output}</p>
                )}
              </div>
            )}
            {testResults && (
              <button
                className="mt-4 w-full bg-green-500 text-white px-4 py-2 rounded-md shadow-md hover:bg-green-600 focus:outline-none focus:ring-2 focus:ring-green-300 focus:ring-opacity-75"
                onClick={handleGetFeedback}
              >
                Get Feedback
              </button>
            )}
            {feedback && <p className="text-blue-500 mt-4">{feedback}</p>}
          </>
        )}
      </div>

      <div className="lg:w-2/3 mt-6 lg:mt-0">
        <AceEditor
          mode={assignmentData?.language || 'python'}
          theme="github"
          onChange={(newValue) => setCode(newValue)}
          name="aceCodeEditor"
          editorProps={{ $blockScrolling: true }}
          setOptions={{
            enableBasicAutocompletion: true,
            enableLiveAutocompletion: true,
            enableSnippets: true,
          }}
          width="100%"
          height="500px"
        />
          <button
            onClick={handleSubmit}
            className="bg-blue-500 mt-5 px-4 py-2 w-full text-white rounded-md shadow-md hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-300 focus:ring-opacity-75"
          >
            Submit Assignment
          </button>
      </div>
    </div>
  );
};

export default memo(ProgrammingAssignment);
