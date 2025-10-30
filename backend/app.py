from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, List, Optional, Any
import pandas as pd
import numpy as np
import joblib
import os
import json
from datetime import datetime
import warnings
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages
from typing_extensions import Annotated, TypedDict
import asyncio
import uvicorn

warnings.filterwarnings("ignore")

app = FastAPI(title="Real Estate Predictor API", version="1.0.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Pydantic models for request/response
class PropertyData(BaseModel):
    location: str
    area: float
    bedrooms: int
    bathrooms: int
    age: Optional[int] = 5
    furnished: Optional[bool] = False
    amenities: Optional[Dict[str, bool]] = {}


class PredictionResponse(BaseModel):
    ensemble_prediction: float
    formatted_price: str
    confidence: str
    individual_predictions: List[Dict[str, Any]]
    insights: List[str]
    prediction_range: Dict[str, Any]
    model_summary: Dict[str, Any]
    timestamp: str


class ModelSummaryResponse(BaseModel):
    summary: str
    key_insights: List[str]
    performance_analysis: Dict[str, Any]
    recommendations: List[str]


# LangGraph State
class AnalysisState(TypedDict):
    model_results: List[Dict[str, Any]]
    performance_data: Dict[str, Any]
    user_input: Dict[str, Any]
    analysis_steps: Annotated[List[str], add_messages]
    summary: str
    insights: List[str]
    recommendations: List[str]


# Global variables
MODEL_DIR = "../ensemble_learning/saved_models"
models = {}
scaler = None
feature_columns = None
model_performance_data = {}
analysis_graph = None


def load_models():
    """Load all saved models and preprocessing objects"""
    global models, scaler, feature_columns

    try:
        # Load the feature scaler
        scaler_path = os.path.join(MODEL_DIR, "feature_scaler.pkl")
        if os.path.exists(scaler_path):
            scaler = joblib.load(scaler_path)
            print("✅ Feature scaler loaded successfully")

        # Load individual models (top 5 performing models)
        model_files = {
            "extra_trees": "best_model_extra_trees.pkl",
            "random_forest": "model_3_random_forest.pkl",
            "decision_tree": "model_4_decision_tree.pkl",
            "lightgbm": "model_5_lightgbm.pkl",
            "extra_trees_alt": "model_1_extra_trees.pkl",  # Alternative extra trees model
        }

        for model_name, filename in model_files.items():
            model_path = os.path.join(MODEL_DIR, filename)
            if os.path.exists(model_path):
                models[model_name] = joblib.load(model_path)
                print(f"✅ {model_name} model loaded successfully")
            else:
                print(f"⚠️ Model file not found: {filename}")

        # Load dataset info to understand feature structure
        info_path = os.path.join(MODEL_DIR, "dataset_info.json")
        if os.path.exists(info_path):
            with open(info_path, "r") as f:
                dataset_info = json.load(f)
                print(
                    f"✅ Dataset info loaded: {dataset_info['feature_count']} features"
                )

        # Load feature importance to understand feature names
        feature_importance_path = os.path.join(MODEL_DIR, "feature_importance.csv")
        if os.path.exists(feature_importance_path):
            feature_df = pd.read_csv(feature_importance_path)
            feature_columns = feature_df["feature"].tolist()
            print(f"✅ Feature columns loaded: {len(feature_columns)} features")

        print(f"🎯 Total models loaded: {len(models)}")
        return True

    except Exception as e:
        print(f"❌ Error loading models: {str(e)}")
        return False


def preprocess_input_data(data):
    """Preprocess input data to match model expectations"""
    try:
        # Create a basic feature vector based on the input
        # This is a simplified mapping - in production, you'd want to match exactly
        # the feature engineering pipeline used during training

        # Basic features from user input
        basic_features = {
            "Total_Area": float(data.get("area", 1000)),
            "Baths": int(data.get("bathrooms", 2)),
            "Price_per_SQFT": 5000,  # Default value, could be estimated
            "location_popularity": 0.5,  # Default value
            "environmental_score": 0.7,  # Default value
            "furnishing_binary": 1 if data.get("furnished", False) else 0,
        }

        # Create a feature vector with default values for all required features
        if feature_columns:
            # Initialize with zeros
            feature_vector = np.zeros(len(feature_columns))

            # Map basic features to their positions
            for i, feature_name in enumerate(feature_columns):
                if feature_name in basic_features:
                    feature_vector[i] = basic_features[feature_name]
                elif "Price_numeric" in feature_name:
                    # Estimate price numeric based on area and location
                    base_price = (
                        basic_features["Total_Area"] * basic_features["Price_per_SQFT"]
                    )
                    feature_vector[i] = base_price
                elif "encoded" in feature_name.lower():
                    # Set encoded features to reasonable defaults
                    feature_vector[i] = np.random.randint(0, 10)
                else:
                    # Set other features to reasonable defaults
                    feature_vector[i] = np.random.random() * 0.1

            return feature_vector.reshape(1, -1)
        else:
            # Fallback: create a basic feature vector
            return np.array(
                [
                    [
                        basic_features["Total_Area"],
                        basic_features["Baths"],
                        basic_features["Price_per_SQFT"],
                        basic_features["location_popularity"],
                        basic_features["environmental_score"],
                        basic_features["furnishing_binary"],
                    ]
                    + [0.1] * 74
                ]
            )  # Pad to 80 features as per dataset_info

    except Exception as e:
        print(f"❌ Error preprocessing data: {str(e)}")
        # Return a default feature vector
        return np.zeros((1, 80))


@app.route("/health", methods=["GET"])
def health_check():
    """Health check endpoint"""
    return jsonify(
        {
            "status": "healthy",
            "models_loaded": len(models),
            "timestamp": datetime.now().isoformat(),
        }
    )


@app.route("/models", methods=["GET"])
def get_available_models():
    """Get list of available models"""
    model_info = []

    # Load model performance data
    results_path = os.path.join(MODEL_DIR, "ensemble_learning_results.csv")
    if os.path.exists(results_path):
        results_df = pd.read_csv(results_path)

        # Map model names to our loaded models
        model_mapping = {
            "extra_trees": "Extra Trees",
            "random_forest": "Random Forest",
            "decision_tree": "Decision Tree",
            "lightgbm": "LightGBM",
            "extra_trees_alt": "Extra Trees",
        }

        for model_key, model_display_name in model_mapping.items():
            if model_key in models:
                # Find corresponding results
                result_row = results_df[results_df["Model"] == model_display_name]
                if not result_row.empty:
                    model_info.append(
                        {
                            "id": model_key,
                            "name": model_display_name,
                            "mae": float(result_row["MAE"].iloc[0]),
                            "rmse": float(result_row["RMSE"].iloc[0]),
                            "r2": float(result_row["R²"].iloc[0]),
                            "mape": float(result_row["MAPE (%)"].iloc[0]),
                        }
                    )

    return jsonify({"models": model_info, "total_models": len(model_info)})


@app.route("/predict", methods=["POST"])
def predict_price():
    """Predict property price using multiple models"""
    try:
        data = request.get_json()

        if not data:
            return jsonify({"error": "No data provided"}), 400

        # Preprocess input data
        feature_vector = preprocess_input_data(data)

        # Scale features if scaler is available
        if scaler:
            feature_vector = scaler.transform(feature_vector)

        # Get predictions from all models
        predictions = {}
        model_details = []

        for model_name, model in models.items():
            try:
                prediction = model.predict(feature_vector)[0]
                # Ensure prediction is positive and reasonable
                prediction = max(prediction, 100000)  # Minimum price
                predictions[model_name] = float(prediction)

                # Format model name for display
                display_name = model_name.replace("_", " ").title()
                model_details.append(
                    {
                        "name": display_name,
                        "prediction": float(prediction),
                        "formatted_price": f"₹{prediction:,.0f}",
                    }
                )

            except Exception as e:
                print(f"❌ Error with {model_name}: {str(e)}")
                continue

        if not predictions:
            return jsonify({"error": "No valid predictions generated"}), 500

        # Calculate ensemble prediction (weighted average based on performance)
        # Extra Trees gets highest weight as it's the best performing model
        weights = {
            "extra_trees": 0.4,
            "random_forest": 0.25,
            "decision_tree": 0.15,
            "lightgbm": 0.15,
            "extra_trees_alt": 0.05,
        }

        weighted_prediction = 0
        total_weight = 0

        for model_name, prediction in predictions.items():
            weight = weights.get(model_name, 0.1)
            weighted_prediction += prediction * weight
            total_weight += weight

        if total_weight > 0:
            ensemble_prediction = weighted_prediction / total_weight
        else:
            ensemble_prediction = np.mean(list(predictions.values()))

        # Generate confidence score based on prediction variance
        prediction_values = list(predictions.values())
        std_dev = np.std(prediction_values)
        mean_pred = np.mean(prediction_values)
        confidence = max(70, min(95, 95 - (std_dev / mean_pred) * 100))

        # Generate insights based on input features
        insights = generate_insights(data, ensemble_prediction)

        return jsonify(
            {
                "ensemble_prediction": float(ensemble_prediction),
                "formatted_price": f"₹{ensemble_prediction:,.0f}",
                "confidence": f"{confidence:.0f}%",
                "individual_predictions": model_details,
                "insights": insights,
                "prediction_range": {
                    "min": float(min(prediction_values)),
                    "max": float(max(prediction_values)),
                    "formatted_min": f"₹{min(prediction_values):,.0f}",
                    "formatted_max": f"₹{max(prediction_values):,.0f}",
                },
                "timestamp": datetime.now().isoformat(),
            }
        )

    except Exception as e:
        print(f"❌ Prediction error: {str(e)}")
        return jsonify({"error": f"Prediction failed: {str(e)}"}), 500


def generate_insights(data, prediction):
    """Generate insights based on input data and prediction"""
    insights = []

    area = float(data.get("area", 1000))
    bedrooms = int(data.get("bedrooms", 2))
    bathrooms = int(data.get("bathrooms", 2))
    location = data.get("location", "")

    # Price per square foot analysis
    price_per_sqft = prediction / area
    if price_per_sqft > 8000:
        insights.append("Premium location with high property values")
    elif price_per_sqft > 5000:
        insights.append("Good location with moderate property values")
    else:
        insights.append("Affordable area with reasonable property values")

    # Area analysis
    if area > 2000:
        insights.append("Large property size adds significant value")
    elif area > 1200:
        insights.append("Good property size for family living")
    else:
        insights.append("Compact property suitable for individuals/couples")

    # Room configuration
    if bathrooms >= bedrooms:
        insights.append("Well-designed bathroom to bedroom ratio")

    # Location-based insights
    if any(
        keyword in location.lower()
        for keyword in ["bangalore", "bengaluru", "koramangala", "indiranagar"]
    ):
        insights.append("Prime Bangalore location with excellent connectivity")

    # Amenities impact
    amenities = data.get("amenities", {})
    amenity_count = sum(1 for v in amenities.values() if v)
    if amenity_count >= 3:
        insights.append("Multiple amenities enhance property value")
    elif amenity_count >= 1:
        insights.append("Good amenities available")

    return insights


# Initialize models on startup
if __name__ == "__main__":
    print("🚀 Starting Real Estate Predictor API...")

    if load_models():
        print("✅ All models loaded successfully!")
        app.run(debug=True, port=5000)
    else:
        print("❌ Failed to load models. Please check model files.")
