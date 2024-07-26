import React, { memo, useEffect } from 'react';
import { useAuth } from '../../context/AuthContext';
import { useNavigate } from 'react-router-dom';


const Logout = () => {
    const navigate = useNavigate();

    const { isAuthenticated } = useAuth();

    useEffect(() => {
        
        if(isAuthenticated){
            na
        }else{
            navigate('/')
        }

    },[isAuthenticated])


}

export default memo(Logout);