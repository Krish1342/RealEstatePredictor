# 🏠 Real Estate Predictor - Full Stack AI Application

A comprehensive real estate price prediction system using ensemble machine learning models with FastAPI backend and React frontend.

## 🌟 Features

### 🤖 AI-Powered Predictions

- **Ensemble Learning**: Top 5 machine learning models working together (Extra Trees, Random Forest, Decision Tree, LightGBM, XGBoost)
- **Real-time Predictions**: Instant property valuations with confidence scores
- **Model Transparency**: Individual model predictions and explanations
- **99.99% Accuracy**: R² score across ensemble models

### 🎯 Advanced Analytics

- **Performance Metrics**: R², MAE, RMSE scores for each model
- **Prediction Confidence**: Dynamic confidence scoring based on model agreement
- **Smart Insights**: AI-generated recommendations and market analysis
- **Comparative Analysis**: Range predictions and variance analysis

### 🖥️ Modern UI/UX

- **React Frontend**: Modern, responsive user interface built with React 18 and Vite
- **Interactive Charts**: Beautiful data visualizations with Recharts
- **Real-time Status**: Live API connection monitoring
- **Mobile Friendly**: Fully responsive design for all devices

## 🏗️ Architecture

### Backend (FastAPI)

- **FastAPI**: High-performance Python web framework
- **Scikit-learn**: Machine learning model pipeline
- **Ensemble Models**: Extra Trees (40%), Random Forest (25%), Decision Tree (15%), LightGBM (15%), XGBoost (5%)
- **RESTful API**: Clean, documented endpoints with auto-generated Swagger docs

### Frontend (React + Vite)

- **React 18**: Modern component-based UI
- **Vite**: Lightning-fast build tool and development server
- **Tailwind CSS**: Utility-first styling framework
- **Framer Motion**: Smooth animations and transitions
- **Recharts**: Interactive data visualizations

### Machine Learning Pipeline

```
Input Data → Feature Engineering → Model Ensemble → Weighted Predictions → Insights + Results
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- Node.js 16 or higher
- Windows OS (for batch scripts) or bash compatible shell

### Option 1: Automated Setup (Windows - Recommended)

```powershell
# Clone the repository
git clone <your-repo-url>
cd RealEstatePredictor

# Run the automated setup script
start_system.bat
```

This will:

- Start the FastAPI backend on port 8000
- Start the React frontend on port 5173
- Open both in separate command windows

### Option 2: Manual Setup

#### Backend Setup

```powershell
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment (Windows)
.\venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Start the FastAPI server
python main.py
```

#### Frontend Setup

```powershell
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

### 🌐 Access Points

- **Frontend Application**: http://localhost:5173
- **Backend API**: http://localhost:8000
- **API Documentation (Swagger)**: http://localhost:8000/docs
- **API Documentation (ReDoc)**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health

## 📊 Model Performance

Our ensemble uses the top 5 performing models:

| Model         | R² Score | MAE     | RMSE      | Weight |
| ------------- | -------- | ------- | --------- | ------ |
| Extra Trees   | 0.999999 | 130.67  | 1,004.53  | 40%    |
| Random Forest | 0.999999 | 262.83  | 1,866.99  | 25%    |
| Decision Tree | 0.999998 | 338.73  | 3,252.90  | 15%    |
| LightGBM      | 0.999992 | 1677.42 | 6,988.41  | 15%    |
| XGBoost       | 0.999942 | 7009.06 | 18,394.10 | 5%     |

## 🔧 API Usage

### Predict Property Price

```javascript
// Example API call using fetch
const prediction = await fetch("http://localhost:8000/predict", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({
    BHK: 3,
    Size_in_SqFt: 1500,
    Year_Built: 2015,
    Floor_No: 5,
    Total_Floors: 15,
    Nearby_Schools: 3,
    Nearby_Hospitals: 2,
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
  }),
});

const result = await prediction.json();
console.log(result.formatted_price); // ₹72.50 Lakhs
```

### Response Structure

