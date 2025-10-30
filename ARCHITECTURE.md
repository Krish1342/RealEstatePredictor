# 🏗️ Project Architecture & File Structure

## System Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                         USER BROWSER                             │
│                    http://localhost:5173                         │
└─────────────────────┬───────────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────────┐
│                    REACT FRONTEND (Vite)                         │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │   Home.jsx   │  │ Predict.jsx  │  │Analytics.jsx │          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
│  ┌──────────────────────────────────────────────────┐          │
│  │            API Service (Axios)                    │          │
│  └──────────────────────────────────────────────────┘          │
└─────────────────────┬───────────────────────────────────────────┘
                      │ HTTP POST/GET
                      ▼
┌─────────────────────────────────────────────────────────────────┐
│                   FASTAPI BACKEND                                │
│                http://localhost:8000                             │
│  ┌──────────────────────────────────────────────────┐          │
│  │              main.py (FastAPI App)                │          │
│  │  ├─ POST /predict                                 │          │
│  │  ├─ GET  /health                                  │          │
│  │  ├─ GET  /models                                  │          │
│  │  └─ GET  /features                                │          │
│  └──────────────────────────────────────────────────┘          │
│                       │                                          │
│                       ▼                                          │
│  ┌──────────────────────────────────────────────────┐          │
│  │         Model Loader & Predictor                  │          │
│  └──────────────────────────────────────────────────┘          │
└─────────────────────┬───────────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────────┐
│              ENSEMBLE ML MODELS (Scikit-learn)                   │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │ Extra Trees  │  │Random Forest │  │Decision Tree │          │
│  │  (40% wt)    │  │  (25% wt)    │  │  (15% wt)    │          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
│  ┌──────────────┐  ┌──────────────┐                            │
│  │  LightGBM    │  │   XGBoost    │                            │
│  │  (15% wt)    │  │   (5% wt)    │                            │
│  └──────────────┘  └──────────────┘                            │
└─────────────────────┬───────────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────────┐
│                      PREDICTION RESULT                           │
│  • Ensemble Prediction (weighted average)                       │
│  • Individual Model Predictions                                 │
│  • Confidence Score                                             │
│  • Price Range (min/max)                                        │
│  • AI-Generated Insights                                        │
│  • Feature Importance                                           │
└─────────────────────────────────────────────────────────────────┘
```

## File Structure Tree

```
RealEstatePredictor/
│
├── 📄 README.md                           # Main documentation
├── 📄 SETUP_GUIDE.md                      # Setup instructions
├── 📄 PROJECT_SUMMARY.md                  # Project overview
├── 📄 .gitignore                          # Git ignore rules
│
├── 🚀 start_system.bat                    # Start both servers
├── 🚀 start_backend.bat                   # Start backend only
├── 🚀 start_frontend.bat                  # Start frontend only
│
├── 📁 backend/                            # FastAPI Backend
│   ├── 📄 main.py                        # FastAPI application (600+ lines)
│   ├── 📄 requirements.txt               # Python dependencies
│   ├── 📄 README.md                      # Backend documentation
│   ├── 📄 .env.example                   # Environment variables template
│   └── 📁 venv/                          # Virtual environment (auto-created)
│
├── 📁 frontend/                           # React Frontend
│   ├── 📄 package.json                   # NPM dependencies & scripts
│   ├── 📄 vite.config.js                 # Vite configuration
│   ├── 📄 tailwind.config.js             # Tailwind CSS config
│   ├── 📄 postcss.config.js              # PostCSS config
│   ├── 📄 index.html                     # HTML entry point
│   ├── 📄 README.md                      # Frontend documentation
│   ├── 📄 .env.example                   # Environment variables template
│   │
│   ├── 📁 src/                           # Source code
│   │   ├── 📄 main.jsx                  # React entry point
│   │   ├── 📄 App.jsx                   # Main app component
│   │   ├── 📄 index.css                 # Global styles
│   │   │
│   │   ├── 📁 components/               # Reusable components
│   │   │   ├── 📄 Navbar.jsx           # Navigation bar
│   │   │   ├── 📄 Footer.jsx           # Footer
│   │   │   └── 📄 PredictionResult.jsx # Results display
│   │   │
│   │   ├── 📁 pages/                    # Page components
│   │   │   ├── 📄 Home.jsx             # Landing page
│   │   │   ├── 📄 Predict.jsx          # Prediction form
│   │   │   ├── 📄 Analytics.jsx        # Model analytics
│   │   │   └── 📄 About.jsx            # About page
│   │   │
│   │   └── 📁 services/                 # API services
│   │       └── 📄 api.js               # API integration
│   │
│   └── 📁 node_modules/                  # NPM packages (auto-created)
│
├── 📁 ensemble_learning/                 # ML Training & Models
│   ├── 📁 saved_models/                 # Trained model files
│   │   ├── 🤖 extra_trees_model.pkl
│   │   ├── 🤖 random_forest_model.pkl
│   │   ├── 🤖 decision_tree_model.pkl
│   │   ├── 🤖 lightgbm_model.pkl
│   │   ├── 🤖 xgboost_model.pkl
│   │   ├── 📊 feature_importance.csv
│   │   └── 📊 ensemble_learning_results.csv
│   │
│   └── 📓 ensemble_learning.ipynb       # Model training notebook
│
├── 📁 feature_engineering/              # Feature Engineering
│   ├── 📊 feature_engineered_expert.csv
│   └── 📓 feature_engineering.ipynb
│
├── 📁 datasets/                         # Training Data
│   ├── 📊 india_housing_prices.csv
│   ├── 📊 Bangalore.csv
│   ├── 📊 air_quality.csv
│   ├── 📊 noise_quality.csv
│   └── ... (other datasets)
│
├── 📁 preprocessing/                    # Data Preprocessing
│   ├── 📓 india_housing_prices.ipynb
│   ├── 📓 bangalore_preprocess.ipynb
│   └── ... (other notebooks)
│
├── 📁 models/                          # Additional Models
│   └── 📓 integration_model.ipynb
│
└── 📁 streamlit/                       # Alternative Streamlit UI
    └── ... (streamlit files)
