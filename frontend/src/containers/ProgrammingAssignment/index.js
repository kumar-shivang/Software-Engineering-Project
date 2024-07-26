import React, { memo }  from "react";
import CodeEditor from "../../components/CodeEditor";

const ProgrammingAssignment = () => {


    return (
        <>
            <p>Programming Assignment</p>
            <CodeEditor />
        </>
    )
}

export default memo(ProgrammingAssignment)