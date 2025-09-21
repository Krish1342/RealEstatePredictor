import React from 'react';

const PopularCities = () => {
  const cities = [
    { name: 'Bangalore', price: '₹85L', growth: '5.2%', color: 'blue' },
    { name: 'Mumbai', price: '₹1.2Cr', growth: '7.8%', color: 'red' },
    { name: 'Delhi', price: '₹95L', growth: '4.5%', color: 'green' },
    { name: 'Hyderabad', price: '₹75L', growth: '6.1%', color: 'purple' }
  ];
  
  return (
    <section className="py-16 px-6 bg-gray-50">
      <div className="container mx-auto">
        <h2 className="text-3xl font-bold text-center mb-4">Properties in Popular Cities</h2>
        <p className="text-gray-600 text-center max-w-2xl mx-auto mb-12">Explore property prices in major Indian cities</p>
        
        <div className="grid md:grid-cols-4 gap-6">
          {cities.map((city, index) => (
            <div key={index} className="city-card bg-white text-center p-6">
              <div className={`w-16 h-16 rounded-full bg-${city.color}-100 flex items-center justify-center text-${city.color}-600 text-2xl mx-auto mb-4`}>
                <i className="fas fa-city"></i>
              </div>
              <h3 className="font-bold text-lg mb-2">{city.name}</h3>
              <p className="text-gray-600 mb-3">Avg. Price: {city.price}</p>
              <div className="text-green-600 font-medium">
                <i className="fas fa-arrow-up"></i> {city.growth} last year
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
};

export default PopularCities;