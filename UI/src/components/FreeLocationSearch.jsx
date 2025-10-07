import React, { useState } from 'react';

const FreeLocationSearch = ({ onLocationSelect, value, onChange }) => {
  const [suggestions, setSuggestions] = useState([]);
  const [showSuggestions, setShowSuggestions] = useState(false);

  // Enhanced Indian locations with specific areas
  const commonLocations = [
    // Bangalore areas
    "Koramangala, Bangalore",
    "Indiranagar, Bangalore", 
    "Whitefield, Bangalore",
    "Marathahalli, Bangalore",
    "Electronic City, Bangalore",
    "HSR Layout, Bangalore",
    "JP Nagar, Bangalore",
    "BTM Layout, Bangalore",
    "Jayanagar, Bangalore",
    "Malleshwaram, Bangalore",
    
    // Mumbai areas
    "Bandra, Mumbai",
    "Andheri, Mumbai",
    "Powai, Mumbai",
    "Juhu, Mumbai",
    "Dadar, Mumbai",
    
    // Delhi areas
    "Connaught Place, Delhi",
    "Dwarka, Delhi", 
    "Saket, Delhi",
    "Rohini, Delhi",
    "Vasant Kunj, Delhi",
    
    // Hyderabad areas
    "Gachibowli, Hyderabad",
    "HITEC City, Hyderabad",
    "Banjara Hills, Hyderabad",
    "Jubilee Hills, Hyderabad",
    
    // Chennai areas
    "Anna Nagar, Chennai",
    "T. Nagar, Chennai",
    "Adyar, Chennai",
    
    // Major cities
    "Bangalore, Karnataka",
    "Mumbai, Maharashtra", 
    "Delhi, India",
    "Hyderabad, Telangana",
    "Chennai, Tamil Nadu",
    "Kolkata, West Bengal",
    "Pune, Maharashtra",
    "Ahmedabad, Gujarat"
  ];

  const handleInputChange = (e) => {
    const value = e.target.value;
    onChange(value);

    if (value.length > 1) {
      const filtered = commonLocations.filter(loc => 
        loc.toLowerCase().includes(value.toLowerCase())
      );
      setSuggestions(filtered);
      setShowSuggestions(true);
    } else {
      setSuggestions([]);
      setShowSuggestions(false);
    }
  };

  const handleSuggestionClick = (suggestion) => {
    onChange(suggestion);
    setShowSuggestions(false);
    if (onLocationSelect) {
      onLocationSelect(suggestion);
    }
  };

  return (
    <div className="relative">
      <div className="flex items-center">
        <i className="fas fa-map-marker-alt text-gray-400 absolute left-3 z-10"></i>
        <input
          type="text"
          value={value}
          onChange={handleInputChange}
          onFocus={() => value.length > 1 && setShowSuggestions(true)}
          onBlur={() => setTimeout(() => setShowSuggestions(false), 200)}
          className="input-field w-full pl-10 pr-4 py-3"
          placeholder="Enter property location (e.g., Koramangala, Bangalore)"
          required
        />
      </div>
      
      {showSuggestions && suggestions.length > 0 && (
        <div className="absolute z-20 w-full mt-1 bg-white border border-gray-300 rounded-lg shadow-lg max-h-60 overflow-y-auto">
          {suggestions.map((suggestion, index) => (
            <div
              key={index}
              className="px-4 py-3 hover:bg-gray-50 cursor-pointer border-b border-gray-100 last:border-b-0"
              onClick={() => handleSuggestionClick(suggestion)}
            >
              <div className="flex items-center">
                <i className="fas fa-map-marker-alt text-gray-400 mr-3"></i>
                <div>
                  <p className="text-sm font-medium text-gray-800">{suggestion}</p>
                  <p className="text-xs text-gray-500">
                    {suggestion.includes('Bangalore') ? 'Karnataka' : 
                     suggestion.includes('Mumbai') ? 'Maharashtra' :
                     suggestion.includes('Delhi') ? 'Delhi' :
                     suggestion.includes('Hyderabad') ? 'Telangana' :
                     suggestion.includes('Chennai') ? 'Tamil Nadu' : 'India'}
                  </p>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default FreeLocationSearch;