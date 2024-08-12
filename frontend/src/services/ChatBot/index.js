import axiosInstance from "../../config/axiosConfig";
import { toast } from "react-toastify";

const ChatBotService = {
  async talkToBot({input,sessionId}) {
    try {
      let res = await axiosInstance.post("/api/help/chat", {message:input,session_id:sessionId});
      return res?.data || null;
    } catch (err) {
      toast.error(err?.response?.data?.error);
    }
  },
};

export default ChatBotService;
