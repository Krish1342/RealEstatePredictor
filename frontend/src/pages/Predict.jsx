import { useEffect, useState } from "react";
import { motion } from "framer-motion";
import toast from "react-hot-toast";
import { Loader2, Home, DollarSign, TrendingUp, MapPin } from "lucide-react";
import { predictPrice, healthCheck } from "../services/api";
import PredictionResult from "../components/PredictionResult";
import LocationMap from "../components/LocationMap";
import { bangaloreLocations } from "../services/geocoding";

const Predict = () => {
  const [loading, setLoading] = useState(false);
  const [prediction, setPrediction] = useState(null);
  const [health, setHealth] = useState({ status: "loading", models_loaded: 0 });
  const [formData, setFormData] = useState({
    BHK: 2,
    Size_in_SqFt: 1000,
    Year_Built: 2015,
    Floor_No: 3,
    Total_Floors: 10,
    Nearby_Schools: 2,
    Nearby_Hospitals: 1,
    Furnished_Status: "Semi-Furnished",
    Public_Transport_Accessibility: "Good",
    Parking_Space: "Yes",
    Security: "Yes",
    Availability_Status: "Ready to Move",
    Baths: 2,
    balcony: "Yes",
    location: "Koramangala",
    Property_Type: "Apartment",
    Facing: "East",
    Owner_Type: "Primary",
  });

  const bangaloreLocationsList = [
    "Koramangala",
    "Indiranagar",
    "Whitefield",
    "Electronic City",
    "HSR Layout",
    "BTM Layout",
    "Jayanagar",
    "Malleshwaram",
    "Marathahalli",
    "Hebbal",
    "Yelahanka",
    "Banashankari",
    "JP Nagar",
    "Bellandur",
    "Sarjapur Road",
  ];

  const handleChange = (e) => {
    const { name, value, type } = e.target;
    setFormData({
      ...formData,
      [name]: type === "number" ? parseFloat(value) : value,
    });
  };

  // Poll backend health to avoid 503 predictions while models load
  useEffect(() => {
    let timerId;

    const poll = async () => {
      try {
        const data = await healthCheck();
        setHealth({ status: data.status, models_loaded: data.models_loaded });
      } catch (err) {
        // If backend is unreachable, mark as unhealthy
        setHealth((h) => ({ ...h, status: "unhealthy" }));
      }
    };

    // Initial check and then every 2s
    poll();
    timerId = setInterval(poll, 2000);
    return () => clearInterval(timerId);
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (health.status !== "healthy") {
      toast("Models are still loading. Please wait a few seconds…", {
        icon: "⏳",
      });
      return;
    }
    setLoading(true);
    setPrediction(null);

    try {
      const result = await predictPrice(formData);
      setPrediction(result);
      toast.success("Prediction generated successfully!");
      // Scroll to results
      setTimeout(() => {
        document.getElementById("prediction-results")?.scrollIntoView({
          behavior: "smooth",
          block: "start",
        });
      }, 100);
    } catch (error) {
      console.error("Prediction error:", error);
      const detail = error?.response?.data?.detail;
      if (error?.response?.status === 503 && typeof detail === "string") {
        toast(detail);
        // Kick off a fresh health check soon
        setTimeout(async () => {
          try {
            const data = await healthCheck();
            setHealth({
              status: data.status,
              models_loaded: data.models_loaded,
            });
          } catch (_) {}
        }, 1500);
      } else {
        toast.error("Failed to generate prediction. Please try again.");
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 py-12">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          className="text-center mb-12"
        >
          <h1 className="text-4xl md:text-5xl font-bold text-gray-900 mb-4">
            Property Price Predictor
          </h1>
          <p className="text-xl text-gray-600">
            Enter property details to get AI-powered price predictions
          </p>
        </motion.div>

        {/* Health banner */}
        {health.status !== "healthy" && (
          <motion.div
            initial={{ opacity: 0, y: -10 }}
            animate={{ opacity: 1, y: 0 }}
            className="max-w-4xl mx-auto mb-6"
          >
            <div className="flex items-start gap-3 p-4 rounded-lg border bg-amber-50 border-amber-200 text-amber-900">
              <Loader2 className="w-5 h-5 mt-0.5 animate-spin" />
              <div>
                <p className="font-medium">Models are loading…</p>
                <p className="text-sm text-amber-800">
                  The backend is warming up the ML models. This typically takes
                  a few seconds. Status:{" "}
                  <span className="font-semibold">{health.status}</span>
                  {" · "}Loaded: {health.models_loaded}
                </p>
              </div>
            </div>
          </motion.div>
        )}

        {/* Form */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
          className="card max-w-4xl mx-auto mb-12"
        >
          <form onSubmit={handleSubmit} className="space-y-6">
            {/* Basic Information */}
            <div>
              <h2 className="text-2xl font-bold text-gray-900 mb-4 flex items-center">
                <Home className="w-6 h-6 mr-2 text-primary-600" />
                Basic Information
              </h2>
              <div className="grid md:grid-cols-2 gap-6">
                <div>
                  <label className="label">Property Type</label>
                  <select
                    name="Property_Type"
                    value={formData.Property_Type}
                    onChange={handleChange}
                    className="input-field"
                    required
                  >
                    <option value="Apartment">Apartment</option>
                    <option value="Villa">Villa</option>
                    <option value="House">House</option>
                    <option value="Penthouse">Penthouse</option>
                  </select>
                </div>

                <div>
                  <label className="label">Location</label>
                  <select
                    name="location"
                    value={formData.location}
                    onChange={handleChange}
                    className="input-field"
                    required
                  >
                    {bangaloreLocationsList.map((loc) => (
                      <option key={loc} value={loc}>
                        {loc}
                      </option>
                    ))}
                  </select>
                </div>

                <div>
                  <label className="label">BHK (Bedrooms)</label>
                  <input
                    type="number"
                    name="BHK"
                    min="1"
                    max="10"
                    value={formData.BHK}
                    onChange={handleChange}
                    className="input-field"
                    required
                  />
                </div>

                <div>
                  <label className="label">Bathrooms</label>
                  <input
                    type="number"
                    name="Baths"
                    min="1"
                    max="10"
                    value={formData.Baths}
                    onChange={handleChange}
                    className="input-field"
                    required
                  />
                </div>

                <div>
                  <label className="label">Size (Sq. Ft.)</label>
                  <input
                    type="number"
                    name="Size_in_SqFt"
                    min="100"
                    step="10"
                    value={formData.Size_in_SqFt}
                    onChange={handleChange}
                    className="input-field"
                    required
                  />
                </div>

                <div>
                  <label className="label">Year Built</label>
                  <input
                    type="number"
                    name="Year_Built"
                    min="1950"
                    max="2025"
                    value={formData.Year_Built}
                    onChange={handleChange}
                    className="input-field"
                    required
                  />
                </div>
              </div>
            </div>

            {/* Floor Details */}
            <div>
              <h2 className="text-2xl font-bold text-gray-900 mb-4">
                Floor Details
              </h2>
              <div className="grid md:grid-cols-3 gap-6">
                <div>
                  <label className="label">Floor Number</label>
                  <input
                    type="number"
                    name="Floor_No"
                    min="0"
                    max="50"
                    value={formData.Floor_No}
                    onChange={handleChange}
                    className="input-field"
                    required
                  />
                </div>

                <div>
                  <label className="label">Total Floors</label>
                  <input
                    type="number"
                    name="Total_Floors"
                    min="1"
                    max="50"
                    value={formData.Total_Floors}
                    onChange={handleChange}
                    className="input-field"
                    required
                  />
                </div>

                <div>
                  <label className="label">Facing</label>
                  <select
                    name="Facing"
                    value={formData.Facing}
                    onChange={handleChange}
                    className="input-field"
                    required
                  >
                    <option value="North">North</option>
                    <option value="South">South</option>
                    <option value="East">East</option>
                    <option value="West">West</option>
                    <option value="North-East">North-East</option>
                    <option value="South-East">South-East</option>
                  </select>
                </div>
              </div>
            </div>

            {/* Amenities */}
            <div>
              <h2 className="text-2xl font-bold text-gray-900 mb-4">
                Amenities & Features
              </h2>
              <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
                <div>
                  <label className="label">Furnished Status</label>
                  <select
                    name="Furnished_Status"
                    value={formData.Furnished_Status}
                    onChange={handleChange}
                    className="input-field"
                    required
                  >
                    <option value="Unfurnished">Unfurnished</option>
                    <option value="Semi-Furnished">Semi-Furnished</option>
                    <option value="Furnished">Furnished</option>
                    <option value="Fully Furnished">Fully Furnished</option>
                  </select>
                </div>

                <div>
                  <label className="label">Parking Space</label>
                  <select
                    name="Parking_Space"
                    value={formData.Parking_Space}
                    onChange={handleChange}
                    className="input-field"
                    required
                  >
                    <option value="Yes">Yes</option>
                    <option value="No">No</option>
                  </select>
                </div>

                <div>
                  <label className="label">Balcony</label>
                  <select
                    name="balcony"
                    value={formData.balcony}
                    onChange={handleChange}
                    className="input-field"
                    required
                  >
                    <option value="Yes">Yes</option>
                    <option value="No">No</option>
                  </select>
                </div>

                <div>
                  <label className="label">Security</label>
                  <select
                    name="Security"
                    value={formData.Security}
                    onChange={handleChange}
                    className="input-field"
                    required
                  >
                    <option value="Yes">Yes</option>
                    <option value="No">No</option>
                  </select>
                </div>

                <div>
                  <label className="label">Public Transport</label>
                  <select
                    name="Public_Transport_Accessibility"
                    value={formData.Public_Transport_Accessibility}
                    onChange={handleChange}
                    className="input-field"
                    required
                  >
                    <option value="Poor">Poor</option>
                    <option value="Fair">Fair</option>
                    <option value="Good">Good</option>
                    <option value="Excellent">Excellent</option>
                  </select>
                </div>

                <div>
                  <label className="label">Availability</label>
                  <select
                    name="Availability_Status"
                    value={formData.Availability_Status}
                    onChange={handleChange}
                    className="input-field"
                    required
                  >
                    <option value="Ready to Move">Ready to Move</option>
                    <option value="Under Construction">
                      Under Construction
                    </option>
                    <option value="Almost Ready">Almost Ready</option>
                  </select>
                </div>
              </div>
            </div>

            {/* Nearby Facilities */}
            <div>
              <h2 className="text-2xl font-bold text-gray-900 mb-4">
                Nearby Facilities
              </h2>
              <div className="grid md:grid-cols-3 gap-6">
                <div>
                  <label className="label">Nearby Schools</label>
                  <input
                    type="number"
                    name="Nearby_Schools"
                    min="0"
                    max="20"
                    value={formData.Nearby_Schools}
                    onChange={handleChange}
                    className="input-field"
                  />
                </div>

                <div>
                  <label className="label">Nearby Hospitals</label>
                  <input
                    type="number"
                    name="Nearby_Hospitals"
                    min="0"
                    max="20"
                    value={formData.Nearby_Hospitals}
                    onChange={handleChange}
                    className="input-field"
                  />
                </div>

                <div>
                  <label className="label">Owner Type</label>
                  <select
                    name="Owner_Type"
                    value={formData.Owner_Type}
                    onChange={handleChange}
                    className="input-field"
                    required
                  >
                    <option value="Primary">Primary</option>
                    <option value="Secondary">Secondary</option>
                    <option value="Tertiary">Tertiary</option>
                  </select>
                </div>
              </div>
            </div>

            {/* Submit Button */}
            <div className="flex justify-center pt-6">
              <button
                type="submit"
                disabled={loading || health.status !== "healthy"}
                className="btn-primary px-12 py-4 text-lg flex items-center space-x-2"
              >
                {loading ? (
                  <>
                    <Loader2 className="w-5 h-5 animate-spin" />
                    <span>Predicting...</span>
                  </>
                ) : health.status !== "healthy" ? (
                  <>
                    <Loader2 className="w-5 h-5 animate-spin" />
                    <span>Models warming up…</span>
                  </>
                ) : (
                  <>
                    <TrendingUp className="w-5 h-5" />
                    <span>Predict Price</span>
                  </>
                )}
              </button>
            </div>
          </form>
        </motion.div>

        {/* Prediction Results */}
        {prediction && (
          <div id="prediction-results">
            <PredictionResult data={prediction} />

            {/* Location Map */}
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.3 }}
              className="card mt-8"
            >
              <h3 className="text-2xl font-bold text-gray-900 mb-4 flex items-center">
                <MapPin className="w-6 h-6 mr-2 text-primary-600" />
                Property Location
              </h3>
              <LocationMap
                location={formData.location}
                position={
                  bangaloreLocations[formData.location] || [12.9716, 77.5946]
                }
              />
              <div className="mt-4 p-4 bg-blue-50 rounded-lg border border-blue-100">
                <p className="text-sm text-gray-700">
                  <strong>📍 Location:</strong> {formData.location}, Bangalore
                </p>
                <p className="text-xs text-gray-500 mt-1">
                  Map powered by OpenStreetMap - 100% free and open source
                </p>
              </div>
            </motion.div>
          </div>
        )}
      </div>
    </div>
  );
};

export default Predict;
