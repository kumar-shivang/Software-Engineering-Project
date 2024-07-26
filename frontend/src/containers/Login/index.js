import React, { useEffect, useState } from 'react';
import LoginService from '../../services/Login';
import { useNavigate } from "react-router-dom";
import { useAuth } from '../../context/AuthContext';
import { toast } from 'react-toastify';

const LoginPage = () => {
  const navigate = useNavigate();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [isLoadingData,setIsLoadingData] = useState(false);

  const { isAuthenticated , login, logout } = useAuth();

  useEffect(() => {
      if(isAuthenticated){
        navigate('/')
      }
  },[isAuthenticated])


  const handleEmailChange = (e) => {
    setEmail(e.target.value);
  };

  const handlePasswordChange = (e) => {
    setPassword(e.target.value);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsLoadingData(true)
    const payload = {
      email,
      password
    }
    try{
      const response = await LoginService.login({ payload });
      console.log("response",response)
      if(response?.data?.access_token){
         login(response.data.access_token);
      }
    }catch(err){
        toast.error(err?.response?.data?.message)
        logout();
    }
     setIsLoadingData(false)
    
  };

  return (
    <div className="flex items-center justify-center h-screen bg-gray-100">
      <div className="bg-white p-8 rounded-lg shadow-lg w-full max-w-md">
        <h2 className="text-2xl font-bold mb-4 text-center">Login</h2>
        <form onSubmit={handleSubmit}>
          <div className="mb-4">
            <label className="block text-gray-700 mb-2" htmlFor="email">Email</label>
            <input 
              type="email" 
              id="email" 
              className="w-full p-2 border border-gray-300 rounded" 
              value={email} 
              onChange={handleEmailChange} 
            />
          </div>
          <div className="mb-6">
            <label className="block text-gray-700 mb-2" htmlFor="password">Password</label>
            <input 
              type="password" 
              id="password" 
              className="w-full p-2 border border-gray-300 rounded" 
              value={password} 
              onChange={handlePasswordChange} 
            />
          </div>
          <button 
            type="submit" 
            className="w-full bg-blue-500 text-white p-2 rounded hover:bg-blue-600 flex items-center justify-center" 
            disabled={isLoadingData}
          >
              {isLoadingData ? (
                <svg className="animate-spin h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"></path>
                </svg>
              ) : (
                'Login'
              )}
          </button>
        </form>
      </div>
    </div>
  );
}

export default LoginPage;
