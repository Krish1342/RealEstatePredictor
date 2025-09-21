import React from 'react';

const Footer = () => {
  return (
    <footer className="bg-gray-900 text-white py-12 px-6">
      <div className="container mx-auto">
        <div className="grid md:grid-cols-4 gap-8">
          <div>
            <div className="flex items-center mb-6">
              <div className="w-10 h-10 rounded-lg bg-indigo-600 flex items-center justify-center text-white font-bold mr-3">RP</div>
              <span className="text-xl font-bold">RealEstate Predictor</span>
            </div>
            <p className="text-gray-400 mb-6">AI-powered property valuation for the modern real estate market.</p>
            <div className="flex space-x-4">
              <a href="#" className="text-gray-400 hover:text-white"><i className="fab fa-facebook-f"></i></a>
              <a href="#" className="text-gray-400 hover:text-white"><i className="fab fa-twitter"></i></a>
              <a href="#" className="text-gray-400 hover:text-white"><i className="fab fa-instagram"></i></a>
              <a href="#" className="text-gray-400 hover:text-white"><i className="fab fa-linkedin-in"></i></a>
            </div>
          </div>
          
          <div>
            <h4 className="text-lg font-semibold mb-6">Quick Links</h4>
            <ul className="space-y-3">
              <li><a href="#" className="text-gray-400 hover:text-white">Home</a></li>
              <li><a href="#" className="text-gray-400 hover:text-white">Predict</a></li>
              <li><a href="#" className="text-gray-400 hover:text-white">About Us</a></li>
              <li><a href="#" className="text-gray-400 hover:text-white">Contact</a></li>
              <li><a href="#" className="text-gray-400 hover:text-white">Privacy Policy</a></li>
            </ul>
          </div>
          
          <div>
            <h4 className="text-lg font-semibold mb-6">Cities</h4>
            <ul className="space-y-3">
              <li><a href="#" className="text-gray-400 hover:text-white">Bangalore</a></li>
              <li><a href="#" className="text-gray-400 hover:text-white">Mumbai</a></li>
              <li><a href="#" className="text-gray-400 hover:text-white">Delhi</a></li>
              <li><a href="#" className="text-gray-400 hover:text-white">Hyderabad</a></li>
              <li><a href="#" className="text-gray-400 hover:text-white">Chennai</a></li>
            </ul>
          </div>
          
          <div>
            <h4 className="text-lg font-semibold mb-6">Contact Us</h4>
            <ul className="space-y-3">
              <li className="flex items-center">
                <i className="fas fa-map-marker-alt mr-3 text-indigo-500"></i>
                <span className="text-gray-400">123 Tech Park, Bangalore</span>
              </li>
              <li className="flex items-center">
                <i className="fas fa-phone mr-3 text-indigo-500"></i>
                <span className="text-gray-400">+91 9876543210</span>
              </li>
              <li className="flex items-center">
                <i className="fas fa-envelope mr-3 text-indigo-500"></i>
                <span className="text-gray-400">info@realestatepredictor.com</span>
              </li>
            </ul>
          </div>
        </div>
        
        <div className="border-t border-gray-800 mt-12 pt-8 text-center text-gray-400">
          <p>© 2023 RealEstate Predictor. All rights reserved.</p>
        </div>
      </div>
    </footer>
  );
};

export default Footer;