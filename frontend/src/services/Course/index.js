import axiosInstance from '../../config/axiosConfig';
import { toast } from 'react-toastify';

const CourseService = {
    async getAllCourses(){
        try{
            let res = await axiosInstance.get('/api/course/');
            return res?.data || null;
        }catch(err){
            toast.error(err?.response?.data?.error || 'Something went wrong!')
        }
    },
    async getAllWeeksContentByCourse(courseId){
        try{
            let res = await axiosInstance.get(`/api/course/${courseId}`);
            return res?.data || null;
        }catch(err){
            toast.error(err?.response?.data?.error || 'Something went wrong!')
        }
    },
    async getAllAssignmentsByCourse(courseId){
        try{
            let res = await axiosInstance.get(`/api/course/assignments/${courseId}`);
            return res?.data || null;
        }catch(err){
            toast.error(err?.response?.data?.error || 'Something went wrong!')
        }
    }
}


export default CourseService;