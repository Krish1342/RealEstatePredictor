import React, { useState, useEffect } from 'react';
import poiService from '../services/poiService';

const POIDisplay = ({ location, isVisible = true }) => {
  const [pois, setPois] = useState([]);
  const [loading, setLoading] = useState(false);
  const [amenityScore, setAmenityScore] = useState(0);
  const [selectedCategory, setSelectedCategory] = useState('all');

  useEffect(() => {
    if (location && isVisible) {
      fetchPOIs(location);
    }
  }, [location, isVisible]);

  const fetchPOIs = async (loc) => {
    setLoading(true);
    try {
      const poisData = await poiService.getAllPOIs(loc);
      setPois(poisData);
      
      const score = poiService.calculateAmenityScore(poisData);
      setAmenityScore(score);
    } catch (error) {
      console.error('Error fetching POIs:', error);
    } finally {
      setLoading(false);
    }
  };

  const categories = {
    all: 'All Places',
    education: 'Schools & Education',
    healthcare: 'Healthcare',
    shopping: 'Shopping',
    recreation: 'Parks & Recreation',
    transport: 'Transportation',
    dining: 'Restaurants',
    services: 'Services'
  };

  const filteredPois = selectedCategory === 'all' 
    ? pois 
    : pois.filter(poi => poi.category === selectedCategory);

  if (!isVisible) return null;

  return (
    <div className="bg-white rounded-2xl shadow-xl p-6">
      <div className="flex justify-between items-start mb-6">
        <div>
          <h3 className="text-2xl font-bold text-gray-800 mb-2">Nearby Amenities</h3>
          <p className="text-gray-600">Points of interest near {location}</p>
        </div>
        
        {/* Amenity Score Badge */}
        <div className="text-center">
          <div className="text-sm text-gray-600 mb-1">Amenity Score</div>
          <div className="bg-gradient-to-r from-green-500 to-green-600 text-white px-4 py-2 rounded-full font-bold text-lg">
            {amenityScore}/10
          </div>
        </div>
      </div>

      {/* Category Filter */}
      <div className="flex flex-wrap gap-2 mb-6">
        {Object.entries(categories).map(([key, label]) => (
          <button
            key={key}
            onClick={() => setSelectedCategory(key)}
            className={`px-4 py-2 rounded-full text-sm font-medium transition-colors ${
              selectedCategory === key
                ? 'bg-indigo-600 text-white'
                : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
            }`}
          >
            {label}
          </button>
        ))}
      </div>

      {/* Loading State */}
      {loading && (
        <div className="flex justify-center items-center py-12">
          <div className="loading-dots">
            <span></span>
            <span></span>
            <span></span>
          </div>
          <span className="ml-3 text-gray-600">Finding nearby places...</span>
        </div>
      )}

      {/* POI List */}
      {!loading && filteredPois.length > 0 && (
        <div className="grid gap-4 max-h-96 overflow-y-auto">
          {filteredPois.map((poi) => (
            <div
              key={poi.id}
              className="flex items-center p-4 border border-gray-200 rounded-lg hover:bg-gray-50 transition-colors"
            >
              <div className="w-12 h-12 rounded-full bg-indigo-100 flex items-center justify-center text-indigo-600 mr-4">
                <i className={poi.icon}></i>
              </div>
              
              <div className="flex-1">
                <h4 className="font-semibold text-gray-800">{poi.name}</h4>
                <p className="text-sm text-gray-600 truncate">{poi.address}</p>
                <div className="flex items-center mt-1">
                  <span className="text-xs bg-gray-100 text-gray-700 px-2 py-1 rounded">
                    {poi.type}
                  </span>
                  <span className="text-xs text-gray-500 ml-2">
                    Importance: {(poi.importance * 10).toFixed(1)}
                  </span>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Empty State */}
      {!loading && filteredPois.length === 0 && location && (
        <div className="text-center py-12">
          <i className="fas fa-map-marker-alt text-gray-400 text-4xl mb-4"></i>
          <p className="text-gray-600">No places found near {location}</p>
          <p className="text-sm text-gray-500 mt-2">Try a more specific location</p>
        </div>
      )}

      {/* No Location State */}
      {!location && (
        <div className="text-center py-12">
          <i className="fas fa-search-location text-gray-400 text-4xl mb-4"></i>
          <p className="text-gray-600">Enter a location to see nearby amenities</p>
        </div>
      )}

      {/* Score Explanation */}
      {amenityScore > 0 && (
        <div className="mt-6 p-4 bg-blue-50 rounded-lg border border-blue-200">
          <div className="flex items-start">
            <i className="fas fa-info-circle text-blue-500 text-lg mt-1 mr-3"></i>
            <div>
              <h4 className="font-semibold text-blue-800 mb-1">About the Amenity Score</h4>
              <p className="text-sm text-blue-700">
                Score {amenityScore}/10 based on variety and quality of nearby amenities. 
                Higher scores indicate better access to schools, hospitals, parks, and shopping.
              </p>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default POIDisplay;