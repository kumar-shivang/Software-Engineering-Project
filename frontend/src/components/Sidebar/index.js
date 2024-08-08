import React, { useState } from 'react';
import { NavLink } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';

const Sidebar = () => {
    const [isCollapsed, setIsCollapsed] = useState(false);
    const { isAuthenticated, logout } = useAuth();

    const toggleSidebar = () => {
        setIsCollapsed(!isCollapsed);
    };

    return (
        <aside className={`${isCollapsed ? 'w-20' : 'w-64'} h-full bg-white shadow-md flex flex-col transition-width duration-300`}>
            <div className="p-6 flex items-center justify-between">
                <h1 className={`text-2xl font-semibold text-gray-800 ${isCollapsed ? 'hidden' : 'block'}`}>E-Learn</h1>
                <button onClick={toggleSidebar} className="text-gray-600 focus:outline-none">
                    <i className={`fas ${isCollapsed ? 'fa-chevron-right' : 'fa-chevron-left'} text-lg`}></i>
                </button>
            </div>
            <nav className="m-2 space-y-1 flex-grow">
                {isAuthenticated ? (
                    <>
                        <NavLink 
                            to="/" 
                            className={({ isActive }) => 
                                isActive 
                                    ? "block py-2.5 px-4 rounded transition duration-200 bg-blue-500 text-white font-bold" 
                                    : "block py-2.5 px-4 rounded transition duration-200 hover:bg-blue-500 hover:text-white"
                            }
                        >
                            <i className="fas fa-home mr-2"></i>
                            <span className={`${isCollapsed ? 'hidden' : 'inline'}`}>Dashboard</span>
                        </NavLink>
                        <NavLink 
                            to="/course" 
                            className={({ isActive }) => 
                                isActive 
                                    ? "block py-2.5 px-4 rounded transition duration-200 bg-blue-500 text-white font-bold" 
                                    : "block py-2.5 px-4 rounded transition duration-200 hover:bg-blue-500 hover:text-white"
                            }
                        >
                            <i className="fas fa-book mr-2"></i>
                            <span className={`${isCollapsed ? 'hidden' : 'inline'}`}>Courses</span>
                        </NavLink>
                    </>
                ) : (
                    <NavLink 
                        to="/login" 
                        className={({ isActive }) => 
                            isActive 
                                ? "block py-2.5 px-4 rounded transition duration-200 bg-blue-500 text-white font-bold" 
                                : "block py-2.5 px-4 rounded transition duration-200 hover:bg-blue-500 hover:text-white"
                        }
                    >
                        <i className="fas fa-sign-in-alt mr-2"></i>
                        <span className={`${isCollapsed ? 'hidden' : 'inline'}`}>Login</span>
                    </NavLink>
                )}
            </nav>
            {isAuthenticated && (
                <button 
                    onClick={logout} 
                    className="m-2 py-2.5 px-4 rounded transition duration-200 bg-red-500 text-white hover:bg-red-600"
                >
                    <i className="fas fa-sign-out-alt mr-2"></i>
                    <span className={`${isCollapsed ? 'hidden' : 'inline'}`}>Logout</span>
                </button>
            )}
        </aside>
    );
}

export default Sidebar;
