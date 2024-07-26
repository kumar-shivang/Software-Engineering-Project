import React from 'react';
import { NavLink } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';

const Sidebar = () => {
    const { isAuthenticated, logout } = useAuth();

    return (
        <aside className="w-64 h-full bg-white shadow-md flex flex-col">
            <div className="p-6">
                <h1 className="text-2xl font-semibold text-gray-800">E-Learn</h1>
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
                            <i className="fas fa-home mr-2"></i>Dashboard
                        </NavLink>
                        <NavLink 
                            to="/course" 
                            className={({ isActive }) => 
                                isActive 
                                    ? "block py-2.5 px-4 rounded transition duration-200 bg-blue-500 text-white font-bold" 
                                    : "block py-2.5 px-4 rounded transition duration-200 hover:bg-blue-500 hover:text-white"
                            }
                        >
                            <i className="fas fa-book mr-2"></i>Courses
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
                        <i className="fas fa-sign-in-alt mr-2"></i>Login
                    </NavLink>
                )}
            </nav>
            {isAuthenticated && (
                <button 
                    onClick={logout} 
                    className="m-2 py-2.5 px-4 rounded transition duration-200 bg-red-500 text-white hover:bg-red-600"
                >
                    <i className="fas fa-sign-out-alt mr-2"></i>Logout
                </button>
            )}
        </aside>
    );
}

export default Sidebar;
