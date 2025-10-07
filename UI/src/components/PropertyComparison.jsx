import React, { useState } from 'react';

const PropertyComparison = () => {
  const [comparisonProperties, setComparisonProperties] = useState([]);
  const [showComparison, setShowComparison] = useState(false);

  // Sample properties for demonstration
  const sampleProperties = [
    {
      id: 1,
      name: "Modern 3BHK in Koramangala",
      location: "Koramangala, Bangalore",
      price: "₹72,50,000",
      area: "1500 sq. ft.",
      bedrooms: 3,
      bathrooms: 2,
      age: "5 years",
      amenities: ["Parking", "Garden", "Security"],
      factors: {
        location: 9,
        safety: 8,
        amenities: 7,
        environment: 8,
        connectivity: 9
      },
      image: "https://images.unsplash.com/photo-1568605114967-8130f3a36994?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1000&q=80"
    },
    {
      id: 2,
      name: "Luxury 4BHK in Indiranagar",
      location: "Indiranagar, Bangalore",
      price: "₹95,00,000",
      area: "2000 sq. ft.",
      bedrooms: 4,
      bathrooms: 3,
      age: "2 years",
      amenities: ["Pool", "Gym", "Parking", "Security"],
      factors: {
        location: 10,
        safety: 9,
        amenities: 9,
        environment: 8,
        connectivity: 8
      },
      image: "https://images.unsplash.com/photo-1613977257363-707ba9348227?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1000&q=80"
    },
    {
      id: 3,
      name: "Spacious 2BHK in HSR Layout",
      location: "HSR Layout, Bangalore",
      price: "₹58,00,000",
      area: "1200 sq. ft.",
      bedrooms: 2,
      bathrooms: 2,
      age: "8 years",
      amenities: ["Parking", "Garden"],
      factors: {
        location: 7,
        safety: 7,
        amenities: 6,
        environment: 7,
        connectivity: 8
      },
      image: "https://images.unsplash.com/photo-1545324418-cc1a3fa10c00?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1000&q=80"
    }
  ];

  const addToComparison = (property) => {
    if (comparisonProperties.length < 3 && !comparisonProperties.find(p => p.id === property.id)) {
      setComparisonProperties([...comparisonProperties, property]);
      setShowComparison(true);
    }
  };

  const removeFromComparison = (propertyId) => {
    const updated = comparisonProperties.filter(p => p.id !== propertyId);
    setComparisonProperties(updated);
    if (updated.length === 0) {
      setShowComparison(false);
    }
  };

  const clearComparison = () => {
    setComparisonProperties([]);
    setShowComparison(false);
  };

  const PropertyCard = ({ property, onAdd, isInComparison }) => (
    <div className="property-card bg-white rounded-xl overflow-hidden">
      <div className="relative">
        <img 
          src={property.image} 
          alt={property.name}
          className="w-full h-48 object-cover"
        />
        <div className="absolute top-3 right-3">
          {isInComparison ? (
            <button className="bg-green-500 text-white p-2 rounded-full">
              <i className="fas fa-check"></i>
            </button>
          ) : (
            <button 
              onClick={() => onAdd(property)}
              className="bg-indigo-600 text-white p-2 rounded-full hover:bg-indigo-700 transition"
            >
              <i className="fas fa-plus"></i>
            </button>
          )}
        </div>
      </div>
      
      <div className="p-4">
        <h3 className="font-bold text-lg text-gray-800 mb-1">{property.name}</h3>
        <p className="text-gray-600 text-sm mb-2 flex items-center">
          <i className="fas fa-map-marker-alt text-gray-400 mr-1"></i>
          {property.location}
        </p>
        
        <div className="text-2xl font-bold text-indigo-600 mb-3">{property.price}</div>
        
        <div className="grid grid-cols-2 gap-2 text-sm text-gray-600 mb-3">
          <div className="flex items-center">
            <i className="fas fa-arrows-alt mr-1 text-gray-400"></i>
            {property.area}
          </div>
          <div className="flex items-center">
            <i className="fas fa-bed mr-1 text-gray-400"></i>
            {property.bedrooms} Beds
          </div>
          <div className="flex items-center">
            <i className="fas fa-bath mr-1 text-gray-400"></i>
            {property.bathrooms} Baths
          </div>
          <div className="flex items-center">
            <i className="fas fa-calendar mr-1 text-gray-400"></i>
            {property.age}
          </div>
        </div>
        
        <div className="flex flex-wrap gap-1 mb-3">
          {property.amenities.map((amenity, index) => (
            <span key={index} className="px-2 py-1 bg-gray-100 text-gray-600 text-xs rounded">
              {amenity}
            </span>
          ))}
        </div>
      </div>
    </div>
  );

  const ComparisonTable = () => (
    <div className="bg-white rounded-2xl shadow-xl p-6">
      <div className="flex justify-between items-center mb-6">
        <h3 className="text-2xl font-bold text-gray-800">Property Comparison</h3>
        <button 
          onClick={clearComparison}
          className="px-4 py-2 bg-gray-200 text-gray-700 rounded-lg font-medium hover:bg-gray-300 transition"
        >
          Clear All
        </button>
      </div>

      <div className="overflow-x-auto">
        <table className="w-full">
          <thead>
            <tr className="border-b-2 border-gray-200">
              <th className="text-left pb-4 font-semibold text-gray-600">Features</th>
              {comparisonProperties.map((property) => (
                <th key={property.id} className="text-center pb-4">
                  <div className="relative">
                    <button 
                      onClick={() => removeFromComparison(property.id)}
                      className="absolute -top-2 -right-2 w-6 h-6 bg-red-500 text-white rounded-full text-xs hover:bg-red-600"
                    >
                      ×
                    </button>
                    <img 
                      src={property.image} 
                      alt={property.name}
                      className="w-20 h-16 object-cover rounded-lg mx-auto mb-2"
                    />
                    <div className="font-semibold text-gray-800">{property.name}</div>
                    <div className="text-lg font-bold text-indigo-600">{property.price}</div>
                  </div>
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {/* Basic Details */}
            <tr className="border-b border-gray-100">
              <td className="py-3 font-medium text-gray-700">Location</td>
              {comparisonProperties.map((property) => (
                <td key={property.id} className="py-3 text-center text-gray-600">
                  {property.location}
                </td>
              ))}
            </tr>
            
            <tr className="border-b border-gray-100">
              <td className="py-3 font-medium text-gray-700">Area</td>
              {comparisonProperties.map((property) => (
                <td key={property.id} className="py-3 text-center text-gray-600">
                  {property.area}
                </td>
              ))}
            </tr>
            
            <tr className="border-b border-gray-100">
              <td className="py-3 font-medium text-gray-700">Bedrooms</td>
              {comparisonProperties.map((property) => (
                <td key={property.id} className="py-3 text-center text-gray-600">
                  {property.bedrooms}
                </td>
              ))}
            </tr>
            
            <tr className="border-b border-gray-100">
              <td className="py-3 font-medium text-gray-700">Bathrooms</td>
              {comparisonProperties.map((property) => (
                <td key={property.id} className="py-3 text-center text-gray-600">
                  {property.bathrooms}
                </td>
              ))}
            </tr>
            
            <tr className="border-b border-gray-100">
              <td className="py-3 font-medium text-gray-700">Property Age</td>
              {comparisonProperties.map((property) => (
                <td key={property.id} className="py-3 text-center text-gray-600">
                  {property.age}
                </td>
              ))}
            </tr>

            {/* Factor Scores */}
            <tr className="bg-gray-50">
              <td colSpan={comparisonProperties.length + 1} className="py-3 font-bold text-gray-800">
                AI Analysis Scores
              </td>
            </tr>
            
            {Object.keys(comparisonProperties[0]?.factors || {}).map((factor) => (
              <tr key={factor} className="border-b border-gray-100">
                <td className="py-3 font-medium text-gray-700 capitalize">{factor}</td>
                {comparisonProperties.map((property) => (
                  <td key={property.id} className="py-3 text-center">
                    <div className="flex items-center justify-center">
                      <div className="w-24 bg-gray-200 rounded-full h-2 mr-2">
                        <div 
                          className="bg-green-500 h-2 rounded-full"
                          style={{ width: `${property.factors[factor] * 10}%` }}
                        ></div>
                      </div>
                      <span className="text-sm font-medium text-gray-700">
                        {property.factors[factor]}/10
                      </span>
                    </div>
                  </td>
                ))}
              </tr>
            ))}

            {/* Amenities */}
            <tr className="bg-gray-50">
              <td colSpan={comparisonProperties.length + 1} className="py-3 font-bold text-gray-800">
                Amenities
              </td>
            </tr>
            
            <tr>
              <td className="py-3 font-medium text-gray-700">Available Features</td>
              {comparisonProperties.map((property) => (
                <td key={property.id} className="py-3 text-center">
                  <div className="flex flex-col gap-1">
                    {property.amenities.map((amenity, index) => (
                      <span key={index} className="text-xs bg-blue-100 text-blue-700 px-2 py-1 rounded">
                        {amenity}
                      </span>
                    ))}
                  </div>
                </td>
              ))}
            </tr>
          </tbody>
        </table>
      </div>

      {/* Summary */}
      <div className="mt-6 p-4 bg-indigo-50 rounded-lg">
        <h4 className="font-semibold text-indigo-800 mb-2">Comparison Summary</h4>
        <div className="grid md:grid-cols-3 gap-4 text-sm">
          {comparisonProperties.map((property, index) => (
            <div key={property.id} className="bg-white p-3 rounded-lg">
              <div className="font-medium text-gray-800 mb-1">{property.name}</div>
              <div className="text-green-600 font-semibold">Best in: {index === 0 ? "Location & Value" : index === 1 ? "Luxury & Amenities" : "Affordability"}</div>
              <div className="text-gray-600 text-xs mt-1">
                {index === 0 ? "Great balance of price and location" : 
                 index === 1 ? "Premium features and prime location" : 
                 "Most affordable option with good connectivity"}
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );

  return (
    <div className="py-8">
      {!showComparison ? (
        <div>
          <div className="text-center mb-8">
            <h2 className="text-3xl font-bold text-gray-800 mb-2">Compare Properties</h2>
            <p className="text-gray-600 max-w-2xl mx-auto">
              Compare up to 3 properties side by side to make the best investment decision
            </p>
          </div>

          <div className="grid md:grid-cols-3 gap-6">
            {sampleProperties.map((property) => (
              <PropertyCard
                key={property.id}
                property={property}
                onAdd={addToComparison}
                isInComparison={comparisonProperties.some(p => p.id === property.id)}
              />
            ))}
          </div>

          {comparisonProperties.length > 0 && (
            <div className="fixed bottom-6 left-1/2 transform -translate-x-1/2">
              <button
                onClick={() => setShowComparison(true)}
                className="bg-indigo-600 text-white px-6 py-3 rounded-full font-semibold shadow-lg hover:bg-indigo-700 transition flex items-center"
              >
                <i className="fas fa-chart-bar mr-2"></i>
                Compare {comparisonProperties.length} Property{comparisonProperties.length > 1 ? 'ies' : ''}
              </button>
            </div>
          )}
        </div>
      ) : (
        <ComparisonTable />
      )}
    </div>
  );
};

export default PropertyComparison;