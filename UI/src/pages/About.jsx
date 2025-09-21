import React from 'react';

const About = () => {
  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-4xl mx-auto">
        <div className="text-center mb-12">
          <h1 className="text-4xl font-bold text-gray-900 mb-4">About RealEstate Predictor</h1>
          <p className="text-lg text-gray-600 max-w-2xl mx-auto">
            We leverage advanced machine learning algorithms to provide accurate property valuations based on multiple factors.
          </p>
        </div>

        <div className="bg-white rounded-2xl shadow-xl p-8 mb-8">
          <h2 className="text-2xl font-semibold text-gray-800 mb-4">Our Mission</h2>
          <p className="text-gray-600 mb-4">
            Our mission is to democratize access to accurate real estate valuation tools. We believe everyone should have access to transparent, data-driven property price predictions.
          </p>
          <p className="text-gray-600">
            By considering environmental factors like air quality, crime rates, noise pollution, and water quality alongside traditional real estate metrics, we provide a more comprehensive valuation model.
          </p>
        </div>

        <div className="bg-white rounded-2xl shadow-xl p-8">
          <h2 className="text-2xl font-semibold text-gray-800 mb-4">Our Technology</h2>
          <p className="text-gray-600 mb-4">
            We use state-of-the-art machine learning models trained on extensive datasets including:
          </p>
          <ul className="list-disc list-inside text-gray-600 mb-4">
            <li>Historical property transaction data</li>
            <li>Environmental quality metrics</li>
            <li>Urban development indicators</li>
            <li>Economic growth patterns</li>
          </ul>
          <p className="text-gray-600">
            Our algorithms continuously learn and improve as more data becomes available, ensuring our predictions remain accurate and relevant.
          </p>
        </div>
      </div>
    </div>
  );
};

export default About;