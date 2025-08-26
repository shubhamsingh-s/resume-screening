import React from 'react';
import { Link } from 'react-router-dom';

const Navigation = () => {
    return (
        <nav className="bg-gray-800 p-4">
            <ul className="flex space-x-4">
                <li>
                    <Link to="/" className="text-white hover:text-gray-300">Home</Link>
                </li>
                <li>
                    <Link to="/analyze" className="text-white hover:text-gray-300">Analyze Resume</Link>
                </li>
                <li>
                    <Link to="/recommendations" className="text-white hover:text-gray-300">Job Recommendations</Link>
                </li>
                <li>
                    <Link to="/skills" className="text-white hover:text-gray-300">Job Skills</Link>
                </li>
            </ul>
        </nav>
    );
};

export default Navigation;
