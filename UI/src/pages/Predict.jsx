import React, { useState, useEffect } from "react";
import { motion } from "framer-motion";
import FreeMapComponent from "../components/FreeMapComponent";
import FreeLocationSearch from "../components/FreeLocationSearch";
import FactorImportance from "../components/FactorImportance";
import WhatIfScenarios from "../components/WhatIfScenarios";
import POIDisplay from "../components/POIDisplay";
import predictionService from "../services/predictionService";

const Predict = () => {
  const [formData, setFormData] = useState({
    location: "",
    area: "",
    bedrooms: "",
    bathrooms: "",
    age: "",
    amenities: {
      parking: false,
      garden: false,
      pool: false,
      gym: false,
    },
  });

  const [prediction, setPrediction] = useState(null);
  const [loading, setLoading] = useState(false);
  const [selectedLocation, setSelectedLocation] = useState("");
  const [showFactors, setShowFactors] = useState(false);
  const [scenarioImpact, setScenarioImpact] = useState(null);
  const [showAmenities, setShowAmenities] = useState(false);
  const [models, setModels] = useState([]);
  const [apiError, setApiError] = useState(null);
  const [apiStatus, setApiStatus] = useState("checking");

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  const handleLocationChange = (value) => {
    setFormData((prev) => ({
      ...prev,
      location: value,
    }));
    setSelectedLocation(value);
  };

  const handleLocationSelect = (suggestion) => {
    setSelectedLocation(suggestion);
  };

  const handleCheckboxChange = (e) => {
    const { name, checked } = e.target;
    setFormData((prev) => ({
      ...prev,
      amenities: {
        ...prev.amenities,
        [name]: checked,
      },
    }));
  };

  const handleScenarioChange = (scenario) => {
    setScenarioImpact(scenario);
  };

  // Check API health and load models on component mount
  useEffect(() => {
    const initializeAPI = async () => {
      try {
        setApiStatus("checking");
        await predictionService.healthCheck();
        const modelsData = await predictionService.getAvailableModels();
        setModels(modelsData.models || []);
        setApiStatus("connected");
        setApiError(null);
      } catch (error) {
        console.error("API initialization failed:", error);
        setApiError(error.message);
        setApiStatus("disconnected");
      }
    };

    initializeAPI();
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();

    // Validate form data
    const validation = predictionService.validatePropertyData(formData);
    if (!validation.isValid) {
      setApiError(
        "Please fix the following errors: " + validation.errors.join(", ")
      );
      return;
    }

    setLoading(true);
    setApiError(null);

    try {
      const result = await predictionService.predictPrice(formData);

      // Transform the FastAPI response to match the existing UI expectations
      setPrediction({
        price: result.formatted_price,
        accuracy: result.confidence,
        factors: result.insights,
        location: formData.location,
        individual_predictions: result.individual_predictions,
        prediction_range: result.prediction_range,
        model_summary: result.model_summary,
        ensemble_prediction: result.ensemble_prediction,
      });
    } catch (error) {
      console.error("Prediction error:", error);
      setApiError(`Prediction failed: ${error.message}`);
      setPrediction(null);
    } finally {
      setLoading(false);
    }
  };

  return (
    <section className="py-16 px-6">
      <div className="container mx-auto">
        <h2 className="text-3xl font-bold text-center mb-4">
          Predict Property Price
        </h2>
        <p className="text-gray-600 text-center max-w-2xl mx-auto mb-8">
          Our advanced algorithm analyzes multiple factors to provide accurate
          property valuation
        </p>

        {/* API Status Indicator */}
        <div className="flex justify-center mb-8">
          <div
            className={`px-4 py-2 rounded-full text-sm font-medium ${
              apiStatus === "connected"
                ? "bg-green-100 text-green-800"
                : apiStatus === "checking"
                ? "bg-yellow-100 text-yellow-800"
                : "bg-red-100 text-red-800"
            }`}
          >
            {apiStatus === "connected" && (
              <>
                <i className="fas fa-check-circle mr-2"></i>
                AI Models Connected ({models.length} models loaded)
              </>
            )}
            {apiStatus === "checking" && (
              <>
                <i className="fas fa-spinner fa-spin mr-2"></i>
                Connecting to AI Models...
              </>
            )}
            {apiStatus === "disconnected" && (
              <>
                <i className="fas fa-exclamation-triangle mr-2"></i>
                AI Models Offline
              </>
            )}
          </div>
        </div>

        {/* Error Display */}
        {apiError && (
          <div className="bg-red-50 border border-red-200 rounded-lg p-4 mb-8 mx-auto max-w-2xl">
            <div className="flex items-center">
              <i className="fas fa-exclamation-circle text-red-500 mr-2"></i>
              <span className="text-red-700">{apiError}</span>
            </div>
          </div>
        )}

        <div className="grid lg:grid-cols-2 gap-10">
          {/* Left Column - Form */}
          <motion.div
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.5, delay: 0.2 }}
            className="prediction-form p-8"
          >
            <form onSubmit={handleSubmit}>
              <div className="mb-6">
                <label
                  className="block text-gray-700 mb-2 font-medium"
                  htmlFor="location"
                >
                  Location
                </label>
                <FreeLocationSearch
                  value={formData.location}
                  onChange={handleLocationChange}
                  onLocationSelect={handleLocationSelect}
                />
                <p className="text-xs text-gray-500 mt-1">
                  Start typing to see location suggestions
                </p>
              </div>

              <div className="grid grid-cols-2 gap-6 mb-6">
                <div>
                  <label
                    className="block text-gray-700 mb-2 font-medium"
                    htmlFor="area"
                  >
                    Area (sq. ft.)
                  </label>
                  <input
                    type="number"
                    id="area"
                    name="area"
                    value={formData.area}
                    onChange={handleChange}
                    className="input-field w-full px-4 py-3"
                    placeholder="e.g., 1500"
                    required
                  />
                </div>
                <div>
                  <label
                    className="block text-gray-700 mb-2 font-medium"
                    htmlFor="bedrooms"
                  >
                    Bedrooms
                  </label>
                  <select
                    id="bedrooms"
                    name="bedrooms"
                    value={formData.bedrooms}
                    onChange={handleChange}
                    className="input-field w-full px-4 py-3"
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
                  <label
                    className="block text-gray-700 mb-2 font-medium"
                    htmlFor="bathrooms"
                  >
                    Bathrooms
                  </label>
                  <select
                    id="bathrooms"
                    name="bathrooms"
                    value={formData.bathrooms}
                    onChange={handleChange}
                    className="input-field w-full px-4 py-3"
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
                  <label
                    className="block text-gray-700 mb-2 font-medium"
                    htmlFor="age"
                  >
                    Property Age (years)
                  </label>
                  <input
                    type="number"
                    id="age"
                    name="age"
                    value={formData.age}
                    onChange={handleChange}
                    className="input-field w-full px-4 py-3"
                    placeholder="e.g., 5"
                    required
                  />
                </div>
              </div>

              <div className="mb-8">
                <label className="block text-gray-700 mb-2 font-medium">
                  Property Amenities
                </label>
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
                ) : (
                  "Predict Price"
                )}
              </button>
            </form>
          </motion.div>

          {/* Right Column - Results & Features */}
          <motion.div
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.5, delay: 0.4 }}
            className="space-y-6"
          >
            {/* Map Section */}
            <div className="bg-white rounded-2xl shadow-xl p-6">
              <h3 className="text-xl font-bold text-gray-800 mb-4">
                Property Location
              </h3>
              <FreeMapComponent location={selectedLocation} height="300px" />
              {selectedLocation && (
                <div className="mt-4 p-3 bg-blue-50 rounded-lg">
                  <div className="flex items-center">
                    <i className="fas fa-map-marker-alt text-blue-500 mr-2"></i>
                    <p className="text-sm text-blue-700">
                      Location:{" "}
                      <span className="font-medium">{selectedLocation}</span>
                    </p>
                  </div>
                  <p className="text-xs text-blue-600 mt-1">
                    <i className="fas fa-info-circle mr-1"></i>
                    Interactive map powered by OpenStreetMap
                  </p>
                </div>
              )}
            </div>

            {/* POI Display Section */}
            {selectedLocation && (
              <div className="bg-white rounded-2xl shadow-xl p-6">
                <div className="flex justify-between items-center mb-4">
                  <h3 className="text-xl font-bold text-gray-800">
                    Nearby Amenities
                  </h3>
                  <button
                    onClick={() => setShowAmenities(!showAmenities)}
                    className="px-4 py-2 bg-indigo-600 text-white rounded-lg font-medium hover:bg-indigo-700 transition"
                  >
                    {showAmenities ? "Hide Amenities" : "Show Amenities"}
                  </button>
                </div>
                <POIDisplay
                  location={selectedLocation}
                  isVisible={showAmenities}
                />
              </div>
            )}

            {/* Factor Importance */}
            <FactorImportance isVisible={showFactors} />

            {/* Prediction Result */}
            {loading ? (
              <div className="result-card p-8 text-center fade-in">
                <div className="text-center py-8">
                  <div className="loading-dots mb-4">
                    <span></span>
                    <span></span>
                    <span></span>
                  </div>
                  <h3 className="text-xl font-bold">Analyzing Property Data</h3>
                  <p className="mt-2">
                    Our top 5 AI models are processing your request...
                  </p>
                </div>
              </div>
            ) : prediction ? (
              <div className="space-y-6">
                {/* Main Prediction Card */}
                <div className="result-card p-8 text-center fade-in">
                  <button
                    onClick={() => setShowFactors(!showFactors)}
                    className="mb-4 px-4 py-2 bg-white bg-opacity-20 rounded-lg text-white font-medium hover:bg-opacity-30 transition"
                  >
                    {showFactors ? "Hide Analysis" : "Show Price Factors"}
                  </button>

                  <h3 className="text-2xl font-bold mb-4">
                    Ensemble Prediction
                  </h3>
                  <div className="text-4xl font-bold mb-4">
                    {scenarioImpact
                      ? `₹${Math.round(prediction.ensemble_prediction * 1.15)}`
                      : prediction.price}
                  </div>
                  {scenarioImpact && (
                    <div className="mb-4 p-3 bg-yellow-500 bg-opacity-20 rounded-lg">
                      <p className="text-yellow-200 text-sm">
                        <i className="fas fa-lightbulb mr-1"></i>
                        With {scenarioImpact.title}: +{scenarioImpact.impact}
                      </p>
                    </div>
                  )}
                  <div className="price-badge inline-block text-sm font-semibold">
                    {prediction.accuracy} Accuracy
                  </div>

                  {/* Prediction Range */}
                  {prediction.prediction_range && (
                    <div className="mt-4 p-3 bg-blue-500 bg-opacity-20 rounded-lg">
                      <p className="text-blue-200 text-sm">
                        <i className="fas fa-chart-line mr-1"></i>
                        Range: {
                          prediction.prediction_range.formatted_min
                        } - {prediction.prediction_range.formatted_max}
                      </p>
                    </div>
                  )}

                  <div className="mt-6">
                    <h4 className="font-medium mb-3">AI Insights</h4>
                    <ul className="space-y-2">
                      {prediction.factors.map((factor, index) => (
                        <li
                          key={index}
                          className="flex items-center justify-center"
                        >
                          <svg
                            className="h-5 w-5 text-green-300 mr-2"
                            fill="currentColor"
                            viewBox="0 0 20 20"
                            xmlns="http://www.w3.org/2000/svg"
                          >
                            <path
                              fillRule="evenodd"
                              d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z"
                              clipRule="evenodd"
                            />
                          </svg>
                          <span>{factor}</span>
                        </li>
                      ))}
                    </ul>
                  </div>
                </div>

                {/* Individual Model Predictions */}
                {prediction.individual_predictions &&
                  prediction.individual_predictions.length > 0 && (
                    <div className="bg-white rounded-2xl shadow-xl p-6">
                      <h4 className="text-xl font-bold text-gray-800 mb-4">
                        Individual Model Predictions
                      </h4>
                      <div className="grid gap-4">
                        {prediction.individual_predictions.map(
                          (model, index) => (
                            <div
                              key={index}
                              className="flex justify-between items-center p-3 bg-gray-50 rounded-lg"
                            >
                              <div className="flex items-center">
                                <div className="w-3 h-3 bg-indigo-500 rounded-full mr-3"></div>
                                <span className="font-medium text-gray-700">
                                  {model.name}
                                </span>
                              </div>
                              <div className="text-right">
                                <div className="font-bold text-gray-900">
                                  {model.formatted_price}
                                </div>
                              </div>
                            </div>
                          )
                        )}
                      </div>
                    </div>
                  )}

                {/* Model Summary */}
                {prediction.model_summary &&
                  prediction.model_summary.summary && (
                    <div className="bg-white rounded-2xl shadow-xl p-6">
                      <h4 className="text-xl font-bold text-gray-800 mb-4">
                        AI Analysis Summary
                      </h4>
                      <div className="prose max-w-none">
                        <div className="text-gray-700 whitespace-pre-line">
                          {prediction.model_summary.summary}
                        </div>

                        {prediction.model_summary.recommendations &&
                          prediction.model_summary.recommendations.length >
                            0 && (
                            <div className="mt-4">
                              <h5 className="font-semibold text-gray-800 mb-2">
                                Recommendations:
                              </h5>
                              <ul className="space-y-1">
                                {prediction.model_summary.recommendations.map(
                                  (rec, index) => (
                                    <li
                                      key={index}
                                      className="flex items-start"
                                    >
                                      <i className="fas fa-lightbulb text-yellow-500 mr-2 mt-1"></i>
                                      <span className="text-gray-700">
                                        {rec}
                                      </span>
                                    </li>
                                  )
                                )}
                              </ul>
                            </div>
                          )}
                      </div>
                    </div>
                  )}
              </div>
            ) : (
              <div className="result-card p-8 text-center fade-in">
                <div className="flex flex-col items-center justify-center h-64 text-center">
                  <div className="mb-4 p-3 bg-indigo-100 rounded-full bg-opacity-20">
                    <i className="fas fa-home text-white text-4xl"></i>
                  </div>
                  <h3 className="text-xl font-bold mb-1">No Prediction Yet</h3>
                  <p className="text-white text-opacity-80">
                    Fill out the form to get an accurate price estimation using
                    our top 5 AI models.
                  </p>
                  {apiStatus === "connected" && (
                    <p className="text-white text-opacity-60 text-sm mt-2">
                      {models.length} models ready for prediction
                    </p>
                  )}
                </div>
              </div>
            )}

            {/* What-If Scenarios */}
            {prediction && !loading && (
              <WhatIfScenarios
                currentPrediction={prediction}
                onScenarioChange={handleScenarioChange}
              />
            )}

            {/* Factors Considered */}
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
                <li className="flex items-center">
                  <div className="w-8 h-8 rounded-full bg-green-100 flex items-center justify-center text-green-600 mr-3">
                    <i className="fas fa-check"></i>
                  </div>
                  <span>Location & Neighborhood</span>
                </li>
                <li className="flex items-center">
                  <div className="w-8 h-8 rounded-full bg-green-100 flex items-center justify-center text-green-600 mr-3">
                    <i className="fas fa-check"></i>
                  </div>
                  <span>Nearby Amenities & Facilities</span>
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
