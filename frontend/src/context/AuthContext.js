import React, { createContext, useContext, useState } from 'react';
import { useNavigate } from 'react-router-dom';

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const navigate = useNavigate();
  const [isAuthenticated, setIsAuthenticated] = useState(localStorage.getItem('access_token'));

  const login = (access_token) => {
      localStorage.setItem('access_token',access_token)
      setIsAuthenticated(true);
      navigate('/')
  }
  const logout = () => {
      localStorage.removeItem('access_token')
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
