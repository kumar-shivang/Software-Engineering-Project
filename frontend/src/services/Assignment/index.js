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
      toast.error(err?.response?.data?.error || 'Something went wrong!');
    }
  },
  async getPrograamingAssignmetById(assignmentId) {
    try {
      let res = await axiosInstance.get(`/api/assignment/programming_assignments/${assignmentId}`, {
        headers: {
          "x-access-token": localStorage.getItem("token"),
        },
      });
      return res?.data || null;
    } catch (err) {
      toast.error(err?.response?.data?.error || 'Something went wrong!');
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
      toast.error(err?.response?.data?.error || 'Something went wrong!');
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
      toast.error(err?.response?.data?.error || 'Something went wrong!');
    }
  },
  async submitProgrammingAssignment(assignmentId, code) {
    try {
      let res = await axiosInstance.post(
        `/api/student/submit/programming/${assignmentId}`,
        { code },
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

export default AssignmentService;