```

## Data Flow Diagram

```
1. USER INPUT
   ↓
   Property Details Form (React)
   • BHK, Size, Location, Year Built, etc.
   • 18 input fields
   ↓

2. FORM VALIDATION
   ↓
   Client-side validation (React)
   • Required fields check
   • Value range validation
   ↓

3. API REQUEST
   ↓
   POST /predict (Axios)
   • JSON payload
   • Property features
   ↓

4. BACKEND PROCESSING
   ↓
   FastAPI Endpoint
   ├─ Parse & Validate (Pydantic)
   ├─ Feature Engineering
   │  ├─ Calculate age
   │  ├─ Encode categories
   │  ├─ Generate derived features
   │  └─ Create feature vector (70+ features)
   ├─ Model Prediction
   │  ├─ Extra Trees → Prediction 1
   │  ├─ Random Forest → Prediction 2
   │  ├─ Decision Tree → Prediction 3
   │  ├─ LightGBM → Prediction 4
   │  └─ XGBoost → Prediction 5
   ├─ Ensemble Calculation
   │  └─ Weighted Average (40%, 25%, 15%, 15%, 5%)
   └─ Generate Insights
      ├─ Size-based insights
      ├─ Location insights
      ├─ Amenity insights
      └─ Age insights
   ↓

5. API RESPONSE
   ↓
   JSON Response
   • Ensemble prediction
   • Individual predictions
   • Confidence score
   • Price range
   • Insights
   • Feature importance
   ↓

6. UI RENDERING
   ↓
   React Components
   ├─ Main Price Card
   ├─ Price Range Cards
   ├─ Insights List
   ├─ Model Comparison Chart (Recharts)
   ├─ Feature Importance Chart (Recharts)
   └─ Model Performance Summary
   ↓

7. USER INTERACTION
   ↓
   • View results
   • Scroll through visualizations
   • Print report
   • Make new prediction
