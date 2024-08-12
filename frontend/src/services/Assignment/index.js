import axiosInstance from "../../config/axiosConfig";
import { toast } from "react-toastify";

const AssignmentService = {
  async getAssignmetsById(assignmentId) {
    try {
      let res = await axiosInstance.get(`/api/assignment/${assignmentId}`, {
        headers: {
          "x-access-token": localStorage.getItem("token"),
        },
      });
      return res?.data || null;
    } catch (err) {
      toast.error(err?.response?.data?.error);
    }
  },
  async getResult(submissionId) {
    try {
      let res = await axiosInstance.get(
        `/api/student/get_result/${submissionId}`,
        {
          headers: {
            "x-access-token": localStorage.getItem("token"),
          },
        }
      );
      return res?.data || null;
    } catch (err) {
      toast.error(err?.response?.data?.error);
    }
  },
  async submitAssignment(assignmentId, payload) {
    try {
      let res = await axiosInstance.post(
        `/api/student/submit`,
        { ...payload, assignment_id: assignmentId },
        {
          headers: {
            "x-access-token": localStorage.getItem("token"),
          },
        }
      );
      return res?.data || null;
    } catch (err) {
      toast.error(err?.response?.data?.error);
    }
  },
};

export default AssignmentService;
