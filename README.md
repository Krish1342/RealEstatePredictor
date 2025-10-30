# 🏠 Real Estate Predictor - Full Stack AI Application

A comprehensive real estate price prediction system using ensemble machine learning models with FastAPI backend and React frontend, enhanced with LangGraph for intelligent analysis and summarization.

## 🌟 Features

### 🤖 AI-Powered Predictions

- **Ensemble Learning**: Top 5 machine learning models working together
- **LangGraph Integration**: Intelligent analysis workflow for smart insights
- **Real-time Predictions**: Instant property valuations with confidence scores
- **Model Transparency**: Individual model predictions and explanations

### 🎯 Advanced Analytics

- **Performance Metrics**: R², MAE, RMSE scores for each model
- **Prediction Confidence**: Dynamic confidence scoring based on model agreement
- **Smart Insights**: AI-generated recommendations and market analysis
- **Comparative Analysis**: Range predictions and variance analysis

### 🖥️ Modern UI/UX

- **React Frontend**: Modern, responsive user interface
- **Interactive Maps**: Property location visualization
- **Real-time Status**: Live API connection monitoring
- **Mobile Friendly**: Responsive design for all devices

## 🏗️ Architecture

### Backend (FastAPI + LangGraph)

- **FastAPI**: High-performance Python web framework
- **LangGraph**: Workflow orchestration for AI analysis
- **Scikit-learn**: Machine learning model pipeline
- **Ensemble Models**: Extra Trees, Random Forest, Decision Tree, LightGBM, XGBoost

### Frontend (React + Vite)

- **React 19**: Modern component-based UI
- **Vite**: Fast build tool and development server
- **Tailwind CSS**: Utility-first styling framework
- **Framer Motion**: Smooth animations and transitions

### Machine Learning Pipeline

```
Input Data → Feature Engineering → Model Ensemble → LangGraph Analysis → Predictions + Insights
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- Node.js 16 or higher
- Git

### Option 1: Automated Setup (Windows)

```bash
# Clone the repository
git clone <your-repo-url>
cd RealEsatePredictor

# Run the automated setup script
start_system.bat
```

### Option 2: Manual Setup

#### Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac

# Install dependencies
pip install -r requirements.txt

# Start the FastAPI server
python start_server.py
```

#### Frontend Setup

```bash
# Navigate to UI directory
cd UI

# Install dependencies
npm install

# Start development server
npm run dev
```

### 🌐 Access Points

- **Frontend Application**: http://localhost:5173
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

## 📊 Model Performance

Our ensemble uses the top 5 performing models:

| Model                   | R² Score | MAE     | RMSE    | Weight |
| ----------------------- | -------- | ------- | ------- | ------ |
| Extra Trees             | 0.999999 | 130.67  | 1004.53 | 40%    |
| Random Forest           | 0.999999 | 262.83  | 1866.99 | 25%    |
| Decision Tree           | 0.999998 | 338.73  | 3252.90 | 15%    |
| LightGBM                | 0.999992 | 1677.42 | 6988.41 | 15%    |
| Alternative Extra Trees | -        | -       | -       | 5%     |

## 🔧 API Usage

### Predict Property Price

```javascript
// Example API call
const prediction = await fetch("http://localhost:8000/predict", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({
    location: "Bangalore, Koramangala",
    area: 1200.0,
    bedrooms: 3,
    bathrooms: 2,
    age: 5,
    furnished: true,
    amenities: {
      parking: true,
      garden: false,
      pool: true,
      gym: true,
    },
  }),
});

const result = await prediction.json();
console.log(result.formatted_price); // ₹72,50,000
```

### Response Structure

```json
{
  "ensemble_prediction": 7250000.0,
  "formatted_price": "₹72,50,000",
  "confidence": "89%",
  "individual_predictions": [
    {
      "name": "Extra Trees",
      "prediction": 7100000.0,
      "formatted_price": "₹71,00,000"
    }
  ],
  "insights": [
    "Large property size detected - premium pricing expected",
    "Bangalore location premium factor applied"
  ],
  "prediction_range": {
    "min": 6800000.0,
    "max": 7500000.0,
    "formatted_min": "₹68,00,000",
    "formatted_max": "₹75,00,000"
  },
  "model_summary": {
    "summary": "## Real Estate Price Prediction Analysis...",
    "recommendations": [
      "Consider luxury property features and premium locations",
      "Focus on high-end amenities and exclusivity factors"
    ]
  }
}
```

## 🧠 LangGraph Workflow

The system uses LangGraph to create an intelligent analysis workflow:

1. **Performance Analysis** - Analyzes model metrics and rankings
2. **Insight Generation** - Creates context-aware insights
3. **Summary Creation** - Generates comprehensive reports
4. **Recommendations** - Provides actionable advice

## 📁 Project Structure

```
RealEsatePredictor/
├── backend/                 # FastAPI backend
│   ├── fastapi_app.py      # Main application
│   ├── start_server.py     # Server launcher
│   ├── requirements.txt    # Python dependencies
│   └── README.md          # Backend documentation
├── UI/                     # React frontend
│   ├── src/
│   │   ├── components/    # React components
│   │   ├── pages/        # Page components
│   │   └── services/     # API services
│   ├── package.json      # Node.js dependencies
│   └── README.md        # Frontend documentation
├── ensemble_learning/     # ML models and training
│   ├── saved_models/     # Trained model files
│   └── ensemble_learning.ipynb
├── datasets/             # Training datasets
├── feature_engineering/  # Feature engineering pipeline
├── models/              # Additional models
├── preprocessing/       # Data preprocessing
├── streamlit/          # Streamlit app (alternative)
├── start_system.bat    # Windows startup script
└── README.md          # This file
```

## 🔍 Features in Detail

### Real-time Model Status

- Live monitoring of API connection
- Model loading status indicators
- Error handling and user feedback

### Intelligent Predictions

- Ensemble averaging with performance-based weights
- Confidence scoring based on model agreement
- Prediction ranges for uncertainty quantification

### Smart Insights

- Location-based analysis
- Property size recommendations
- Market trend considerations
- Amenity impact assessment

### Interactive UI

- Property location mapping
- Nearby amenities display
- What-if scenario analysis
- Responsive design for all devices

## 🚀 Deployment

### Development

Both frontend and backend include hot-reload for development:

- Backend: `--reload` flag enabled
- Frontend: Vite dev server with HMR

### Production

For production deployment:

1. **Backend**: Use gunicorn or similar WSGI server
2. **Frontend**: Build with `npm run build` and serve static files
3. **Models**: Ensure model files are accessible
4. **Environment**: Set appropriate environment variables

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

### Common Issues

**Backend won't start:**

- Check Python version (3.8+)
- Verify all model files exist
- Check dependency installation

**Frontend won't connect:**

- Ensure backend is running on port 8000
- Check CORS configuration
- Verify API endpoints

**Prediction errors:**

- Validate input data format
- Check model file integrity
- Review feature preprocessing

### Getting Help

1. Check the README files in backend/ and UI/
2. Review API documentation at /docs
3. Check server logs for error details
4. Open an issue on GitHub

## 🎯 Future Enhancements

- [ ] Real-time market data integration
- [ ] Advanced visualization dashboards
- [ ] Mobile app development
- [ ] Additional ML models
- [ ] Historical price trend analysis
- [ ] Neighborhood comparison features
- [ ] Investment ROI calculations
- [ ] Property recommendation system

---

**Built with ❤️ using FastAPI, React, and LangGraph**
