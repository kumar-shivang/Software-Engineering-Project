import axiosInstance from '../../config/axiosConfig';
import { toast } from 'react-toastify';

const LoginService = {
    async login({ payload }){
        try{
            let res = await axiosInstance.post('/api/student/login',payload);
            return res?.data || null;
        }catch(err){
            localStorage.removeItem('token')
            toast.error(err?.response?.data?.error || 'Something went wrong!')
        }
    }
}


export default LoginService;