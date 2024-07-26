import React from 'react';
import ReactDOM from 'react-dom/client';
import { ToastContainer, toast } from 'react-toastify';
import { BrowserRouter as Router, Route,  Routes } from 'react-router-dom';

import Sidebar from './components/Sidebar/index';
import Login from './containers/Login/index';
import LoginPage from './containers/Login';
import Weeks from './containers/Weeks';
import Home from './containers/Home';
import WeekModule from './containers/WeekModule';
import GradedAssignment from './containers/GradedAssignment';
import ProgrammingAssignment from './containers/ProgrammingAssignment';
import ErrorPage from './containers/ErrorPage/index'
import Course from './containers/Courses/index'
import ProtectedRoute from './components/ProtectedRoute';

import { AuthProvider } from './context/AuthContext';

import './index.css';
import 'react-toastify/dist/ReactToastify.css';

const root = ReactDOM.createRoot(document.getElementById('root'));

root.render(
  <React.StrictMode>
     <Router>
    <AuthProvider>
        <div className="flex h-screen">
          <div className="h-full">
            <Sidebar />
          </div>
          <div className="flex-1 overflow-y-auto">
              <Routes>
                <Route path="/login" element={<LoginPage />} />
                <Route element={<ProtectedRoute />}>
                  <Route path="/" element={<Home />} />
                  <Route path="/course" element={<Course />}  />
                  <Route path="/course/:courseId" element={<Weeks />}   />
                  <Route path="/course/:courseId/week/:weekId" element={<WeekModule />}   />
                  <Route path="/course/:courseId/week/:weekId/mcq/:assignmentId" element={<GradedAssignment />}   />
                  <Route path="/course/:courseId/week/:weekId/programming/:assignmentId" element={<ProgrammingAssignment />}   />
                </Route>
                <Route path='*' element={<ErrorPage />} />
              </Routes>
          </div>
        </div>
        <ToastContainer />
    </AuthProvider>
    </Router>
  </React.StrictMode>
);

