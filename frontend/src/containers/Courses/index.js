import React from 'react';
import { useNavigate } from 'react-router-dom';


const weeks = [
  { id : 1, courseId : 1, name: 'Course 1', assignmentScore: 85, quizScore: 90 },
  {id : 2,courseId : 2, name: 'Course 2', assignmentScore: 78, quizScore: 85 },
  { id : 3,courseId : 3,name: 'Course 3', assignmentScore: 92, quizScore: 88 },
];

const Weeks = () => {

    const navigate = useNavigate();

    const handleCardClick = (course) => {
        navigate(`/course/${course?.id}`);
    }

  return (
      <>
        <div className="min-h-screen bg-gray-100 p-6">
        <div className="bg-white p-6 rounded-lg shadow-md">
            <h3 className="text-2xl font-semibold text-gray-800 mb-4">Your Courses</h3>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {weeks.map((course, index) => (
                 <div key={index + 1} className="bg-gray-50 p-4 rounded-lg shadow-md">
                  <h4 className="text-xl font-semibold text-gray-800">Course Title {index+1}</h4>
                  <p className="text-gray-600 mt-2">Brief description of the course content goes here.</p>
                  <button onClick={() => handleCardClick(course)} className="mt-4 bg-blue-500 text-white px-4 py-2 rounded-md hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-300">Continue</button>
                  </div>
            ))}
              
            </div>
         </div>
         </div>
       
    </>)
}

export default Weeks;
