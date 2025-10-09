import React, { useState } from 'react';

const WhatIfScenarios = ({ currentPrediction, onScenarioChange }) => {
  const [activeScenario, setActiveScenario] = useState(null);

  const scenarios = [
    {
      id: 'better-location',
      title: 'Better Location',
      description: 'If property was in a premium neighborhood',
      icon: 'fas fa-map-marker-alt',
      color: 'green',
      impact: '+15%',
      factors: ['Lower crime rate', 'Better schools', 'More amenities']
    },
    {
      id: 'more-space',
      title: 'Larger Area',
      description: 'If property had 20% more area',
      icon: 'fas fa-expand-arrows-alt',
      color: 'blue',
      impact: '+12%',
      factors: ['More living space', 'Better resale value', 'Higher comfort']
    },
    {
      id: 'more-rooms',
      title: 'Extra Bedroom',
      description: 'If property had one more bedroom',
      icon: 'fas fa-bed',
      color: 'purple',
      impact: '+8%',
      factors: ['Accommodates more people', 'Better rental potential', 'Family-friendly']
    },
    {
      id: 'better-environment',
      title: 'Improved Environment',
      description: 'If area had better air and water quality',
      icon: 'fas fa-leaf',
      color: 'emerald',
      impact: '+10%',
      factors: ['Healthier living', 'Long-term value', 'Premium appeal']
    }
  ];

  const handleScenarioClick = (scenario) => {
    if (activeScenario === scenario.id) {
      setActiveScenario(null);
      onScenarioChange(null);
    } else {
      setActiveScenario(scenario.id);
      onScenarioChange(scenario);
    }
  };

  return (
    <div className="bg-white rounded-2xl shadow-xl p-6">
      <h3 className="text-2xl font-bold text-gray-800 mb-2">Explore What-If Scenarios</h3>
      <p className="text-gray-600 mb-6">See how different factors affect property value</p>

      <div className="grid md:grid-cols-2 gap-4">
        {scenarios.map((scenario) => (
          <div
            key={scenario.id}
            className={`border-2 rounded-xl p-4 cursor-pointer transition-all duration-300 ${
              activeScenario === scenario.id
                ? `border-${scenario.color}-500 bg-${scenario.color}-50 transform scale-105`
                : 'border-gray-200 hover:border-gray-300 hover:bg-gray-50'
            }`}
            onClick={() => handleScenarioClick(scenario)}
          >
            <div className="flex items-start justify-between">
              <div className="flex items-center">
                <div className={`w-10 h-10 rounded-full bg-${scenario.color}-100 flex items-center justify-center text-${scenario.color}-600 mr-3`}>
                  <i className={`${scenario.icon}`}></i>
                </div>
                <div>
                  <h4 className="font-semibold text-gray-800">{scenario.title}</h4>
                  <p className="text-sm text-gray-600">{scenario.description}</p>
                </div>
              </div>
              <div className={`text-lg font-bold text-${scenario.color}-600`}>
                {scenario.impact}
              </div>
            </div>

            {activeScenario === scenario.id && (
              <div className="mt-3 pt-3 border-t border-gray-200">
                <p className="text-sm font-medium text-gray-700 mb-2">Key Improvements:</p>
                <ul className="text-sm text-gray-600 space-y-1">
                  {scenario.factors.map((factor, index) => (
                    <li key={index} className="flex items-center">
                      <i className={`fas fa-check text-${scenario.color}-500 mr-2 text-xs`}></i>
                      {factor}
                    </li>
                  ))}
                </ul>
              </div>
            )}
          </div>
        ))}
      </div>

      {activeScenario && (
        <div className="mt-4 p-4 bg-gradient-to-r from-indigo-500 to-purple-600 rounded-lg text-white">
          <div className="flex items-center justify-between">
            <div>
              <h4 className="font-semibold">Potential Value Increase</h4>
              <p className="text-sm opacity-90">Explore how improvements can boost your property value</p>
            </div>
            <button 
              className="px-4 py-2 bg-white text-indigo-600 rounded-lg font-semibold hover:bg-gray-100 transition"
              onClick={() => {
                setActiveScenario(null);
                onScenarioChange(null);
              }}
            >
              Reset
            </button>
          </div>
        </div>
      )}
    </div>
  );
};

export default WhatIfScenarios;