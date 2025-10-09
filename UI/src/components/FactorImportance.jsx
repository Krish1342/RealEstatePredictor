import React, { useState, useEffect } from 'react';

const FactorImportance = ({ factors, isVisible = true }) => {
  const [animatedFactors, setAnimatedFactors] = useState([]);

  // Sample factor data - in real app, this would come from your ML model
  const defaultFactors = [
    { name: 'Location', importance: 35, description: 'Neighborhood, proximity to amenities, city area' },
    { name: 'Property Size', importance: 25, description: 'Square footage, plot area, built-up area' },
    { name: 'Bedrooms & Bathrooms', importance: 15, description: 'Number of rooms and bathrooms' },
    { name: 'Environmental Factors', importance: 15, description: 'Air quality, noise levels, water quality' },
    { name: 'Crime Rate & Safety', importance: 10, description: 'Area safety, crime statistics' }
  ];

  const displayFactors = factors || defaultFactors;

  useEffect(() => {
    if (isVisible) {
      // Animate the factors one by one
      const timer = setTimeout(() => {
        setAnimatedFactors(displayFactors.map(factor => ({
          ...factor,
          animatedImportance: 0
        })));
        
        // Animate each factor's percentage
        displayFactors.forEach((factor, index) => {
          setTimeout(() => {
            setAnimatedFactors(prev => {
              const newFactors = [...prev];
              newFactors[index] = { ...newFactors[index], animatedImportance: factor.importance };
              return newFactors;
            });
          }, index * 300);
        });
      }, 500);

      return () => clearTimeout(timer);
    }
  }, [isVisible, displayFactors]);

  if (!isVisible) return null;

  return (
    <div className="bg-white rounded-2xl shadow-xl p-6">
      <h3 className="text-2xl font-bold text-gray-800 mb-2">What Drives Property Prices?</h3>
      <p className="text-gray-600 mb-6">Our AI analyzes multiple factors to determine property values</p>
      
      <div className="space-y-4">
        {animatedFactors.map((factor, index) => (
          <div key={index} className="flex items-center justify-between p-4 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors">
            <div className="flex-1">
              <div className="flex items-center justify-between mb-2">
                <span className="font-semibold text-gray-800">{factor.name}</span>
                <span className="text-lg font-bold text-indigo-600">
                  {factor.animatedImportance}%
                </span>
              </div>
              
              <div className="w-full bg-gray-200 rounded-full h-3">
                <div 
                  className="bg-gradient-to-r from-indigo-500 to-purple-600 h-3 rounded-full transition-all duration-1000 ease-out"
                  style={{ width: `${factor.animatedImportance}%` }}
                ></div>
              </div>
              
              <p className="text-sm text-gray-600 mt-2">{factor.description}</p>
            </div>
          </div>
        ))}
      </div>

      <div className="mt-6 p-4 bg-blue-50 rounded-lg border border-blue-200">
        <div className="flex items-start">
          <div className="flex-shrink-0">
            <i className="fas fa-brain text-blue-500 text-xl mt-1"></i>
          </div>
          <div className="ml-3">
            <h4 className="text-sm font-semibold text-blue-800">AI-Powered Analysis</h4>
            <p className="text-sm text-blue-700 mt-1">
              Our machine learning models consider these factors along with real-time environmental data 
              to provide accurate property valuations.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default FactorImportance;