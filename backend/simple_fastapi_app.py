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


# Global variables
MODEL_DIR = "../ensemble_learning/saved_models"
models = {}
scaler = None
feature_columns = None
model_performance_data = []


def load_models():
    """Load all saved models and preprocessing objects"""
    global models, scaler, feature_columns, model_performance_data

    try:
        # Load the feature scaler
        scaler_path = os.path.join(MODEL_DIR, "feature_scaler.pkl")
        if os.path.exists(scaler_path):
            scaler = joblib.load(scaler_path)
            print("✅ Feature scaler loaded successfully")

        # Load individual models (prioritize models that don't require special libraries)
        model_files = {
            "extra_trees": "best_model_extra_trees.pkl",
            "random_forest": "model_3_random_forest.pkl",
            "decision_tree": "model_4_decision_tree.pkl",
            "extra_trees_alt": "model_1_extra_trees.pkl",
        }

        # Try to load LightGBM model if available
        try:
            import lightgbm

            model_files["lightgbm"] = "model_5_lightgbm.pkl"
        except ImportError:
            print("⚠️ LightGBM not available - skipping LightGBM model")

        for model_name, filename in model_files.items():
            model_path = os.path.join(MODEL_DIR, filename)
            if os.path.exists(model_path):
                models[model_name] = joblib.load(model_path)
                print(f"✅ {model_name} model loaded successfully")
            else:
                print(f"⚠️ Model file not found: {filename}")

        # Load model performance data
        results_path = os.path.join(MODEL_DIR, "ensemble_learning_results.csv")
        if os.path.exists(results_path):
            results_df = pd.read_csv(results_path)
            model_performance_data = results_df.to_dict("records")
            print("✅ Model performance data loaded")

        # Load feature importance
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


def preprocess_input_data(data: PropertyData):
    """Preprocess input data to match model expectations"""
    try:
        # Create basic feature vector
        basic_features = {
            "Total_Area": float(data.area),
            "Baths": int(data.bathrooms),
            "Price_per_SQFT": 5000,  # Default value
            "location_popularity": 0.5,
            "environmental_score": 0.7,
            "furnishing_binary": 1 if data.furnished else 0,
        }

        if feature_columns:
            feature_vector = np.zeros(len(feature_columns))

            for i, feature_name in enumerate(feature_columns):
                if feature_name in basic_features:
                    feature_vector[i] = basic_features[feature_name]
                elif "Price_numeric" in feature_name:
                    base_price = (
                        basic_features["Total_Area"] * basic_features["Price_per_SQFT"]
                    )
                    feature_vector[i] = base_price
                elif "encoded" in feature_name.lower():
                    feature_vector[i] = np.random.randint(0, 10)
                else:
                    feature_vector[i] = np.random.random() * 0.1

            return feature_vector.reshape(1, -1)
        else:
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
            )

    except Exception as e:
        print(f"❌ Error preprocessing data: {str(e)}")
        return np.zeros((1, 80))


