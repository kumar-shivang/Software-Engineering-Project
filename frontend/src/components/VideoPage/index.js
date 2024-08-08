import React from 'react';
import YouTube from 'react-youtube';

const VideoPage = ({ src }) => {
    const getVideoId = (url) => {
        const urlObj = new URL(url);
        const params = new URLSearchParams(urlObj.search);
        return params.get('v');
    };

    const videoId = getVideoId(src);

    const opts = {
        height: '390',
        width: '640',
        playerVars: {
            autoplay: 1,
        },
    };

    return (
        <div className="bg-gray-100 flex items-center justify-center">
            <div className="bg-white shadow-md rounded-lg p-4">
                {videoId ? (
                    <YouTube videoId={videoId} opts={opts} />
                ) : (
                    <p>Invalid video URL</p>
                )}
            </div>
        </div>
    );
};

export default VideoPage;
