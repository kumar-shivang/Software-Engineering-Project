import React, { memo } from 'react';

const Home = () => {

    return (
        <div className="h-full p-8 bg-gray-100">
        <header className="flex justify-between items-center mb-8">
            <div>
                <h2 className="text-3xl font-semibold text-gray-800">Welcome to E-Learn</h2>
                <p className="text-gray-600">Your personalized dashboard</p>
            </div>
        </header>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-8 bg-gray-100">
            <div className="bg-white p-6 rounded-lg shadow-md">
                <h3 className="text-xl font-semibold text-gray-800">Courses Enrolled</h3>
                <p className="mt-2 text-3xl font-bold text-blue-500">5</p>
            </div>
            <div className="bg-white p-6 rounded-lg shadow-md">
                <h3 className="text-xl font-semibold text-gray-800">Courses Completed</h3>
                <p className="mt-2 text-3xl font-bold text-green-500">3</p>
            </div>
            <div className="bg-white p-6 rounded-lg shadow-md">
                <h3 className="text-xl font-semibold text-gray-800">Hours Studied</h3>
                <p className="mt-2 text-3xl font-bold text-purple-500">120</p>
            </div>
        </div>

        <div className="bg-white p-6 rounded-lg shadow-md">
            <h3 className="text-2xl font-semibold text-gray-800 mb-4">Recent Updates</h3>
            <div className="space-y-4">
                <div className="flex items-start space-x-4">
                    <div className="flex-shrink-0">
                        <i className="fas fa-bell text-blue-500 text-2xl"></i>
                    </div>
                    <div>
                        <h4 className="text-lg font-semibold text-gray-800">New Course Available: Advanced Java</h4>
                        <p className="text-gray-600">A new course on advanced Java programming has been added. Check it out!</p>
                        <span className="text-sm text-gray-400">2 hours ago</span>
                    </div>
                </div>
                <div className="flex items-start space-x-4">
                    <div className="flex-shrink-0">
                        <i className="fas fa-bell text-blue-500 text-2xl"></i>
                    </div>
                    <div>
                        <h4 className="text-lg font-semibold text-gray-800">System Maintenance Scheduled</h4>
                        <p className="text-gray-600">The platform will undergo maintenance on Sunday from 2 AM to 4 AM.</p>
                        <span className="text-sm text-gray-400">1 day ago</span>
                    </div>
                </div>
            </div>
        </div>
    </div>

    )
}

export default memo(Home)