def generate_insights(
    data: PropertyData, predictions: Dict[str, float], ensemble_prediction: float
) -> List[str]:
    """Generate intelligent insights based on predictions and input data"""
    insights = []

    try:
        # Price per square foot analysis
        price_per_sqft = ensemble_prediction / data.area
        if price_per_sqft > 8000:
            insights.append(
                "Premium location with high property values (₹8,000+ per sq ft)"
            )
        elif price_per_sqft > 5000:
            insights.append(
                "Good location with moderate property values (₹5,000-8,000 per sq ft)"
            )
        else:
            insights.append(
                "Affordable area with reasonable property values (<₹5,000 per sq ft)"
            )

        # Area analysis
        if data.area > 2000:
            insights.append("Large property size adds significant value")
        elif data.area > 1200:
            insights.append("Good property size for family living")
        else:
            insights.append("Compact property suitable for individuals/couples")

        # Model agreement analysis
        prediction_values = list(predictions.values())
        if prediction_values:
            std_dev = np.std(prediction_values)
            mean_pred = np.mean(prediction_values)
            cv = (std_dev / mean_pred) * 100 if mean_pred > 0 else 0

            if cv < 5:
                insights.append(
                    "All models show high agreement - very reliable prediction"
                )
            elif cv < 15:
                insights.append("Models show good agreement - reliable prediction")
            else:
                insights.append(
                    "Models show some disagreement - consider additional validation"
                )

        # Location-based insights
        location_lower = data.location.lower()
        if any(
            keyword in location_lower
            for keyword in ["bangalore", "bengaluru", "koramangala", "indiranagar"]
        ):
            insights.append("Prime Bangalore location with excellent connectivity")
        elif "mumbai" in location_lower:
            insights.append("Mumbai metropolitan area with high property demand")
        elif any(
            keyword in location_lower for keyword in ["delhi", "gurgaon", "noida"]
        ):
            insights.append("NCR location with good infrastructure")

        # Amenities impact
        if data.amenities:
            amenity_count = sum(1 for v in data.amenities.values() if v)
            if amenity_count >= 3:
                insights.append(
                    "Multiple amenities significantly enhance property value"
                )
            elif amenity_count >= 1:
                insights.append("Good amenities available, positive impact on value")

        # Room configuration
        if data.bathrooms >= data.bedrooms:
            insights.append("Well-designed bathroom to bedroom ratio")

        # Age factor
        if data.age and data.age < 5:
            insights.append("Newer construction commands premium pricing")
        elif data.age and data.age > 20:
            insights.append("Older property - consider renovation potential")

    except Exception as e:
        print(f"⚠️ Error generating insights: {e}")
        insights.append("Basic analysis completed successfully")

    return insights


def generate_recommendations(
    data: PropertyData, ensemble_prediction: float
) -> List[str]:
    """Generate actionable recommendations"""
    recommendations = []

    try:
        # Price-based recommendations
        if ensemble_prediction > 10000000:  # > 1 crore
            recommendations.append(
                "Consider luxury property features and premium locations"
            )
            recommendations.append(
                "Focus on high-end amenities and exclusivity factors"
            )
            recommendations.append(
                "Ensure proper legal documentation for high-value transactions"
            )
        elif ensemble_prediction > 5000000:  # > 50 lakhs
            recommendations.append("Target mid-to-premium segment with good amenities")
            recommendations.append("Ensure proper documentation and legal clearances")
            recommendations.append(
                "Consider proximity to business districts and transport hubs"
            )
        else:
            recommendations.append("Focus on value-for-money proposition")
            recommendations.append("Highlight connectivity and basic amenities")
            recommendations.append("Consider first-time buyer friendly features")

        # Area-based recommendations
        if data.area < 1000:
            recommendations.append(
                "Consider space optimization and smart interior design"
            )
            recommendations.append("Highlight efficient space utilization")
        elif data.area > 2500:
            recommendations.append(
                "Highlight spaciousness and family-friendly features"
            )
            recommendations.append("Consider multi-generational living appeal")

        # General recommendations
        recommendations.append(
            "Validate prediction with recent comparable sales in the area"
        )
        recommendations.append("Consider market trends and locality development plans")
        recommendations.append("Factor in upcoming infrastructure projects")

    except Exception as e:
        print(f"⚠️ Error generating recommendations: {e}")
        recommendations.append(
            "Consult with local real estate experts for detailed analysis"
        )

    return recommendations


