import React, { useEffect } from 'react'
import { ToastContainer, toast } from 'react-toastify';
import { BrowserRouter as Router, Route,  Routes } from 'react-router-dom';

import Sidebar from './components/Sidebar/index';
import Login from './containers/Login/index';
import LoginPage from './containers/Login';
import Weeks from './containers/Weeks';
import Home from './containers/Home';
import ErrorPage from './containers/ErrorPage/index'
import Course from './containers/Courses/index'
import ProtectedRoute from './components/ProtectedRoute';

import { AuthProvider } from './context/AuthContext';

import './index.css';
import 'react-toastify/dist/ReactToastify.css';


const App = () => {
    return (
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
                </Route>
                <Route path='*' element={<ErrorPage />} />
              </Routes>
          </div>
        </div>
        <ToastContainer />
    </AuthProvider>
    </Router>
    )
}

export default App;