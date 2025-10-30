/**
 * Free Geocoding Service using OpenStreetMap Nominatim
 * No API key required - 100% FREE!
 * Rate limit: 1 request/second (fair use policy)
 */

const NOMINATIM_BASE = "https://nominatim.openstreetmap.org";

// Delay helper to respect rate limit
const delay = (ms) => new Promise((resolve) => setTimeout(resolve, ms));

let lastRequestTime = 0;

/**
 * Geocode an address to coordinates
 * @param {string} address - The address to geocode
 * @param {string} city - City name (default: Bangalore)
 * @param {string} country - Country name (default: India)
 * @returns {Promise<{lat: number, lon: number, displayName: string}|null>}
 */
export const geocodeAddress = async (
  address,
  city = "Bangalore",
  country = "India"
) => {
  try {
    // Respect rate limit (1 request per second)
    const now = Date.now();
    const timeSinceLastRequest = now - lastRequestTime;
    if (timeSinceLastRequest < 1000) {
      await delay(1000 - timeSinceLastRequest);
    }
    lastRequestTime = Date.now();

    const query = `${address}, ${city}, ${country}`;
    const response = await fetch(
      `${NOMINATIM_BASE}/search?` +
        new URLSearchParams({
          q: query,
          format: "json",
          limit: 1,
          addressdetails: 1,
        }),
      {
        headers: {
          "User-Agent": "RealEstatePredictorApp/1.0", // Required by Nominatim
        },
      }
    );

    const data = await response.json();

    if (data && data.length > 0) {
      return {
        lat: parseFloat(data[0].lat),
        lon: parseFloat(data[0].lon),
        displayName: data[0].display_name,
        address: data[0].address,
      };
    }

    return null;
  } catch (error) {
    console.error("Geocoding error:", error);
    return null;
  }
};

/**
 * Reverse geocode coordinates to address
 * @param {number} lat - Latitude
 * @param {number} lon - Longitude
 * @returns {Promise<object|null>}
 */
export const reverseGeocode = async (lat, lon) => {
  try {
    // Respect rate limit
    const now = Date.now();
    const timeSinceLastRequest = now - lastRequestTime;
    if (timeSinceLastRequest < 1000) {
      await delay(1000 - timeSinceLastRequest);
    }
    lastRequestTime = Date.now();

    const response = await fetch(
      `${NOMINATIM_BASE}/reverse?` +
        new URLSearchParams({
          lat: lat.toString(),
          lon: lon.toString(),
          format: "json",
          addressdetails: 1,
        }),
      {
        headers: {
          "User-Agent": "RealEstatePredictorApp/1.0",
        },
      }
    );

    const data = await response.json();
    return data.address || null;
  } catch (error) {
    console.error("Reverse geocoding error:", error);
    return null;
  }
};

/**
 * Pre-defined coordinates for popular Bangalore locations
 * Instant lookup without API calls
 */
export const bangaloreLocations = {
  Koramangala: [12.9352, 77.6245],
  Indiranagar: [12.9784, 77.6408],
  Whitefield: [12.9698, 77.75],
  "Electronic City": [12.8456, 77.6603],
  "HSR Layout": [12.9121, 77.6446],
  "BTM Layout": [12.9165, 77.6101],
  Jayanagar: [12.925, 77.5838],
  Malleshwaram: [13.0039, 77.5727],
  Marathahalli: [12.9591, 77.7011],
  Hebbal: [13.0358, 77.597],
  Yelahanka: [13.1007, 77.5963],
  Banashankari: [12.925, 77.5482],
  "JP Nagar": [12.9078, 77.585],
  Bellandur: [12.926, 77.6747],
  "Sarjapur Road": [12.901, 77.6874],
};

/**
 * Get coordinates for a location
 * Uses pre-defined coordinates first, falls back to geocoding if needed
 */
export const getLocationCoordinates = async (location) => {
  // Check pre-defined locations first (instant, no API call)
  if (bangaloreLocations[location]) {
    return {
      lat: bangaloreLocations[location][0],
      lon: bangaloreLocations[location][1],
      source: "predefined",
    };
  }

  // Fall back to geocoding API if not in predefined list
  const result = await geocodeAddress(location);
  if (result) {
    return {
      lat: result.lat,
      lon: result.lon,
      source: "geocoded",
    };
  }

  // Default to Bangalore city center if all else fails
  return {
    lat: 12.9716,
    lon: 77.5946,
    source: "default",
  };
};
