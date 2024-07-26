import React, { memo } from 'react';
import VideoPage from '../../components/VideoPage';

const WeekModule = () => {

    return (
        <div className="flex items-center justify-center min-h-screen bg-gray-100">
            <VideoPage />
        </div>
    )
}

export default memo(WeekModule)