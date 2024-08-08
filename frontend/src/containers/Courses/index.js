import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import CourseService from '../../services/Course/index';
import { toast } from 'react-toastify';

const Courses = () => {
  const navigate = useNavigate();
  const [allCourses, setAllCourses] = useState([]);
  const [isLoadingData, setIsLoadingData] = useState(false);
  const [searchTerm, setSearchTerm] = useState('');

  useEffect(() => {
    getAllCourses();
  }, []);

  const getAllCourses = async () => {
    setIsLoadingData(true);
    const { data } = await CourseService.getAllCourses() || {};
    setAllCourses(data || []);
    setIsLoadingData(false);
  };

  const handleCardClick = (course) => {
    navigate(`/course/${course?._id}`);
  };

  const handleSearchChange = (e) => {
    setSearchTerm(e.target.value);
  };

  const filteredCourses = allCourses.filter(course =>
    course.name.toLowerCase().includes(searchTerm.toLowerCase())
  );

  if (isLoadingData) {
    return (
      <div className="flex justify-center items-center min-h-screen">
        <svg className="animate-spin h-8 w-8 text-blue-500" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
          <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
          <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"></path>
        </svg>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-100 p-6">
      <div className="bg-white p-6 rounded-lg shadow-md">
        <h3 className="text-2xl font-semibold text-gray-800 mb-4">My Courses</h3>
        <input
          type="text"
          placeholder="Search courses..."
          value={searchTerm}
          onChange={handleSearchChange}
          className="mb-4 p-2 border border-gray-300 rounded-md w-full"
        />
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {filteredCourses.map((course) => (
            <div key={course._id} className="bg-gray-50 p-4 rounded-lg shadow-md flex flex-col justify-between">
              <div>
                <h4 className="text-xl font-semibold text-gray-800">{course.name}</h4>
                <p className="text-gray-600 mt-2">{course.description}</p>
                <p className="text-gray-500 mt-2">Duration: {course?.weeks?.length} weeks</p>
              </div>
              <button
                onClick={() => handleCardClick(course)}
                className="mt-4 bg-blue-500 text-white px-4 py-2 rounded-md hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-300"
              >
                Continue
              </button>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default Courses;
