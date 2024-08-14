import axiosInstance from "../../config/axiosConfig";
import { toast } from "react-toastify";

const ChatBotService = {
  async talkToBot({ input, sessionId }) {
    try {
      let res = await axiosInstance.post("/api/help/chat", {
        message: input,
        session_id: sessionId,
      });
      return res?.data || null;
    } catch (err) {
      toast.error(err?.response?.data?.error || 'Something went wrong!');
    }
  },
  async getFeedback(submissionId) {
    try {
      let res = await axiosInstance.post(
        '/api/help/feedback',
        { submission_id :submissionId },
        {
          headers: {
            "x-access-token": localStorage.getItem("token"),
          },
        }
      );
      return res?.data || null;
    } catch (err) {
      toast.error(err?.response?.data?.error || 'Something went wrong!');
    }
  },
  async getProgrammingFeedback(submissionId) {
    try {
      let res = await axiosInstance.post(
        '/api/help/explain',
        { submission_id :submissionId },
        {
          headers: {
            "x-access-token": localStorage.getItem("token"),
          },
        }
      );
      return res?.data || null;
    } catch (err) {
      toast.error(err?.response?.data?.error || 'Something went wrong!');
    }
  },
};

export default ChatBotService;
