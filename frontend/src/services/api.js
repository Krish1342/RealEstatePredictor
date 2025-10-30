import axios from "axios";

const API_BASE_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    "Content-Type": "application/json",
  },
  timeout: 30000, // 30 seconds
});

// Request interceptor
api.interceptors.request.use(
  (config) => {
    // You can add authentication tokens here if needed
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response) {
      // Server responded with error
      console.error("API Error:", error.response.data);
    } else if (error.request) {
      // Request made but no response
      console.error("Network Error:", error.message);
    } else {
      // Something else happened
      console.error("Error:", error.message);
    }
    return Promise.reject(error);
  }
);

// API functions
export const healthCheck = async () => {
  try {
    const response = await api.get("/health");
    return response.data;
  } catch (error) {
    throw error;
  }
};

export const predictPrice = async (propertyData) => {
  try {
    const response = await api.post("/predict", propertyData);
    return response.data;
  } catch (error) {
    throw error;
  }
};

export const getModelsInfo = async () => {
  try {
    const response = await api.get("/models");
    return response.data;
  } catch (error) {
    throw error;
  }
};

export const getFeatures = async () => {
  try {
    const response = await api.get("/features");
    return response.data;
  } catch (error) {
    throw error;
  }
};

export default api;
