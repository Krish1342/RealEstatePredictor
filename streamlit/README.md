# 🏠 Real Estate Price Predictor - Streamlit Application

A comprehensive AI-powered real estate price prediction system with an interactive Streamlit dashboard.

## 🚀 Features

- **AI-Powered Price Prediction**: Multiple machine learning models for accurate price estimation
- **Interactive Dashboard**: Comprehensive data exploration and visualization
- **Model Performance Analysis**: Compare and analyze different ML models
- **Feature Importance Analysis**: Understand what drives property prices
- **Environmental Factors**: Integration of air quality and noise data
- **Location Intelligence**: Location-based pricing insights

## 📊 Models Included

- Extra Trees Regressor (Best performing with 99.99%+ accuracy)
- Random Forest Regressor
- Gradient Boosting
- XGBoost
- LightGBM
- Decision Trees
- Ensemble methods (Voting, Stacking, Bagging)

## 🏗️ Architecture

### Data Pipeline

1. **Data Collection**: Multiple datasets (housing, air quality, noise, location)
2. **Preprocessing**: Cleaning, feature engineering, encoding
3. **Integration**: Merging datasets with location-based matching
4. **Feature Engineering**: Creating derived features and interactions
5. **Model Training**: Ensemble learning with cross-validation
6. **Deployment**: Streamlit web application

### Project Structure

```
streamlit/
├── app.py                 # Main Streamlit application
├── data_utils.py         # Data preprocessing utilities
├── prediction_utils.py   # Model prediction and visualization
├── test_app.py          # Comprehensive testing suite
├── run_app.py           # Simple launcher script
├── requirements.txt     # Python dependencies
└── README.md           # This file
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- All datasets in the correct directory structure
- Trained models in `../ensemble_learning/saved_models/`

### Installation

1. Navigate to the streamlit directory:

   ```bash
   cd RealEstatePredictor/streamlit
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Run tests to verify setup:

   ```bash
   python test_app.py
   ```

4. Launch the application:
   ```bash
   streamlit run app.py
   ```

### Alternative Launch Methods

```bash
# Using the launcher script
streamlit run run_app.py

# Direct Python execution
python -m streamlit run app.py
```

## 📱 Using the Application

### 🏠 Dashboard

- Overview of system performance
- Quick statistics and insights
- Model performance summary

### 🔮 Price Prediction

1. Enter property details (BHK, size, location features)
2. Specify environmental factors (AQI, noise levels)
3. Select prediction model
4. Get instant price prediction with confidence intervals
5. View feature impact analysis and recommendations

### 📊 Model Analysis

- Compare performance of all trained models
- View R² scores, RMSE, and other metrics
- Analyze model training times
- Cross-validation results

### 📈 Data Exploration

- Interactive visualization of datasets
- Statistical summaries and distributions
- Correlation analysis
- Missing data analysis

### 🎯 Feature Analysis

- Feature importance rankings
- Categorical analysis of feature types
- Cumulative importance charts
- Feature correlation with target variables

## 🎯 Key Features

### Smart Input Handling

- Automatic feature completion for missing values
- Intelligent defaults based on training data
- Real-time validation and error handling

### Advanced Visualizations

- Interactive Plotly charts
- Multiple chart types (bar, scatter, heatmap, treemap)
- Responsive design for different screen sizes

### Model Intelligence

- Automatic model selection based on performance
- Confidence intervals for predictions
- Feature impact analysis for individual predictions

### Data Integration

- Seamless handling of multiple data sources
- Automatic preprocessing and feature engineering
- Real-time data validation

## 🔧 Configuration

### Environment Variables

The application automatically detects and loads:

- Dataset paths from `../datasets/`
- Preprocessed data from `../preprocessed_data/`
- Feature engineered data from `../feature_engineering/`
- Trained models from `../ensemble_learning/saved_models/`

### Customization

- Modify `data_utils.py` for custom preprocessing
- Update `prediction_utils.py` for new visualization components
- Extend `app.py` for additional dashboard features

## 🧪 Testing

Run the comprehensive test suite:

```bash
python test_app.py
```

Tests include:

- ✅ Library imports verification
- ✅ Data availability checks
- ✅ Model loading validation
- ✅ Prediction pipeline testing
- ✅ Data integrity verification

## 📊 Performance Metrics

- **Best Model**: Extra Trees Regressor
- **Accuracy**: R² > 0.9999
- **Prediction Speed**: < 100ms per prediction
- **Features**: 80+ engineered features
- **Data Points**: 20,000+ property records

## 🚨 Troubleshooting

### Common Issues

1. **Models not loading**

   - Ensure ensemble learning has been run
   - Check `../ensemble_learning/saved_models/` directory
   - Verify sklearn version compatibility

2. **Data not found**

   - Confirm all datasets are in `../datasets/`
   - Run preprocessing notebooks first
   - Check file paths in error messages

3. **Prediction errors**

   - Verify feature compatibility
   - Check input data types
   - Run test_app.py for diagnostics

4. **Import errors**
   - Install missing packages: `pip install -r requirements.txt`
   - Check Python version compatibility
   - Verify virtual environment activation

### Performance Optimization

- Use cached data loading with `@st.cache_data`
- Limit large dataset operations
- Optimize visualization rendering
- Use efficient data structures

## 🛠️ Development

### Adding New Features

1. Create utility functions in appropriate modules
2. Add UI components in `app.py`
3. Update tests in `test_app.py`
4. Document changes in README

### Model Integration

1. Train models using ensemble learning pipeline
2. Save models in `../ensemble_learning/saved_models/`
3. Update model loading logic in `prediction_utils.py`
4. Test with `test_app.py`

## 📈 Future Enhancements

- Real-time data updates
- Advanced filtering and search
- Export functionality for reports
- Mobile-responsive design improvements
- API integration for external data sources
- Automated model retraining

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Add comprehensive tests
4. Submit pull request with documentation

## 📄 License

This project is part of the Real Estate Predictor system. See main project LICENSE file.

## 🙏 Acknowledgments

- Streamlit for the excellent web framework
- Plotly for interactive visualizations
- Scikit-learn and ensemble learning libraries
- The open-source Python data science community

---

**Happy Predicting! 🏠✨**