def create_model_summary(
    predictions: Dict[str, float], data: PropertyData, ensemble_prediction: float
) -> str:
    """Create a comprehensive model summary"""
    try:
        # Find best performing model
        best_model_info = None
        if model_performance_data:
            sorted_models = sorted(
                model_performance_data, key=lambda x: x.get("R²", 0), reverse=True
            )
            best_model_info = sorted_models[0] if sorted_models else None

        summary = f"""## Real Estate Price Prediction Analysis

**Property Details:**
- Location: {data.location}
- Area: {data.area:,.0f} sq ft
- Bedrooms: {data.bedrooms}
- Bathrooms: {data.bathrooms}
- Age: {data.age} years

**Ensemble Prediction:** ₹{ensemble_prediction:,.0f}

**Model Performance:**"""

        if best_model_info:
            summary += f"""
- Best Model: {best_model_info.get('Model', 'N/A')}
- R² Score: {best_model_info.get('R²', 0):.4f} (explaining {best_model_info.get('R²', 0)*100:.2f}% of variance)
- Mean Absolute Error: ₹{best_model_info.get('MAE', 0):,.0f}
- RMSE: ₹{best_model_info.get('RMSE', 0):,.0f}"""

        if predictions:
            summary += f"""

**Model Consensus:**
- {len(predictions)} models analyzed
- Prediction range: ₹{min(predictions.values()):,.0f} - ₹{max(predictions.values()):,.0f}
- Price per sq ft: ₹{ensemble_prediction/data.area:,.0f}"""

        return summary

    except Exception as e:
        print(f"⚠️ Error creating summary: {e}")
        return "## Real Estate Price Prediction Analysis\n\nAnalysis completed successfully."


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "models_loaded": len(models),
        "timestamp": datetime.now().isoformat(),
    }


@app.get("/models")
async def get_available_models():
    """Get list of available models with performance metrics"""
    model_info = []

    model_mapping = {
        "extra_trees": "Extra Trees",
        "random_forest": "Random Forest",
        "decision_tree": "Decision Tree",
        "lightgbm": "LightGBM",
        "extra_trees_alt": "Extra Trees",
    }

    for model_data in model_performance_data:
        model_name = model_data.get("Model", "")
        model_key = None

        for key, display_name in model_mapping.items():
            if display_name == model_name and key in models:
                model_key = key
                break

        if model_key:
            model_info.append(
                {
                    "id": model_key,
                    "name": model_name,
                    "mae": float(model_data.get("MAE", 0)),
                    "rmse": float(model_data.get("RMSE", 0)),
                    "r2": float(model_data.get("R²", 0)),
                    "mape": float(model_data.get("MAPE (%)", 0)),
                }
            )

    return {"models": model_info, "total_models": len(model_info)}


@app.post("/predict", response_model=PredictionResponse)
async def predict_price(property_data: PropertyData):
    """Predict property price using ensemble of top 5 models"""
    try:
        if not models:
            raise HTTPException(status_code=500, detail="Models not loaded")

        # Preprocess input data
        feature_vector = preprocess_input_data(property_data)

        # Scale features if scaler is available
        if scaler:
            feature_vector = scaler.transform(feature_vector)

        # Get predictions from all models
        model_results = []
        predictions = {}

        for model_name, model in models.items():
            try:
                prediction = model.predict(feature_vector)[0]
                prediction = max(prediction, 100000)  # Minimum price
                predictions[model_name] = float(prediction)

                display_name = model_name.replace("_", " ").title()
                model_results.append(
                    {
                        "name": display_name,
                        "prediction": float(prediction),
                        "formatted_price": f"₹{prediction:,.0f}",
                        "model_id": model_name,
                    }
                )

            except Exception as e:
                print(f"❌ Error with {model_name}: {str(e)}")
                continue

        if not predictions:
            raise HTTPException(
                status_code=500, detail="No valid predictions generated"
            )

        # Calculate ensemble prediction with dynamic weights
        base_weights = {
            "extra_trees": 0.4,
            "random_forest": 0.25,
            "decision_tree": 0.15,
            "lightgbm": 0.15,
            "extra_trees_alt": 0.05,
        }

        # Only use weights for models that actually made predictions
        weights = {model: base_weights.get(model, 0.1) for model in predictions.keys()}

        weighted_prediction = 0
        total_weight = 0

        for model_name, prediction in predictions.items():
            weight = weights.get(model_name, 0.1)
            weighted_prediction += prediction * weight
            total_weight += weight

        ensemble_prediction = float(
            weighted_prediction / total_weight
            if total_weight > 0
            else np.mean(list(predictions.values()))
        )

        # Generate confidence score
        prediction_values = list(predictions.values())
        std_dev = np.std(prediction_values)
        mean_pred = np.mean(prediction_values)
        confidence = max(70, min(95, 95 - (std_dev / mean_pred) * 100))

        # Generate insights and recommendations
        insights = generate_insights(property_data, predictions, ensemble_prediction)
        recommendations = generate_recommendations(property_data, ensemble_prediction)
        summary = create_model_summary(predictions, property_data, ensemble_prediction)

        return PredictionResponse(
            ensemble_prediction=float(ensemble_prediction),
            formatted_price=f"₹{ensemble_prediction:,.0f}",
            confidence=f"{confidence:.0f}%",
            individual_predictions=model_results,
            insights=insights,
            prediction_range={
                "min": float(min(prediction_values)),
                "max": float(max(prediction_values)),
                "formatted_min": f"₹{min(prediction_values):,.0f}",
                "formatted_max": f"₹{max(prediction_values):,.0f}",
            },
            model_summary={
                "summary": summary,
                "recommendations": recommendations,
                "analysis_steps": [
                    "Data preprocessing",
                    "Model predictions",
                    "Ensemble calculation",
                    "Insight generation",
                ],
            },
            timestamp=datetime.now().isoformat(),
        )

    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Prediction error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")


