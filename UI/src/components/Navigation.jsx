import React from 'react';
import { Link } from 'react-router-dom';

const Navigation = ({ isLoggedIn, onLogout }) => {
  return (
    <nav className="navbar fixed w-full z-50 py-4">
      <div className="container mx-auto px-6 flex justify-between items-center">
        <div className="flex items-center">
          <div className="w-10 h-10 rounded-lg bg-indigo-600 flex items-center justify-center text-white font-bold mr-3">RP</div>
          <span className="text-xl font-bold text-gray-800">RealEstate Predictor</span>
        </div>
        
        <div className="hidden md:flex space-x-10">
          <Link to="/" className="text-gray-600 hover:text-indigo-600 font-medium">Home</Link>
          <Link to="/predict" className="text-gray-600 hover:text-indigo-600 font-medium">Predict</Link>
          <Link to="/about" className="text-gray-600 hover:text-indigo-600 font-medium">About</Link>
          <Link to="/contact" className="text-gray-600 hover:text-indigo-600 font-medium">Contact</Link>
          <Link to="/compare" className="text-gray-600 hover:text-indigo-600 font-medium">Compare</Link>
        </div>
        
        <div>
          <div className="flex items-center space-x-4">
            <span className="text-gray-700 hidden md:block">Welcome!</span>
            <button 
              className="px-4 py-2 rounded-full bg-gray-200 text-gray-700 font-medium hover:bg-gray-300 transition"
              onClick={onLogout}
            >
              Logout
            </button>
          </div>
        </div>
      </div>
    </nav>
  );
};

export default Navigation;