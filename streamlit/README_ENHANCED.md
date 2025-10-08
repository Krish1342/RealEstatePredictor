# 🏠 Professional Real Estate AI Predictor

A state-of-the-art machine learning application for predicting real estate prices in Bangalore using multiple AI models and real-time environmental data.

## 🌟 Features

### 🤖 Advanced AI Models

- **5 Top-Performing Models**: Extra Trees, Random Forest, LightGBM, Decision Tree, and Weighted Average Ensemble
- **99.99%+ Accuracy**: Trained on 18,000+ Bangalore properties
- **Ensemble Predictions**: Get predictions from all models for maximum reliability

### 🌍 Real-Time Data Integration

- **OpenWeather API**: Live air quality and weather data
- **Environmental Scoring**: Air quality impact on property values
- **Dynamic Pricing**: Weather-adjusted price predictions

### 💎 Professional Interface

- **Modern UI**: Clean, responsive design with gradient themes
- **Interactive Visualizations**: Plotly-powered charts and insights
- **Model Performance**: Real-time accuracy metrics display
- **Detailed Analysis**: Comprehensive property insights

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- OpenWeather API Key (free from [openweathermap.org](https://openweathermap.org/api))

### Installation

1. **Clone or navigate to the project directory**

   ```bash
   cd RealEsatePredictor/streamlit
   ```

2. **Install dependencies**

   ```bash
   pip install -r enhanced_requirements.txt
   ```

3. **Launch the application**

   ```bash
   python launch_app.py
   ```

   Or directly with Streamlit:

   ```bash
   streamlit run professional_app.py
   ```

4. **Open your browser** to `http://localhost:8501`

## 📊 Model Performance

| Model            | R² Score | RMSE  | MAE   | Training Time |
| ---------------- | -------- | ----- | ----- | ------------- |
| Extra Trees      | 0.999999 | 1,005 | 131   | 0.64s         |
| Weighted Average | 0.999999 | 1,647 | 209   | -             |
| Random Forest    | 0.999999 | 1,867 | 263   | 1.35s         |
| Decision Tree    | 0.999998 | 3,253 | 339   | 0.25s         |
| LightGBM         | 0.999992 | 6,988 | 1,677 | 0.40s         |

## 🏡 Input Features

### Primary Features (Most Important)

- **Total Area**: Property size in square feet
- **Bedrooms/Bathrooms**: Number of rooms
- **Location Type**: Prime Area, City Center, Developing Area, Suburban
- **Property Age**: Calculated from year built
- **Furnishing Status**: Unfurnished, Semi-furnished, Fully furnished

### Environmental Features (Real-time)

- **Air Quality Index (AQI)**: Current air pollution levels
- **PM2.5 & PM10**: Fine particulate matter concentrations
- **NO₂, O₃, CO**: Gas pollutant levels
- **Environmental Score**: Composite health index

### Location & Amenities

- **Floor Number**: Property floor level
- **Parking Spaces**: Number of parking spots
- **Property Facing**: Direction orientation
- **Public Transport**: Accessibility rating
- **Security Level**: Property security features

## 🎯 How It Works

### 1. Data Collection

The app collects input from two sources:

- **User Input**: Property specifications and preferences
- **OpenWeather API**: Real-time environmental data for Bangalore

### 2. Feature Engineering

- Calculates derived features (price per sqft, area per bedroom, property age)
- Applies location popularity scoring
- Integrates environmental impact metrics
- Normalizes and scales all features

### 3. Model Prediction

- Processes data through all 5 trained models
- Applies ensemble weighting for final predictions
- Calculates confidence intervals and variance metrics

### 4. Results Display

- Shows individual model predictions
- Provides summary statistics and insights
- Displays interactive visualizations
- Offers property-specific recommendations

## 📈 API Integration

### OpenWeather API Setup

1. Visit [OpenWeather API](https://openweathermap.org/api)
2. Sign up for a free account
3. Generate an API key
4. Enter the key in the sidebar of the app

### Environmental Data Used

- **Current Weather**: Temperature, humidity, pressure
- **Air Pollution**: AQI, PM2.5, PM10, NO₂, O₃, CO, NH₃
- **Location**: Bangalore coordinates (12.9716°N, 77.5946°E)

## 🔧 Technical Architecture

### File Structure

```
streamlit/
├── professional_app.py          # Main application
├── production_model_handler.py  # Model loading and prediction logic
├── launch_app.py               # Application launcher
├── enhanced_requirements.txt   # Dependencies
└── README_ENHANCED.md         # This file
```

### Key Components

#### `ProfessionalRealEstateApp`

- Main application class
- Handles UI rendering and user interactions
- Manages API calls and data processing

#### `ProductionModelHandler`

- Model loading and management
- Feature engineering pipeline
- Prediction generation and ensemble methods

### Data Flow

1. **Input Collection** → User form + Weather API
2. **Preprocessing** → Feature engineering + scaling
3. **Prediction** → All 5 models + ensemble
4. **Visualization** → Charts + insights + recommendations

## 🎨 UI Features

### Modern Design Elements

- **Gradient Headers**: Eye-catching color schemes
- **Interactive Cards**: Hover effects and animations
- **Responsive Layout**: Works on desktop and mobile
- **Professional Typography**: Clean, readable fonts

### Visualizations

- **Model Comparison**: Bar charts comparing predictions
- **Price Distribution**: Pie charts showing model contributions
- **Performance Metrics**: Real-time accuracy displays
- **Property Insights**: Comprehensive analysis panels

## 🔍 Model Details

### Training Data

- **18,000+ Properties**: Comprehensive Bangalore dataset
- **80+ Features**: Engineered from raw property data
- **Multiple Sources**: Property listings, environmental data, location metrics

### Feature Importance (Top 10)

1. Price_numeric (58.6%)
2. Price_numeric_log (25.4%)
3. Price_encoded (6.5%)
4. Price_per_SQFT (2.7%)
5. Total_Area (2.7%)
6. Property Title_encoded (1.3%)
7. Baths (1.3%)
8. Balcony_encoded (0.3%)
9. Name_encoded (0.3%)
10. location_encoded (0.2%)

## 🚀 Performance Optimization

### Speed Enhancements

- **Lazy Loading**: Models loaded once at startup
- **Caching**: Streamlit caching for repeated operations
- **Async API Calls**: Non-blocking weather data fetching
- **Optimized Visualizations**: Efficient Plotly rendering

### Memory Management

- **Model Compression**: Optimized pickle files
- **Feature Selection**: Only most important features used
- **Data Streaming**: Efficient data processing pipeline

## 🛠️ Customization

### Adding New Models

1. Save model as `.pkl` file in `ensemble_learning/saved_models/`
2. Update `ProductionModelHandler.model_files` mapping
3. Add performance metrics to `get_model_performance()`

### Modifying Features

1. Update `create_feature_vector()` in `ProductionModelHandler`
2. Adjust input form in `create_input_form()`
3. Update feature importance display

### Styling Changes

1. Modify CSS in the `st.markdown()` style section
2. Update color schemes in visualization functions
3. Adjust layout in `st.columns()` configurations

## 📱 Usage Examples

### Basic Prediction

1. Enter property details (area, rooms, location)
2. Select furnishing and amenities
3. Click "Generate AI Price Predictions"
4. View results from all 5 models

### With Weather Data

1. Add OpenWeather API key in sidebar
2. View live Bangalore environmental data
3. Generate weather-adjusted predictions
4. See environmental impact analysis

### Advanced Analysis

1. Explore model comparison charts
2. Review property insights and recommendations
3. Analyze price per square foot metrics
4. Compare with market segments

## 🔧 Troubleshooting

### Common Issues

**Models not loading**

- Ensure `ensemble_learning/saved_models/` directory exists
- Check that `.pkl` files are present and accessible
- Verify Python has read permissions

**Weather API errors**

- Validate API key at openweathermap.org
- Check internet connectivity
- Ensure API key has sufficient quota

**Performance issues**

- Clear Streamlit cache: `streamlit cache clear`
- Restart the application
- Check system memory usage

### Error Messages

**"Production model handler not found"**

- Ensure `production_model_handler.py` is in the same directory
- Check file permissions and Python path

**"Weather API request timed out"**

- Check internet connection
- Try refreshing the page
- App will use default values automatically

## 🤝 Contributing

### Development Setup

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

### Code Standards

- Follow PEP 8 style guidelines
- Add docstrings to all functions
- Include type hints where possible
- Write comprehensive tests

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- **Scikit-learn**: Machine learning framework
- **Streamlit**: Web application framework
- **Plotly**: Interactive visualizations
- **OpenWeather**: Real-time environmental data
- **Bangalore Open Data**: Property and location datasets

## 📞 Support

For support, questions, or feature requests:

- Open an issue on GitHub
- Contact the development team
- Check the troubleshooting section above

---

**Made with ❤️ for the Bangalore real estate market**