```json
{
  "ensemble_prediction": 7250000.0,
  "formatted_price": "₹72.50 Lakhs",
  "confidence": "92.5%",
  "individual_predictions": [
    {
      "name": "Extra Trees",
      "prediction": 7100000.0,
      "formatted_price": "₹71.00 Lakhs",
      "weight": 40,
      "metrics": {
        "R2": 0.999999,
        "MAE": 130.67,
        "RMSE": 1004.53
      }
    }
  ],
  "insights": [
    "🏡 Large property size - Premium segment pricing",
    "📍 Location: Koramangala - Premium Bangalore area",
    "🚗 Parking available - Essential in Bangalore"
  ],
  "prediction_range": {
    "min": 6800000.0,
    "max": 7500000.0,
    "formatted_min": "₹68.00 Lakhs",
    "formatted_max": "₹75.00 Lakhs",
    "std_dev": 125000.0
  },
  "feature_importance": [
    { "feature": "Price_numeric", "importance": 0.5859 },
    { "feature": "Price_numeric_log", "importance": 0.2536 }
  ],
  "model_performance": {
    "total_models": 5,
    "average_r2": 0.999998,
    "best_model": "Extra Trees"
  }
}
```

## 📁 Project Structure

```
RealEstatePredictor/
├── backend/                    # FastAPI backend
│   ├── main.py                # Main FastAPI application
│   ├── requirements.txt       # Python dependencies
│   └── README.md             # Backend documentation
├── frontend/                  # React frontend
│   ├── src/
│   │   ├── components/       # React components
│   │   │   ├── Navbar.jsx
│   │   │   ├── Footer.jsx
│   │   │   └── PredictionResult.jsx
│   │   ├── pages/           # Page components
│   │   │   ├── Home.jsx
│   │   │   ├── Predict.jsx
│   │   │   ├── Analytics.jsx
│   │   │   └── About.jsx
│   │   ├── services/        # API services
│   │   │   └── api.js
│   │   ├── App.jsx          # Main app component
│   │   ├── main.jsx         # Entry point
│   │   └── index.css        # Global styles
│   ├── package.json         # Node.js dependencies
│   ├── vite.config.js       # Vite configuration
│   ├── tailwind.config.js   # Tailwind configuration
│   └── README.md           # Frontend documentation
├── ensemble_learning/        # ML models and training
│   ├── saved_models/        # Trained model files
│   │   ├── extra_trees_model.pkl
│   │   ├── random_forest_model.pkl
│   │   ├── decision_tree_model.pkl
│   │   ├── lightgbm_model.pkl
│   │   ├── xgboost_model.pkl
│   │   ├── ensemble_learning_results.csv
│   │   └── feature_importance.csv
│   └── ensemble_learning.ipynb
├── datasets/                # Training datasets
│   └── [various data files]
├── feature_engineering/     # Feature engineering pipeline
│   └── feature_engineered_expert.csv
├── models/                  # Additional models
├── preprocessing/           # Data preprocessing notebooks
├── start_system.bat        # Start both servers (Windows)
├── start_backend.bat       # Start backend only (Windows)
├── start_frontend.bat      # Start frontend only (Windows)
└── README.md              # This file
```

## 🔍 Features in Detail

### Frontend Pages

1. **Home Page**

   - Hero section with gradient background
   - Feature showcase with icons
   - Statistics display (models, accuracy, features)
   - How it works section
   - Call-to-action buttons

2. **Predict Page**

   - Comprehensive property input form
   - Real-time form validation
   - Prediction results with:
     - Main predicted price
     - Confidence score
     - Price range (min/max)
     - AI-generated insights
     - Individual model predictions
     - Feature importance charts
     - Model performance summary

3. **Analytics Page**

   - Model performance metrics
   - R² score comparison charts
   - MAE and RMSE visualizations
   - Ensemble weight distribution
   - Multi-dimensional radar charts
   - Detailed metrics table

4. **About Page**
   - Project mission and vision
   - Technology stack details
   - Model performance table
   - Dataset information
   - Call-to-action section

### Backend Endpoints

- `GET /` - Root endpoint with API info
- `GET /health` - Health check with model status
- `POST /predict` - Property price prediction
- `GET /models` - Model information and metrics
- `GET /features` - List of all features used

### Prediction Features

The system analyzes 70+ features including:

- **Property Details**: BHK, size, year built, floor details
- **Location**: Area, nearby amenities, accessibility
- **Amenities**: Furnished status, parking, balcony, security
- **Environmental**: Air quality, noise levels (placeholders for API integration)
- **Derived Features**: Price per sqft, area per bedroom, age of property
- **Encoded Features**: All categorical variables properly encoded

## 🚀 Deployment

### Development

Both frontend and backend include hot-reload for development:

- **Backend**: `--reload` flag enabled in uvicorn
- **Frontend**: Vite dev server with HMR (Hot Module Replacement)

### Production

#### Backend Deployment

```powershell
# Using waitress (Windows) or gunicorn (Linux)
pip install waitress
waitress-serve --listen=0.0.0.0:8000 main:app
```

#### Frontend Deployment

```powershell
cd frontend
npm run build
# Deploy the 'dist' folder to:
# - Vercel
# - Netlify
# - AWS S3
# - GitHub Pages
# - Any static hosting service
```

### Environment Variables

#### Backend (.env)

```env
API_HOST=0.0.0.0
API_PORT=8000
MODEL_DIR=../ensemble_learning/saved_models
```

#### Frontend (.env)

```env
VITE_API_URL=http://localhost:8000
```

## 📊 Data & Models

### Dataset Information

- **Total Records**: 21,388+ verified property records
- **Location**: Bangalore, India
- **Features**: 70+ engineered features
- **Target**: Property price in INR

### Feature Engineering

Key engineered features:

- Price per square foot
- Area per bedroom
- Bath to bedroom ratio
- Age of property
- Location popularity
- Environmental scores
- Log transformations
- Interaction terms

### Model Training

Models were trained using:

- Cross-validation
- Feature importance analysis
- Hyperparameter tuning
- Ensemble weighting based on performance

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Troubleshooting

### Common Issues

**Backend won't start:**

- Check Python version (3.8+)
- Verify model files exist in `ensemble_learning/saved_models/`
- Check dependency installation: `pip list`
- Ensure port 8000 is not in use

**Frontend won't connect:**

- Ensure backend is running on port 8000
- Check CORS configuration in backend
- Verify API URL in frontend `.env` file
- Clear browser cache

**Prediction errors:**

- Validate input data format
- Check all required fields are filled
- Review backend logs for errors
- Ensure models are loaded correctly

**Module not found errors:**

- Backend: `pip install -r backend/requirements.txt`
- Frontend: `cd frontend && npm install`

### Port Conflicts

If ports 8000 or 5173 are already in use:

**Backend (change in main.py):**

```python
uvicorn.run(app, host="0.0.0.0", port=8001)  # Change port
```

**Frontend (change in vite.config.js):**

```javascript
server: {
  port: 3000; // Change port
}
```

### Getting Help

1. Check the README files in `backend/` and `frontend/`
2. Review API documentation at http://localhost:8000/docs
3. Check server logs for error details
4. Open an issue on GitHub with:
   - Error message
   - Steps to reproduce
   - System information (OS, Python/Node version)

## 🎯 Future Enhancements

- [ ] Real-time environmental data integration (Air Quality API, Noise API)
- [ ] Interactive map integration for location selection
- [ ] Historical price trend analysis
- [ ] Neighborhood comparison features
- [ ] Investment ROI calculator
- [ ] Property recommendation system
- [ ] User authentication and saved predictions
- [ ] Export predictions to PDF/Excel
- [ ] Mobile app development
- [ ] Multi-city support beyond Bangalore

## 🔑 API Keys (Free Tier)

For real-time environmental data integration, you can use these free APIs:

1. **Air Quality**:

   - OpenWeatherMap Air Pollution API (Free tier: 1000 calls/day)
   - IQAir (Free tier: 100 calls/month)

2. **Location Data**:
   - Google Maps Geocoding API (Free $200/month credit)
   - Mapbox (Free 50,000 requests/month)

To integrate, add to backend `.env`:

```env
OPENWEATHER_API_KEY=your_key_here
GOOGLE_MAPS_API_KEY=your_key_here
```

---

**Built with ❤️ using FastAPI, React, and Ensemble Machine Learning**

For more information, visit:

- **Backend Documentation**: [backend/README.md](backend/README.md)
- **Frontend Documentation**: [frontend/README.md](frontend/README.md)
- **API Documentation**: http://localhost:8000/docs (when running)