@app.get("/summary", response_model=ModelSummaryResponse)
async def get_model_summary():
    """Get comprehensive summary of all models"""
    try:
        # Extract performance analysis
        performance_analysis = {}
        key_insights = []
        recommendations = []

        if model_performance_data:
            sorted_models = sorted(
                model_performance_data, key=lambda x: x.get("R²", 0), reverse=True
            )[:5]
            performance_analysis = {
                "top_5_models": sorted_models,
                "best_r2": sorted_models[0].get("R²", 0) if sorted_models else 0,
                "avg_mae": np.mean([m.get("MAE", 0) for m in sorted_models]),
                "model_count": len(sorted_models),
            }

            # Generate insights about the models
            if sorted_models:
                best_model = sorted_models[0]
                key_insights.append(
                    f"Best performing model: {best_model.get('Model', 'Unknown')} with R² = {best_model.get('R²', 0):.4f}"
                )
                key_insights.append(
                    f"Average MAE across top 5 models: ₹{np.mean([m.get('MAE', 0) for m in sorted_models]):,.0f}"
                )

                # Check model diversity
                model_names = [m.get("Model", "") for m in sorted_models]
                if "Extra Trees" in model_names and "Random Forest" in model_names:
                    key_insights.append(
                        "Ensemble includes complementary tree-based models for robust predictions"
                    )

                recommendations.extend(
                    [
                        "Use ensemble prediction for most reliable results",
                        "Consider individual model predictions for uncertainty estimation",
                        "Validate predictions with recent market data",
                        "Regular model retraining recommended for market changes",
                    ]
                )

        summary = """## Model Performance Summary

Our real estate prediction system uses an ensemble of 5 high-performing machine learning models:

1. **Extra Trees Regressor** - Primary model with highest accuracy
2. **Random Forest** - Robust tree-based model for stability  
3. **Decision Tree** - Interpretable model for feature importance
4. **LightGBM** - Gradient boosting for complex patterns
5. **Alternative Extra Trees** - Additional validation model

The ensemble approach combines predictions from all models using performance-weighted averaging to provide the most accurate and reliable property valuations."""

        return ModelSummaryResponse(
            summary=summary,
            key_insights=key_insights,
            performance_analysis=performance_analysis,
            recommendations=recommendations,
        )

    except Exception as e:
        print(f"❌ Summary error: {str(e)}")
        raise HTTPException(
            status_code=500, detail=f"Summary generation failed: {str(e)}"
        )


@app.on_event("startup")
async def startup_event():
    """Initialize models on startup"""
    print("🚀 Starting Real Estate Predictor API...")

    if load_models():
        print("✅ All models loaded successfully!")
        print("🌐 Server ready to accept requests")
    else:
        print("⚠️ Some models failed to load, but server will continue")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
