import axios from 'axios';

const LoginService = {
    login({ payload }){
        return axios.post('/login',payload);
    }
}


export default LoginService;