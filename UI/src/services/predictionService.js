// API service for connecting to FastAPI backend
const API_BASE_URL = "http://localhost:8000";

class PredictionService {
  async healthCheck() {
    try {
      const response = await fetch(`${API_BASE_URL}/health`);
      return await response.json();
    } catch (error) {
      console.error("Health check failed:", error);
      throw error;
    }
  }

  async getAvailableModels() {
    try {
      const response = await fetch(`${API_BASE_URL}/models`);
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      return await response.json();
    } catch (error) {
      console.error("Failed to fetch models:", error);
      throw error;
    }
  }

  async predictPrice(propertyData) {
    try {
      const response = await fetch(`${API_BASE_URL}/predict`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          location: propertyData.location || "",
          area: parseFloat(propertyData.area) || 1000,
          bedrooms: parseInt(propertyData.bedrooms) || 2,
          bathrooms: parseInt(propertyData.bathrooms) || 2,
          age: parseInt(propertyData.age) || 5,
          furnished: propertyData.furnished || false,
          amenities: propertyData.amenities || {},
        }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(
          errorData.detail || `HTTP error! status: ${response.status}`
        );
      }

      return await response.json();
    } catch (error) {
      console.error("Prediction failed:", error);
      throw error;
    }
  }

  async getModelSummary() {
    try {
      const response = await fetch(`${API_BASE_URL}/summary`);
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      return await response.json();
    } catch (error) {
      console.error("Failed to fetch model summary:", error);
      throw error;
    }
  }

  // Helper method to format currency
  formatCurrency(amount) {
    return new Intl.NumberFormat("en-IN", {
      style: "currency",
      currency: "INR",
      minimumFractionDigits: 0,
      maximumFractionDigits: 0,
    }).format(amount);
  }

  // Helper method to validate property data
  validatePropertyData(data) {
    const errors = [];

    if (!data.location || data.location.trim() === "") {
      errors.push("Location is required");
    }

    if (
      !data.area ||
      isNaN(parseFloat(data.area)) ||
      parseFloat(data.area) <= 0
    ) {
      errors.push("Valid area is required");
    }

    if (
      !data.bedrooms ||
      isNaN(parseInt(data.bedrooms)) ||
      parseInt(data.bedrooms) <= 0
    ) {
      errors.push("Valid number of bedrooms is required");
    }

    if (
      !data.bathrooms ||
      isNaN(parseInt(data.bathrooms)) ||
      parseInt(data.bathrooms) <= 0
    ) {
      errors.push("Valid number of bathrooms is required");
    }

    return {
      isValid: errors.length === 0,
      errors,
    };
  }
}

// Create and export singleton instance
const predictionService = new PredictionService();
export default predictionService;