```

## Component Hierarchy

```
App.jsx
├── Navbar.jsx (Always visible)
├── Routes
│   ├── Home.jsx (/)
│   │   ├── Hero Section
│   │   ├── Features Grid
│   │   ├── Stats Display
│   │   └── How It Works
│   │
│   ├── Predict.jsx (/predict)
│   │   ├── Property Form
│   │   │   ├── Basic Info Section
│   │   │   ├── Floor Details Section
│   │   │   ├── Amenities Section
│   │   │   └── Nearby Facilities Section
│   │   └── PredictionResult.jsx (conditional)
│   │       ├── Main Price Card
│   │       ├── Price Range Cards
│   │       ├── Insights Section
│   │       ├── Model Predictions Chart
│   │       ├── Feature Importance Chart
│   │       └── Performance Summary
│   │
│   ├── Analytics.jsx (/analytics)
│   │   ├── Stats Cards
│   │   ├── R² Comparison Chart
│   │   ├── MAE Chart
│   │   ├── Weights Chart
│   │   ├── Radar Chart
│   │   └── Metrics Table
│   │
│   └── About.jsx (/about)
│       ├── Mission Section
│       ├── Features Grid
│       ├── Technology Stack
│       ├── Performance Table
│       └── Dataset Info
│
└── Footer.jsx (Always visible)
```

## API Endpoint Structure

```
FastAPI Backend (main.py)
│
├── GET /
│   └── Returns: API welcome message
│
├── GET /health
│   └── Returns: {status, models_loaded, timestamp, version}
│
├── POST /predict
│   ├── Input: PropertyFeatures (Pydantic model)
│   │   └── 18 property attributes
│   ├── Processing:
│   │   ├── Feature preparation (70+ features)
│   │   ├── Model predictions (5 models)
│   │   ├── Ensemble calculation
│   │   └── Insight generation
│   └── Returns: PredictionResponse
│       ├── ensemble_prediction
│       ├── formatted_price
│       ├── confidence
│       ├── individual_predictions[]
│       ├── insights[]
│       ├── prediction_range{}
│       ├── feature_importance[]
│       └── model_performance{}
│
├── GET /models
│   └── Returns: {models[], total_models}
│
└── GET /features
    └── Returns: {features[], total_features}
```

## Technology Stack Layers

```
┌─────────────────────────────────────────┐
│         PRESENTATION LAYER              │
│  React 18 + Tailwind CSS + Recharts     │
│  • Components, Pages, Routing           │
│  • Responsive UI, Animations            │
└─────────────────┬───────────────────────┘
                  │
┌─────────────────▼───────────────────────┐
│          API LAYER                      │
│  FastAPI + Uvicorn                      │
│  • RESTful endpoints                    │
│  • Request validation                   │
│  • Error handling                       │
└─────────────────┬───────────────────────┘
                  │
┌─────────────────▼───────────────────────┐
│       BUSINESS LOGIC LAYER              │
│  Python + Pandas + NumPy                │
│  • Feature engineering                  │
│  • Data preprocessing                   │
│  • Insight generation                   │
└─────────────────┬───────────────────────┘
                  │
┌─────────────────▼───────────────────────┐
│         ML MODEL LAYER                  │
│  Scikit-learn + XGBoost + LightGBM      │
│  • 5 Ensemble models                    │
│  • Weighted predictions                 │
│  • Performance metrics                  │
└─────────────────┬───────────────────────┘
                  │
┌─────────────────▼───────────────────────┐
│          DATA LAYER                     │
│  Trained Models (.pkl files)            │
│  • Model weights                        │
│  • Feature importance                   │
│  • Performance metrics                  │
└─────────────────────────────────────────┘
```

---

This architecture provides:
✅ **Separation of Concerns**: Clear layer separation
✅ **Scalability**: Easy to add new models or features
✅ **Maintainability**: Well-organized code structure
✅ **Performance**: Efficient model loading and caching
✅ **User Experience**: Fast, responsive UI with real-time feedback
