import axiosInstance from '../../config/axiosConfig';
import { toast } from 'react-toastify';

const ChatBotService = {
    async talkToBot(message){
        try{
            let res = await axiosInstance.get('/api/chatbot/',{ message});
            return res?.data || null;
        }catch(err){
            toast.error(err?.response?.data?.error)
        }
    },
}


export default ChatBotService;