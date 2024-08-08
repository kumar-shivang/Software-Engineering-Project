import React, { createContext, useContext, useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const navigate = useNavigate();
  const [isAuthenticated, setIsAuthenticated] = useState(localStorage.getItem('token'));

  const login = (access_token) => {
      localStorage.setItem('token',access_token)
      setIsAuthenticated(true);
      navigate('/')
  }
  const logout = () => {
      localStorage.removeItem('token')
      setIsAuthenticated(false);
      navigate('/login')
  }

  return (
    <AuthContext.Provider value={{ isAuthenticated, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const context = useContext(AuthContext);
  return context;
}
