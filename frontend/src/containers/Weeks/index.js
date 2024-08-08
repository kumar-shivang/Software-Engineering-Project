import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import CourseService from '../../services/Course/index';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faPlay, faFileAlt } from '@fortawesome/free-solid-svg-icons';
import VideoPage from '../../components/VideoPage';
import GradedAssignment from '../../containers/Assignment';
import Chatbot from '../../components/ChatBot/index'

const Weeks = () => {
  const { courseId } = useParams();
  const [data, setData] = useState([]);
  const [isLoadingData, setIsLoadingData] = useState(false);
  const [expandedWeek, setExpandedWeek] = useState(null);
  const [selectedLecture, setSelectedLecture] = useState(null);
  const [selectedAssignment, setSelectedAssignment] = useState(null);

  useEffect(() => {
    getAllWeeksContent();
  }, []);

  const getAllWeeksContent = async () => {
    setIsLoadingData(true);
    const { data } = await CourseService.getAllWeeksContentByCourse(courseId) || {};
    setData(data || []);
    setIsLoadingData(false);
  };

  const handleWeekClick = (week) => {
    if (expandedWeek && expandedWeek.id === week.id) {
      setExpandedWeek(null);
    } else {
      setExpandedWeek(week);
      setSelectedLecture(null);
      setSelectedAssignment(null);
    }
  };

  const handleLectureClick = (lecture) => {
    setSelectedLecture(lecture);
    setSelectedAssignment(null);
  };

  const handleAssignmentClick = (assignment) => {
    setSelectedAssignment(assignment);
    setSelectedLecture(null);
  };

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

  const getWeekLectures = (lectures) => {
      if(lectures?.length === 0){
          return <li >No Lecture Added</li>
      }
      return lectures?.map((lecture) => (
          <li key={lecture.id}>
            <button
              onClick={() => handleLectureClick(lecture)}
              className="text-blue-500 hover:text-blue-700 flex items-center"
            >
             <FontAwesomeIcon icon={faPlay} className="mr-2 text-red-600" />
              {lecture.name}
            </button>
          </li>
        ))
  }

  const getWeeAssignments = (assignments) => {
    if(assignments?.length === 0){
        return <li >No Assignments Added</li>
    }
    return assignments?.map((assignment) => (
            <li key={assignment.id} className="mb-2" >
              <button
                key={assignment.id}
                onClick={() => handleAssignmentClick(assignment)}
                className="text-blue-500 hover:text-blue-700 flex items-center"
              >
                <FontAwesomeIcon icon={faFileAlt} className="mr-2" />
                {assignment.name}
              </button>
          </li>
        ))
   }

  return (
    <div className="min-h-screen bg-gray-100 p-6 flex flex-col lg:flex-row">
      <div className="w-full lg:w-1/4 bg-white p-4 rounded-lg shadow-md mb-6 lg:mb-0">
        <h2 className="text-xl font-semibold mb-4">Weeks</h2>
        <ul className="list-none">
          {data.weeks?.map((week) => (
            <li key={week.id} className="mb-4">
              <button
                onClick={() => handleWeekClick(week)}
                className={`w-full text-left px-4 py-2 rounded-md ${expandedWeek?.id === week.id ? 'bg-blue-500 text-white' : 'bg-gray-200'}`}
              >
                Week {week.number}
              </button>
              {expandedWeek?.id === week.id && (
                <div className="mt-2 ml-4">
                  <h3 className="text-lg font-semibold">Lectures</h3>
                  <ul className="list-none mb-4">
                    {getWeekLectures(week?.lectures)}
                  </ul>
                  <h3 className="text-lg font-semibold">Assignments</h3>
                  <ul className="list-none">
                    {getWeeAssignments(week?.assignments)}
                  </ul>
                </div>
              )}
            </li>
          ))}
        </ul>
      </div>
      <div>
        <Chatbot />
      </div>
      <div className="w-full lg:w-3/4 px-2">
        {selectedLecture && (
          <div>
            <h3 className="text-xl font-semibold mb-2 flex items-center">
              <FontAwesomeIcon icon={faPlay} className="mr-2" />
              {selectedLecture.name}
            </h3>
            <VideoPage src={selectedLecture?.url} />
          </div>
        )}
        {selectedAssignment && (
            <GradedAssignment assignmentId={selectedAssignment?.id} key={selectedAssignment?.id} />
        )}
      </div>
    </div>
  );
};

export default Weeks;
