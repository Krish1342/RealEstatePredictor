import React from 'react';

const Features = () => {
  return (
    <section className="py-16 px-6 bg-white">
      <div className="container mx-auto">
        <h2 className="text-3xl font-bold text-center mb-4">How It Works</h2>
        <p className="text-gray-600 text-center max-w-2xl mx-auto mb-16">Our advanced AI analyzes multiple data points to deliver accurate property valuations</p>
        
        <div className="grid md:grid-cols-3 gap-10">
          <div className="text-center">
            <div className="feature-icon">
              <i className="fas fa-database text-white text-2xl"></i>
            </div>
            <h3 className="text-xl font-bold mb-3">Data Collection</h3>
            <p className="text-gray-600">We gather comprehensive data including property details, location factors, and environmental metrics.</p>
          </div>
          
          <div className="text-center">
            <div className="feature-icon">
              <i className="fas fa-brain text-white text-2xl"></i>
            </div>
            <h3 className="text-xl font-bold mb-3">AI Analysis</h3>
            <p className="text-gray-600">Our machine learning models process the data to identify patterns and predict accurate property values.</p>
          </div>
          
          <div className="text-center">
            <div className="feature-icon">
              <i className="fas fa-chart-line text-white text-2xl"></i>
            </div>
            <h3 className="text-xl font-bold mb-3">Result Delivery</h3>
            <p className="text-gray-600">You receive a detailed valuation report with price estimation and key influencing factors.</p>
          </div>
        </div>
      </div>
    </section>
  );
};

export default Features;