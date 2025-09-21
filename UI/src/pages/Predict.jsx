import React, { useState } from 'react';
import { motion } from 'framer-motion';

const Predict = () => {
  const [formData, setFormData] = useState({
    location: '',
    area: '',
    bedrooms: '',
    bathrooms: '',
    age: '',
    amenities: {
      parking: false,
      garden: false,
      pool: false,
      gym: false
    }
  });
  
  const [prediction, setPrediction] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleCheckboxChange = (e) => {
    const { name, checked } = e.target;
    setFormData(prev => ({
      ...prev,
      amenities: {
        ...prev.amenities,
        [name]: checked
      }
    }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    setLoading(true);
    
    // Simulate API call
    setTimeout(() => {
      setPrediction({
        price: '₹72,50,000',
        accuracy: '85%',
        factors: [
          'Good location',
          'Low crime rate',
          'Excellent air quality',
          'Good water quality'
        ]
      });
      setLoading(false);
    }, 2500);
  };

  return (
    <section className="py-16 px-6">
      <div className="container mx-auto">
        <h2 className="text-3xl font-bold text-center mb-4">Predict Property Price</h2>
        <p className="text-gray-600 text-center max-w-2xl mx-auto mb-12">Our advanced algorithm analyzes multiple factors to provide accurate property valuation</p>
        
        <div className="grid md:grid-cols-2 gap-10">
          <motion.div 
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.5, delay: 0.2 }}
            className="prediction-form p-8"
          >
            <form onSubmit={handleSubmit}>
              <div className="mb-6">
                <label className="block text-gray-700 mb-2 font-medium" htmlFor="location">Location</label>
                <input 
                  type="text" 
                  id="location" 
                  name="location"
                  value={formData.location}
                  onChange={handleChange}
                  className="input-field w-full px-5 py-4" 
                  placeholder="e.g., Bangalore, Indiranagar" 
                  required
                />
              </div>
              
              <div className="grid grid-cols-2 gap-6 mb-6">
                <div>
                  <label className="block text-gray-700 mb-2 font-medium" htmlFor="area">Area (sq. ft.)</label>
                  <input 
                    type="number" 
                    id="area" 
                    name="area"
                    value={formData.area}
                    onChange={handleChange}
                    className="input-field w-full px-5 py-4" 
                    placeholder="e.g., 1500" 
                    required
                  />
                </div>
                <div>
                  <label className="block text-gray-700 mb-2 font-medium" htmlFor="bedrooms">Bedrooms</label>
                  <select 
                    id="bedrooms" 
                    name="bedrooms"
                    value={formData.bedrooms}
                    onChange={handleChange}
                    className="input-field w-full px-5 py-4"
                    required
                  >
                    <option value="">Select</option>
                    <option value="1">1</option>
                    <option value="2">2</option>
                    <option value="3">3</option>
                    <option value="4">4</option>
                    <option value="5+">5+</option>
                  </select>
                </div>
              </div>
              
              <div className="grid grid-cols-2 gap-6 mb-6">
                <div>
                  <label className="block text-gray-700 mb-2 font-medium" htmlFor="bathrooms">Bathrooms</label>
                  <select 
                    id="bathrooms" 
                    name="bathrooms"
                    value={formData.bathrooms}
                    onChange={handleChange}
                    className="input-field w-full px-5 py-4"
                    required
                  >
                    <option value="">Select</option>
                    <option value="1">1</option>
                    <option value="2">2</option>
                    <option value="3">3</option>
                    <option value="4+">4+</option>
                  </select>
                </div>
                <div>
                  <label className="block text-gray-700 mb-2 font-medium" htmlFor="age">Property Age (years)</label>
                  <input 
                    type="number" 
                    id="age" 
                    name="age"
                    value={formData.age}
                    onChange={handleChange}
                    className="input-field w-full px-5 py-4" 
                    placeholder="e.g., 5" 
                    required
                  />
                </div>
              </div>
              
              <div className="mb-8">
                <label className="block text-gray-700 mb-2 font-medium">Amenities</label>
                <div className="grid grid-cols-2 gap-4">
                  <label className="flex items-center">
                    <input 
                      type="checkbox" 
                      name="parking"
                      checked={formData.amenities.parking}
                      onChange={handleCheckboxChange}
                      className="mr-2 h-5 w-5 text-indigo-600" 
                    />
                    <span>Parking</span>
                  </label>
                  <label className="flex items-center">
                    <input 
                      type="checkbox" 
                      name="garden"
                      checked={formData.amenities.garden}
                      onChange={handleCheckboxChange}
                      className="mr-2 h-5 w-5 text-indigo-600" 
                    />
                    <span>Garden</span>
                  </label>
                  <label className="flex items-center">
                    <input 
                      type="checkbox" 
                      name="pool"
                      checked={formData.amenities.pool}
                      onChange={handleCheckboxChange}
                      className="mr-2 h-5 w-5 text-indigo-600" 
                    />
                    <span>Pool</span>
                  </label>
                  <label className="flex items-center">
                    <input 
                      type="checkbox" 
                      name="gym"
                      checked={formData.amenities.gym}
                      onChange={handleCheckboxChange}
                      className="mr-2 h-5 w-5 text-indigo-600" 
                    />
                    <span>Gym</span>
                  </label>
                </div>
              </div>
              
              <button 
                type="submit" 
                className="btn-primary w-full py-4 text-lg font-semibold"
                disabled={loading}
              >
                {loading ? (
                  <div className="flex items-center justify-center">
                    <div className="loading-dots">
                      <span></span>
                      <span></span>
                      <span></span>
                    </div>
                    <span className="ml-2">Predicting...</span>
                  </div>
                ) : 'Predict Price'}
              </button>
            </form>
          </motion.div>
          
          <motion.div 
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.5, delay: 0.4 }}
            className="flex flex-col justify-center"
          >
            {loading ? (
              <div className="result-card p-8 mb-8 text-center fade-in">
                <div className="text-center py-8">
                  <div className="loading-dots mb-4">
                    <span></span>
                    <span></span>
                    <span></span>
                  </div>
                  <h3 className="text-xl font-bold">Analyzing Property Data</h3>
                  <p className="mt-2">This may take a few seconds...</p>
                </div>
              </div>
            ) : prediction ? (
              <div className="result-card p-8 mb-8 text-center fade-in">
                <h3 className="text-2xl font-bold mb-4">Predicted Property Value</h3>
                <div className="text-4xl font-bold mb-4">{prediction.price}</div>
                <div className="price-badge inline-block text-sm font-semibold">{prediction.accuracy} Accuracy</div>
                <div className="mt-6">
                  <h4 className="font-medium mb-3">Key Positive Factors</h4>
                  <ul className="space-y-2">
                    {prediction.factors.map((factor, index) => (
                      <li key={index} className="flex items-center justify-center">
                        <svg className="h-5 w-5 text-green-300 mr-2" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg">
                          <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                        </svg>
                        <span>{factor}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              </div>
            ) : (
              <div className="result-card p-8 mb-8 text-center fade-in">
                <div className="flex flex-col items-center justify-center h-64 text-center">
                  <div className="mb-4 p-3 bg-indigo-100 rounded-full bg-opacity-20">
                    <i className="fas fa-home text-white text-4xl"></i>
                  </div>
                  <h3 className="text-xl font-bold mb-1">No Prediction Yet</h3>
                  <p className="text-white text-opacity-80">Fill out the form to get an accurate price estimation for your property.</p>
                </div>
              </div>
            )}
            
            <div className="bg-white rounded-2xl p-6 shadow-lg">
              <h4 className="font-bold text-lg mb-4">Factors Considered</h4>
              <ul className="space-y-3">
                <li className="flex items-center">
                  <div className="w-8 h-8 rounded-full bg-green-100 flex items-center justify-center text-green-600 mr-3">
                    <i className="fas fa-check"></i>
                  </div>
                  <span>Air Quality Index</span>
                </li>
                <li className="flex items-center">
                  <div className="w-8 h-8 rounded-full bg-green-100 flex items-center justify-center text-green-600 mr-3">
                    <i className="fas fa-check"></i>
                  </div>
                  <span>Crime Rate in Area</span>
                </li>
                <li className="flex items-center">
                  <div className="w-8 h-8 rounded-full bg-green-100 flex items-center justify-center text-green-600 mr-3">
                    <i className="fas fa-check"></i>
                  </div>
                  <span>Noise Pollution Levels</span>
                </li>
                <li className="flex items-center">
                  <div className="w-8 h-8 rounded-full bg-green-100 flex items-center justify-center text-green-600 mr-3">
                    <i className="fas fa-check"></i>
                  </div>
                  <span>Water Quality</span>
                </li>
              </ul>
            </div>
          </motion.div>
        </div>
      </div>
    </section>
  );
};

export default Predict;