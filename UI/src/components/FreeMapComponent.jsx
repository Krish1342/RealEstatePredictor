import React, { useState, useEffect } from 'react';
import { MapContainer, TileLayer, Marker, Popup, useMap } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';
import L from 'leaflet';

// Fix for default markers in react-leaflet
delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon-2x.png',
  iconUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon.png',
  shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-shadow.png',
});

// Component to update map center when location changes
function MapUpdater({ center }) {
  const map = useMap();
  useEffect(() => {
    map.setView(center, 13);
  }, [center, map]);
  return null;
}

const FreeMapComponent = ({ location, height = '400px' }) => {
  const [coordinates, setCoordinates] = useState([12.9716, 77.5946]); // Default: Bangalore
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  // Geocode the location using OpenStreetMap Nominatim API
  useEffect(() => {
    if (!location) return;

    const geocodeLocation = async () => {
      setLoading(true);
      setError(null);
      
      try {
        const response = await fetch(
          `https://nominatim.openstreetmap.org/search?format=json&q=${encodeURIComponent(location)}&limit=1`
        );
        const data = await response.json();
        
        if (data && data.length > 0) {
          const { lat, lon } = data[0];
          setCoordinates([parseFloat(lat), parseFloat(lon)]);
        } else {
          setError('Location not found');
          // Fallback to Bangalore coordinates
          setCoordinates([12.9716, 77.5946]);
        }
      } catch (err) {
        setError('Failed to geocode location');
        console.error('Geocoding error:', err);
      } finally {
        setLoading(false);
      }
    };

    // Add delay to avoid too many API calls
    const timeoutId = setTimeout(geocodeLocation, 1000);
    return () => clearTimeout(timeoutId);
  }, [location]);

  if (!location) {
    return (
      <div className="bg-gray-100 rounded-lg flex items-center justify-center" style={{ height }}>
        <div className="text-center text-gray-500">
          <i className="fas fa-map-marker-alt text-3xl mb-2"></i>
          <p>Enter a location to see the map</p>
        </div>
      </div>
    );
  }

  if (loading) {
    return (
      <div className="bg-gray-100 rounded-lg flex items-center justify-center" style={{ height }}>
        <div className="text-center text-gray-500">
          <div className="loading-dots mb-2">
            <span></span>
            <span></span>
            <span></span>
          </div>
          <p>Finding location...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="rounded-lg overflow-hidden shadow-lg" style={{ height }}>
      <MapContainer 
        center={coordinates} 
        zoom={13} 
        style={{ height: '100%', width: '100%' }}
        scrollWheelZoom={false}
      >
        <MapUpdater center={coordinates} />
        <TileLayer
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />
        <Marker position={coordinates}>
          <Popup>
            <div className="p-2">
              <h3 className="font-bold text-gray-800">Property Location</h3>
              <p className="text-sm text-gray-600">{location}</p>
              <p className="text-xs text-gray-500 mt-1">
                📍 {coordinates[0].toFixed(4)}, {coordinates[1].toFixed(4)}
              </p>
              {error && (
                <p className="text-xs text-red-500 mt-1">
                  <i className="fas fa-exclamation-triangle mr-1"></i>
                  {error}
                </p>
              )}
            </div>
          </Popup>
        </Marker>
      </MapContainer>
    </div>
  );
};

export default FreeMapComponent;