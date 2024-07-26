import React from 'react';

const GradedAssignment = () => {
    return (
        <div className="min-h-screen bg-gray-100 p-6">
            <div className="bg-white shadow-md rounded-lg p-6">
                <h1 className="text-2xl font-bold mb-4">Graded Assignment</h1>

                <div className="mb-6">
                    <p className="text-red-500 font-semibold">The due date for submitting this assignment has passed.</p>
                    <p className="text-gray-700">Due on <span className="font-medium">2024-06-16, 23:59 IST</span>.</p>
                    <p className="text-gray-700">You may submit any number of times before the due date. The final submission will be considered for grading.</p>
                    <p className="text-gray-700">You have last submitted on: <span className="font-medium">2024-06-16, 20:18 IST</span></p>
                </div>

                <div className="mb-6">
                    <p className="text-xl font-semibold mb-2">1 point</p>
                    <p className="text-gray-800 mb-4">What do you recall from the lecture? An intelligent agent in AI settings is __________ .</p>
                    <ul className="list-disc list-inside mb-4">
                        <li>Persistent</li>
                        <li>Autonomous</li>
                        <li>Proactive</li>
                        <li>Goal Directed</li>
                    </ul>
                    <p className="text-green-600 font-semibold">Yes, the answer is correct.</p>
                    <p className="text-gray-700">Score: <span className="font-medium">1</span></p>
                    <p className="text-gray-700">Accepted Answers:</p>
                    <ul className="list-disc list-inside">
                        <li>Persistent</li>
                        <li>Autonomous</li>
                        <li>Proactive</li>
                        <li>Goal Directed</li>
                    </ul>
                </div>

                <div>
                    <p className="text-xl font-semibold mb-2">1 point</p>
                    <p className="text-gray-800 mb-4">What do you recall about self-aware agents discussed in the lecture? A self-aware agent __________ .</p>
                    <ul className="list-disc list-inside mb-4">
                        <li>is conscious of the meaning of life in this cosmos</li>
                        <li>has a model of the world</li>
                        <li>models itself in the model of the world</li>
                        <li>is conscious of its purpose in life in this cosmos</li>
                    </ul>
                    <p className="text-green-600 font-semibold">Yes, the answer is correct.</p>
                    <p className="text-gray-700">Score: <span className="font-medium">1</span></p>
                    <p className="text-gray-700">Accepted Answers:</p>
                    <ul className="list-disc list-inside">
                        <li>has a model of the world</li>
                        <li>models itself in the model of the world</li>
                    </ul>
                </div>
            </div>

            <button className="fixed bottom-5 right-10 bg-blue-500 text-white p-3 rounded-md shadow-md hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-300 focus:ring-opacity-75">
        Submit
    </button>
        </div>
    );
};

export default GradedAssignment;
