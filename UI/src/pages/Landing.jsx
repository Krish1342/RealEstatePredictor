import React from 'react';
import { Link } from 'react-router-dom';

const Landing = () => {
  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      {/* Navigation */}
      <nav className="navbar py-4">
        <div className="container mx-auto px-6 flex justify-between items-center">
          <div className="flex items-center">
            <div className="w-10 h-10 rounded-lg bg-indigo-600 flex items-center justify-center text-white font-bold mr-3">RP</div>
            <span className="text-xl font-bold text-gray-800">RealEstate Predictor</span>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <div className="container mx-auto px-6 pt-16 pb-20">
        <div className="hero-section py-16 px-8 text-center text-white">
          <h1 className="text-4xl md:text-5xl font-bold mb-6">Smart Property Valuation in Minutes</h1>
          <p className="text-xl max-w-2xl mx-auto mb-10">AI-powered real estate price prediction using advanced machine learning algorithms</p>
        </div>

        {/* Auth Options */}
        <div className="max-w-4xl mx-auto grid md:grid-cols-2 gap-10 mt-16">
          {/* Login Card */}
          <div className="bg-white rounded-2xl shadow-xl p-8 text-center">
            <div className="w-16 h-16 rounded-full bg-indigo-100 flex items-center justify-center text-indigo-600 text-2xl mx-auto mb-6">
              <i className="fas fa-sign-in-alt"></i>
            </div>
            <h2 className="text-2xl font-bold text-gray-800 mb-4">Welcome Back</h2>
            <p className="text-gray-600 mb-6">Sign in to access your account and property predictions</p>
            <Link to="/login" className="btn-primary w-full py-3 text-lg font-semibold inline-block">
              Sign In
            </Link>
          </div>

          {/* Signup Card */}
          <div className="bg-white rounded-2xl shadow-xl p-8 text-center">
            <div className="w-16 h-16 rounded-full bg-green-100 flex items-center justify-center text-green-600 text-2xl mx-auto mb-6">
              <i className="fas fa-user-plus"></i>
            </div>
            <h2 className="text-2xl font-bold text-gray-800 mb-4">Create Account</h2>
            <p className="text-gray-600 mb-6">Join us to get accurate property valuations and market insights</p>
            <Link to="/signup" className="btn-primary w-full py-3 text-lg font-semibold inline-block bg-gradient-to-r from-green-500 to-green-600 hover:from-green-600 hover:to-green-700">
              Sign Up
            </Link>
          </div>
        </div>

        {/* Features Preview */}
        <div className="max-w-4xl mx-auto mt-20">
          <h2 className="text-3xl font-bold text-center text-gray-800 mb-12">Why Choose Us?</h2>
          <div className="grid md:grid-cols-3 gap-8">
            <div className="text-center">
              <div className="feature-icon">
                <i className="fas fa-bolt text-white text-2xl"></i>
              </div>
              <h3 className="text-xl font-semibold text-gray-800 mb-3">Instant Predictions</h3>
              <p className="text-gray-600">Get accurate property valuations in seconds</p>
            </div>
            <div className="text-center">
              <div className="feature-icon">
                <i className="fas fa-chart-line text-white text-2xl"></i>
              </div>
              <h3 className="text-xl font-semibold text-gray-800 mb-3">Market Insights</h3>
              <p className="text-gray-600">Access comprehensive market data and trends</p>
            </div>
            <div className="text-center">
              <div className="feature-icon">
                <i className="fas fa-shield-alt text-white text-2xl"></i>
              </div>
              <h3 className="text-xl font-semibold text-gray-800 mb-3">Secure & Private</h3>
              <p className="text-gray-600">Your data is always protected and confidential</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Landing;