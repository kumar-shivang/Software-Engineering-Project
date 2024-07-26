import React from 'react';
import { Link, useNavigate } from 'react-router-dom';


const weeks = [
  { id : 1, courseId : 1, name: 'Week 1', assignments:[{ id: 1,type:'MCQ' }],  assignmentScore: 85, quizScore: 90 },
  {id : 2,courseId : 2, name: 'Week 2',assignments:[{ id: 1,type:'PROGRAMMING' }], assignmentScore: 78, quizScore: 85 },
  { id : 3,courseId : 3,name: 'Week 3',assignments:[{ id: 1,type:'MCQ'  }], assignmentScore: 92, quizScore: 88 },
];

const Weeks = () => {

  return (
      <>
        <div className="min-h-screen bg-gray-100 p-6">
          <h1 className="text-3xl font-bold mb-6 text-center">Weekly Overview</h1>
          <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
            {weeks.map((week, index) => (
              <div key={index} className="bg-white rounded-lg shadow-lg overflow-hidden">
                <div className="p-6">
                  <h3 className="text-xl font-semibold mb-2 text-gray-800">{week.name}</h3>
                  <div className="space-y-2">
                  
                    <ul className="list-disc list-inside space-y-1">
                    <li >
                    <Link to={`/course/${week?.courseId}/week/${week?.id}`} className="text-blue-500 hover:text-blue-700">
                      View Lectures
                    </Link>
                      </li>
                      {week.assignments.map((assignmentInfo, idx) => (
                        <li key={idx}>
                          {assignmentInfo.type === 'MCQ' ? (
                            <Link to={`/course/${week?.courseId}/week/${week?.id}/mcq/${assignmentInfo?.id}`} className="text-blue-500 hover:text-blue-700">
                              MCQ Assignment
                            </Link>
                          ) : (
                            <Link to={`/course/${week?.courseId}/week/${week?.id}/programming/${assignmentInfo?.id}`} className="text-blue-500 hover:text-blue-700">
                              Programming Assignment
                            </Link>
                          )}
                        </li>
                      ))}
                    </ul>
                  </div>
                </div>
                <div className="bg-gray-100 p-4">
                  <p className="text-gray-600">Assignment Score: {week.assignmentScore}</p>
                  <p className="text-gray-600">Quiz Score: {week.quizScore}</p>
                </div>
              </div>
            ))}
          </div>
      </div>
    </>
  );
}

export default Weeks;
