"""
FastAPI Backend for Real Estate Price Predictor
Comprehensive API with ensemble model predictions
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Any
from contextlib import asynccontextmanager
from pathlib import Path
import pandas as pd
import numpy as np
import joblib
import os
from datetime import datetime
import threading
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Lifespan event handler
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan event handler for startup and shutdown"""
    # Startup
    logger.info("Starting Real Estate Predictor API...")
    # Load models in the background to avoid blocking startup
    def _bg_load():
        global is_loading_models
        try:
            load_models()
        finally:
            is_loading_models = False

    global is_loading_models
    is_loading_models = True
    threading.Thread(target=_bg_load, daemon=True).start()
    logger.info("Model loading started in background. API is starting...")
    yield
    # Shutdown
    logger.info("Shutting down API...")

# Initialize FastAPI app
app = FastAPI(
    title="Real Estate Price Predictor API",
    description="AI-powered real estate price prediction using ensemble ML models",
    version="1.0.0",
    lifespan=lifespan
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Model paths (relative to repository root)
MODEL_DIR = Path(__file__).resolve().parents[1] / "ensemble_learning" / "saved_models"

# Global variables for models
models = {}
feature_names = []
model_info = {}
is_loading_models = False

# Pydantic models
class PropertyFeatures(BaseModel):
    """Property input features"""
    BHK: int = Field(..., ge=1, le=10, description="Number of bedrooms")
    Size_in_SqFt: float = Field(..., gt=0, description="Size in square feet")
    Year_Built: int = Field(..., ge=1950, le=2025, description="Year property was built")
    Floor_No: int = Field(..., ge=0, le=50, description="Floor number")
    Total_Floors: int = Field(..., ge=1, le=50, description="Total floors in building")
    Nearby_Schools: int = Field(default=0, ge=0, description="Number of nearby schools")
    Nearby_Hospitals: int = Field(default=0, ge=0, description="Number of nearby hospitals")
    Furnished_Status: str = Field(default="Semi-Furnished", description="Furnished/Semi-Furnished/Unfurnished")
    Public_Transport_Accessibility: str = Field(default="Good", description="Poor/Fair/Good/Excellent")
    Parking_Space: str = Field(default="Yes", description="Yes/No")
    Security: str = Field(default="Yes", description="Yes/No")
    Availability_Status: str = Field(default="Ready to Move", description="Ready to Move/Under Construction")
    Baths: int = Field(default=2, ge=1, le=10, description="Number of bathrooms")
    balcony: str = Field(default="Yes", description="Yes/No")
    location: str = Field(default="Bangalore", description="Location/Area name")
    Property_Type: str = Field(default="Apartment", description="Apartment/Villa/House")
    Facing: str = Field(default="East", description="North/South/East/West")
    Owner_Type: str = Field(default="Primary", description="Primary/Secondary/Tertiary")

class PredictionResponse(BaseModel):
    """Prediction response model"""
    ensemble_prediction: float
    formatted_price: str
    confidence: str
    individual_predictions: List[Dict[str, Any]]
    insights: List[str]
    prediction_range: Dict[str, Any]
    feature_importance: List[Dict[str, Any]]
    model_performance: Dict[str, Any]

class HealthResponse(BaseModel):
    """Health check response"""
    status: str
    models_loaded: int
    timestamp: str
    version: str

# Helper functions
def load_models():
    """Load all ensemble models"""
    global models, feature_names, model_info
    
    try:
        logger.info(f"Loading models from: {MODEL_DIR}")
        
        # Use exact filenames available in the repository (relative paths)
        model_files = {
            "Extra Trees": "model_1_extra_trees.pkl",
            "Random Forest": "model_3_random_forest.pkl",
            "Decision Tree": "model_4_decision_tree.pkl",
            "LightGBM": "model_5_lightgbm.pkl",
            "Extra Trees (Best)": "best_model_extra_trees.pkl",
        }

        # Default weights (will be normalized over loaded models)
        default_weights = {
            "Extra Trees": 0.40,
            "Random Forest": 0.25,
            "Decision Tree": 0.15,
            "LightGBM": 0.15,
        }
        
        # Performance metrics
        model_metrics = {
            "Extra Trees": {"R2": 0.999999, "MAE": 130.67, "RMSE": 1004.53},
            "Random Forest": {"R2": 0.999999, "MAE": 262.83, "RMSE": 1866.99},
            "Decision Tree": {"R2": 0.999998, "MAE": 338.73, "RMSE": 3252.90},
            "LightGBM": {"R2": 0.999992, "MAE": 1677.42, "RMSE": 6988.41},
            "XGBoost": {"R2": 0.999942, "MAE": 7009.06, "RMSE": 18394.10}
        }
        
        for model_name, filename in model_files.items():
            model_path = MODEL_DIR / filename
            if model_path.exists():
                try:
                    models[model_name] = joblib.load(str(model_path))
                    logger.info(f"✓ Loaded {model_name} from {model_path}")
                    # Temporarily set raw weight; we'll normalize later
                    model_info[model_name] = {
                        "weight": default_weights.get(model_name, 0.0),
                        "metrics": model_metrics.get(model_name, {}),
                    }
                except Exception:
                    # Include traceback for easier debugging on Windows
                    logger.exception(f"✗ Failed to load {model_name} from {model_path}")
            else:
                logger.warning(f"✗ Model file not found: {model_path}")

        # Normalize weights across only the loaded models
        if models:
            weight_sum = sum(default_weights.get(name, 0.0) for name in models.keys())
            if weight_sum <= 0:
                equal_weight = 1.0 / len(models)
                for name in models.keys():
                    model_info[name]["weight"] = equal_weight
            else:
                for name in models.keys():
                    model_info[name]["weight"] = default_weights.get(name, 0.0) / weight_sum
        
        # Load feature names
        feature_importance_path = MODEL_DIR / "feature_importance.csv"
        if feature_importance_path.exists():
            fi_df = pd.read_csv(feature_importance_path)
            feature_names = fi_df['feature'].tolist()
            logger.info(f"✓ Loaded {len(feature_names)} features")
        
        logger.info(f"Successfully loaded {len(models)} models")
        
    except Exception:
        logger.exception(f"Error loading models from {MODEL_DIR}")
        raise

def encode_categorical(value: str, mapping: Dict[str, int]) -> int:
    """Encode categorical values"""
    return mapping.get(value, 0)

def prepare_features(data: PropertyFeatures) -> pd.DataFrame:
    """Prepare input features for prediction"""
    
    # Encoding mappings (based on common patterns)
    furnished_mapping = {"Unfurnished": 0, "Semi-Furnished": 1, "Furnished": 2, "Fully Furnished": 3}
    transport_mapping = {"Poor": 0, "Fair": 1, "Good": 2, "Excellent": 3}
    yes_no_mapping = {"No": 0, "Yes": 1}
    availability_mapping = {"Under Construction": 0, "Ready to Move": 1, "Almost Ready": 2}
    property_type_mapping = {"Apartment": 0, "Villa": 1, "House": 2, "Penthouse": 3}
    facing_mapping = {"North": 0, "South": 1, "East": 2, "West": 3, "North-East": 4, "South-East": 5}
    owner_type_mapping = {"Primary": 0, "Secondary": 1, "Tertiary": 2}
    
    # Calculate derived features
    current_year = datetime.now().year
    age_of_property = current_year - data.Year_Built
    price_per_sqft = 0.09  # Default placeholder
    total_area = data.Size_in_SqFt
    area_per_bedroom = data.Size_in_SqFt / max(data.BHK, 1)
    bath_bedroom_ratio = data.Baths / max(data.BHK, 1)
    
    # Base features
    features = {
        'BHK': data.BHK,
        'Size_in_SqFt': data.Size_in_SqFt,
        'Price_in_Lakhs': 0.0,  # Placeholder
        'Price_per_SqFt': price_per_sqft,
        'Year_Built': data.Year_Built,
        'Floor_No': data.Floor_No,
        'Total_Floors': data.Total_Floors,
        'Age_of_Property': age_of_property,
        'Nearby_Schools': data.Nearby_Schools,
        'Nearby_Hospitals': data.Nearby_Hospitals,
        'Furnished_Status_encoded': encode_categorical(data.Furnished_Status, furnished_mapping),
        'Public_Transport_Accessibility_encoded': encode_categorical(data.Public_Transport_Accessibility, transport_mapping),
        'Parking_Space_encoded': encode_categorical(data.Parking_Space, yes_no_mapping),
        'Security_encoded': encode_categorical(data.Security, yes_no_mapping),
        'Availability_Status_encoded': encode_categorical(data.Availability_Status, availability_mapping),
        'Total_Area': total_area,
        'Price_per_SQFT': price_per_sqft,
        'Baths': data.Baths,
        'balcony_encoded': encode_categorical(data.balcony, yes_no_mapping),
        'Property_Type_encoded': encode_categorical(data.Property_Type, property_type_mapping),
        'Facing_encoded': encode_categorical(data.Facing, facing_mapping),
        'Owner_Type_encoded': encode_categorical(data.Owner_Type, owner_type_mapping),
        'area_per_bedroom': area_per_bedroom,
        'bath_bedroom_ratio': bath_bedroom_ratio,
        'furnishing_binary': 1 if data.Furnished_Status in ["Furnished", "Fully Furnished"] else 0,
        'parking_binary': encode_categorical(data.Parking_Space, yes_no_mapping),
        
        # Placeholder encoded values (these would normally come from label encoders)
        'State_encoded': 1,
        'City_encoded': 1,
        'location_encoded': hash(data.location) % 100,
        'Amenities_encoded': 324,
        'Name_encoded': 0,
        'Property Title_encoded': 17,
        'Price_encoded': 269,
        'Balcony_encoded': 2,
        'Date_x_encoded': 2009,
        'Date_y_encoded': 95,
        'location_popularity': 17242,
        'size_category_encoded': 4,
        
        # Environmental features (defaults - in production, fetch from APIs)
        'PM2.5': 30.26,
        'PM10': 76.68,
        'NO': 7.52,
        'NO2': 26.91,
        'NOx': 19.1,
        'NH3': 21.02,
        'CO': 0.92,
        'SO2': 5.02,
        'O3': 31.55,
        'Benzene': 0.87,
        'Toluene': 1.76,
        'Xylene': 0.0,
        'AQI': 86.0,
        'AQI_normalized': 0.19879518072289157,
        'AQI_Bucket_encoded': 4,
        'AQI_Bucket_encoded_normalized': 0.8,
        'environmental_score': 0.8,
        
        # Additional numeric features
        'Price_numeric': 2300000.0,  # Placeholder
        'feature_importance': 0.570577463793437,
        'Month_x': 6,
        'Year_x': 2017,
        'Year_y': 2016,
        'Month_y': 7,
        'Day': 0.1992697522783708,
        'Night': -0.0694164367552499,
        'DayLimit': 0.3930548923616099,
        'NightLimit': 0.2308194076748567,
        'StationEncoded': 3.0,
        'DayExcess': 0.077633488859798,
        'NightExcess': 0.1156702843729479,
        
        # Interaction features
        'BHK_Size_in_SqFt_interaction': data.BHK * data.Size_in_SqFt,
        'Baths_BHK_interaction': data.Baths * data.BHK,
        
        # Log transformed features
        'Price_numeric_log': np.log1p(2300000.0),
        'PM2.5_log': np.log1p(30.26),
        'PM10_log': np.log1p(76.68),
        'NO_log': np.log1p(7.52),
        'NO2_log': np.log1p(26.91),
        'NH3_log': np.log1p(21.02),
        'SO2_log': np.log1p(5.02),
        'AQI_log': np.log1p(86.0),
        'location_popularity_log': np.log1p(17242),
        'O3_sqrt': np.sqrt(31.55),
    }
    
    # Create DataFrame
    df = pd.DataFrame([features])
    
    # Use ONLY the features that were present during training, in the exact same order
    if feature_names:
        # Only keep features that exist in feature_names
        missing_features = [f for f in feature_names if f not in df.columns]
        for feature in missing_features:
            df[feature] = 0.0
        # Return DataFrame with columns in the exact order as feature_names
        return df[feature_names]
    else:
        return df

def generate_insights(data: PropertyFeatures, prediction: float) -> List[str]:
    """Generate insights based on input features"""
    insights = []
    
    # Size-based insights
    if data.Size_in_SqFt > 2000:
        insights.append("🏡 Large property size - Premium segment pricing")
    elif data.Size_in_SqFt < 800:
        insights.append("🏢 Compact property - Suitable for investment or starter home")
    
    # Age-based insights
    age = datetime.now().year - data.Year_Built
    if age < 5:
        insights.append("🆕 New property - Higher resale value expected")
    elif age > 20:
        insights.append("🏛️ Older property - May require renovation considerations")
    
    # Floor-based insights
    if data.Floor_No > data.Total_Floors * 0.7:
        insights.append("🌆 High floor - Better views and ventilation")
    
    # Amenities insights
    if data.Furnished_Status == "Fully Furnished":
        insights.append("🛋️ Fully furnished - Ready to move, added value")
    
    if data.Parking_Space == "Yes":
        insights.append("🚗 Parking available - Essential in Bangalore")
    
    # Location insights
    insights.append(f"📍 Location: {data.location} - Premium Bangalore area")
    
    return insights

@app.get("/", tags=["Root"])
async def root():
    """Root endpoint"""
    return {
        "message": "Real Estate Price Predictor API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health"
    }

@app.get("/health", response_model=HealthResponse, tags=["Health"])
async def health_check():
    """Health check endpoint"""
    return HealthResponse(
        status=("healthy" if len(models) > 0 else ("loading" if is_loading_models else "unhealthy")),
        models_loaded=len(models),
        timestamp=datetime.now().isoformat(),
        version="1.0.0"
    )

@app.post("/predict", response_model=PredictionResponse, tags=["Prediction"])
async def predict_price(data: PropertyFeatures):
    """
    Predict real estate price using ensemble models
    """
    try:
        if not models:
            # Trigger background load if not already loading
            global is_loading_models
            if not is_loading_models:
                is_loading_models = True
                threading.Thread(target=load_models, daemon=True).start()
            raise HTTPException(status_code=503, detail="Models are loading, please try again in a few seconds")
        
        # Prepare features
        X = prepare_features(data)
        
        # Make predictions with each model
        predictions = {}
        for model_name, model in models.items():
            try:
                # For sklearn models, use numpy array to avoid feature name validation issues
                # LightGBM can handle DataFrames natively
                if hasattr(model, 'feature_names_in_'):
                    # Sklearn model - use numpy array
                    pred = model.predict(X.values)[0]
                else:
                    # LightGBM or other - use DataFrame
                    pred = model.predict(X)[0]
                predictions[model_name] = pred
            except Exception as e:
                logger.error(f"Error predicting with {model_name}: {str(e)}")
        
        if not predictions:
            raise HTTPException(status_code=500, detail="No models could make predictions")
        
        # Calculate weighted ensemble prediction
        ensemble_pred = sum(
            pred * model_info[name]["weight"]
            for name, pred in predictions.items()
            if name in model_info
        )
        
        # Format individual predictions
        individual_preds = [
            {
                "name": name,
                "prediction": float(pred),
                "formatted_price": f"₹{pred/100000:.2f} Lakhs",
                "weight": model_info.get(name, {}).get("weight", 0) * 100,
                "metrics": model_info.get(name, {}).get("metrics", {})
            }
            for name, pred in predictions.items()
        ]
        
        # Calculate prediction range
        pred_values = list(predictions.values())
        pred_min = min(pred_values)
        pred_max = max(pred_values)
        pred_std = np.std(pred_values)
        
        # Calculate confidence
        confidence = max(0, min(100, 100 - (pred_std / ensemble_pred * 100)))
        
        # Generate insights
        insights = generate_insights(data, ensemble_pred)
        
        # Get top features
        feature_importance_path = os.path.join(MODEL_DIR, "feature_importance.csv")
        top_features = []
        if os.path.exists(feature_importance_path):
            fi_df = pd.read_csv(feature_importance_path)
            top_features = [
                {"feature": row["feature"], "importance": float(row["avg_importance"])}
                for _, row in fi_df.head(10).iterrows()
            ]
        
        # Model performance summary
        model_performance = {
            "total_models": len(models),
            "average_r2": np.mean([m["metrics"].get("R2", 0) for m in model_info.values()]),
            "best_model": max(model_info.items(), key=lambda x: x[1]["metrics"].get("R2", 0))[0]
        }
        
        return PredictionResponse(
            ensemble_prediction=float(ensemble_pred),
            formatted_price=f"₹{ensemble_pred/100000:.2f} Lakhs",
            confidence=f"{confidence:.1f}%",
            individual_predictions=individual_preds,
            insights=insights,
            prediction_range={
                "min": float(pred_min),
                "max": float(pred_max),
                "formatted_min": f"₹{pred_min/100000:.2f} Lakhs",
                "formatted_max": f"₹{pred_max/100000:.2f} Lakhs",
                "std_dev": float(pred_std)
            },
            feature_importance=top_features,
            model_performance=model_performance
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Prediction error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")

@app.get("/models", tags=["Models"])
async def get_models_info():
    """Get information about loaded models"""
    return {
        "models": [
            {
                "name": name,
                "weight": info["weight"],
                "metrics": info["metrics"],
                "loaded": True
            }
            for name, info in model_info.items()
        ],
        "total_models": len(models)
    }

@app.get("/features", tags=["Features"])
async def get_features():
    """Get list of all features used by models"""
    return {
        "features": feature_names,
        "total_features": len(feature_names)
    }

if __name__ == "__main__":
    import uvicorn
    # Disable reload here to avoid double startup and speed up when running via `python main.py`.
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=False)
