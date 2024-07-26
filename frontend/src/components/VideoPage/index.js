import React from 'react';
import YouTube from 'react-youtube';

const VideoPage = () => {
    const videoId = 'wbt8XGSBF2s'; // Replace with your YouTube video ID

    const opts = {
        height: '390',
        width: '640',
        playerVars: {
            autoplay: 1,
        },
    };

    return (
        <div className="min-h-screen bg-gray-100 flex items-center p-1">
            <div className="bg-white shadow-md rounded-lg p-4">
                <YouTube videoId={videoId} opts={opts} />
            </div>
        </div>
    );
};

export default VideoPage;
