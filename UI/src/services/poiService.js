// Free Points of Interest Service using OpenStreetMap
class POIService {
  // Search for specific types of places near a location
  async searchNearby(location, placeType, limit = 5) {
    try {
      const query = this.getQueryForType(placeType, location);
      const response = await fetch(
        `https://nominatim.openstreetmap.org/search?q=${encodeURIComponent(query)}&format=json&limit=${limit}`
      );
      
      if (!response.ok) {
        throw new Error('Failed to fetch POI data');
      }
      
      const data = await response.json();
      return this.formatPOIData(data, placeType);
    } catch (error) {
      console.error('POI Search Error:', error);
      return [];
    }
  }

  // Get query string based on place type
  getQueryForType(placeType, location) {
    const typeMap = {
      school: 'school',
      hospital: 'hospital',
      park: 'park',
      shopping: 'shopping mall',
      supermarket: 'supermarket',
      metro: 'metro station',
      restaurant: 'restaurant',
      bank: 'bank',
      pharmacy: 'pharmacy'
    };

    const typeQuery = typeMap[placeType] || placeType;
    return `${typeQuery} in ${location}`;
  }

  // Format the raw API data into a consistent structure
  formatPOIData(data, placeType) {
    return data.map(item => ({
      id: item.place_id,
      name: item.display_name.split(',')[0], // Get the first part as name
      address: item.display_name,
      type: placeType,
      latitude: parseFloat(item.lat),
      longitude: parseFloat(item.lon),
      importance: item.importance,
      category: this.getCategory(placeType),
      icon: this.getIconForType(placeType)
    }));
  }

  // Categorize places for scoring
  getCategory(placeType) {
    const categories = {
      school: 'education',
      hospital: 'healthcare',
      park: 'recreation',
      shopping: 'shopping',
      supermarket: 'shopping',
      metro: 'transport',
      restaurant: 'dining',
      bank: 'services',
      pharmacy: 'healthcare'
    };
    return categories[placeType] || 'other';
  }

  // Get FontAwesome icons for each place type
  getIconForType(placeType) {
    const icons = {
      school: 'fas fa-school',
      hospital: 'fas fa-hospital',
      park: 'fas fa-tree',
      shopping: 'fas fa-shopping-cart',
      supermarket: 'fas fa-store',
      metro: 'fas fa-subway',
      restaurant: 'fas fa-utensils',
      bank: 'fas fa-university',
      pharmacy: 'fas fa-prescription-bottle'
    };
    return icons[placeType] || 'fas fa-map-marker-alt';
  }

  // Get all important POIs for a location
  async getAllPOIs(location) {
    const types = ['school', 'hospital', 'park', 'shopping', 'metro', 'supermarket'];
    
    try {
      const promises = types.map(type => this.searchNearby(location, type, 3));
      const results = await Promise.all(promises);
      
      // Flatten and sort by importance
      const allPOIs = results.flat();
      return allPOIs.sort((a, b) => b.importance - a.importance);
    } catch (error) {
      console.error('Error fetching all POIs:', error);
      return [];
    }
  }

  // Calculate amenity score based on POI density and importance
  calculateAmenityScore(pois) {
    if (!pois.length) return 0;
    
    const categoryCount = {};
    let totalScore = 0;
    
    pois.forEach(poi => {
      categoryCount[poi.category] = (categoryCount[poi.category] || 0) + 1;
      totalScore += poi.importance * 10; // Scale importance to 0-10
    });
    
    const uniqueCategories = Object.keys(categoryCount).length;
    const averageImportance = totalScore / pois.length;
    
    // Score formula: based on variety and quality of amenities
    const score = Math.min(10, (uniqueCategories * 1.5) + (averageImportance * 0.8));
    return Math.round(score * 10) / 10; // Round to 1 decimal
  }
}

export default new POIService();