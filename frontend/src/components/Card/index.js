import { memo } from "react";

const Card = ({ course, content,handleClick = () => {} }) => (
   
    <div className="bg-white shadow-md rounded-lg p-4 mb-4" onClick={handleClick}>
        {content}
    </div>
)

export default memo(Card)