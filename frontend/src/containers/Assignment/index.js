import React, { memo } from "react";
import ProgrammingAssignment from '../ProgrammingAssignment/index'
import GradedAssignment from "../GradedAssignment";


const WeekAssignment = () => {

    return (
        <>
            <ProgrammingAssignment />
            <GradedAssignment />
        </>
    )
}

export default memo(WeekAssignment)