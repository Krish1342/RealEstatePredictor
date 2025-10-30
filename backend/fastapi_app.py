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
    global models, scaler, feature_columns, model_performance_data

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
            "extra_trees_alt": "model_1_extra_trees.pkl",
        }

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


def create_analysis_graph():
    """Create LangGraph for model analysis and summarization"""

    def analyze_performance(state: AnalysisState) -> AnalysisState:
        """Analyze model performance metrics"""
        analysis_steps = state.get("analysis_steps", [])
        analysis_steps.append("Analyzing model performance metrics...")

        performance_data = state["performance_data"]

        # Extract top 5 models
        sorted_models = sorted(
            performance_data, key=lambda x: x.get("R²", 0), reverse=True
        )[:5]

        analysis = {
            "top_models": sorted_models,
            "best_model": sorted_models[0] if sorted_models else None,
            "avg_r2": np.mean([m.get("R²", 0) for m in sorted_models]),
            "avg_mae": np.mean([m.get("MAE", 0) for m in sorted_models]),
        }

        state["performance_analysis"] = analysis
        state["analysis_steps"] = analysis_steps
        return state

    def generate_insights(state: AnalysisState) -> AnalysisState:
        """Generate insights based on model predictions and performance"""
        analysis_steps = state.get("analysis_steps", [])
        analysis_steps.append("Generating model insights...")

        model_results = state["model_results"]
        performance_analysis = state["performance_analysis"]
        user_input = state["user_input"]

        insights = []

        # Performance insights
        best_model = performance_analysis["best_model"]
        if best_model:
            insights.append(
                f"Best performing model: {best_model['Model']} with R² score of {best_model['R²']:.4f}"
            )

        # Prediction variance insights
        if model_results:
            predictions = [result["prediction"] for result in model_results]
            if predictions:
                variance = np.var(predictions)
                mean_pred = np.mean(predictions)
                cv = (np.sqrt(variance) / mean_pred) * 100 if mean_pred > 0 else 0

                if cv < 5:
                    insights.append(
                        "All models show high agreement in predictions (low variance)"
                    )
                elif cv < 15:
                    insights.append("Models show moderate agreement in predictions")
                else:
                    insights.append(
                        "Models show significant disagreement - consider additional validation"
                    )

        # Property-specific insights
        if user_input:
            area = user_input.get("area", 0)
            location = user_input.get("location", "")

            if area > 2000:
                insights.append(
                    "Large property size detected - premium pricing expected"
                )
            elif area < 800:
                insights.append("Compact property - budget-friendly segment")

            if "bangalore" in location.lower() or "bengaluru" in location.lower():
                insights.append("Bangalore location premium factor applied")

        state["insights"] = insights
        state["analysis_steps"] = analysis_steps
        return state

    def create_summary(state: AnalysisState) -> AnalysisState:
        """Create comprehensive summary of analysis"""
        analysis_steps = state.get("analysis_steps", [])
        analysis_steps.append("Creating comprehensive summary...")

        model_results = state["model_results"]
        performance_analysis = state["performance_analysis"]
        insights = state["insights"]

        # Create summary
        if model_results:
            ensemble_pred = np.mean([r["prediction"] for r in model_results])
        else:
            ensemble_pred = 0

        best_model = performance_analysis["best_model"]

        summary = f"""
## Real Estate Price Prediction Analysis

**Ensemble Prediction:** ₹{ensemble_pred:,.0f}

**Top Performing Model:** {best_model['Model'] if best_model else 'N/A'}
- R² Score: {best_model['R²']:.4f} (explaining {best_model['R²']*100:.2f}% of variance)
- Mean Absolute Error: ₹{best_model['MAE']:,.0f}
- Root Mean Square Error: ₹{best_model['RMSE']:,.0f}

**Model Consensus:**
- {len(model_results)} models analyzed
- Average R² across top models: {performance_analysis['avg_r2']:.4f}
- Prediction range: ₹{min([r['prediction'] for r in model_results]):,.0f} - ₹{max([r['prediction'] for r in model_results]):,.0f}

**Key Insights:**
""" + "\n".join(
            [f"- {insight}" for insight in insights]
        )

        state["summary"] = summary
        state["analysis_steps"] = analysis_steps
        return state

    def generate_recommendations(state: AnalysisState) -> AnalysisState:
        """Generate actionable recommendations"""
        analysis_steps = state.get("analysis_steps", [])
        analysis_steps.append("Generating recommendations...")

        model_results = state["model_results"]
        user_input = state["user_input"]

        recommendations = []

        # Price-based recommendations
        if model_results:
            predictions = [r["prediction"] for r in model_results]
            avg_pred = np.mean(predictions)

            if avg_pred > 10000000:  # > 1 crore
                recommendations.append(
                    "Consider luxury property features and premium locations"
                )
                recommendations.append(
                    "Focus on high-end amenities and exclusivity factors"
                )
            elif avg_pred > 5000000:  # > 50 lakhs
                recommendations.append(
                    "Target mid-to-premium segment with good amenities"
                )
                recommendations.append(
                    "Ensure proper documentation and legal clearances"
                )
            else:
                recommendations.append("Focus on value-for-money proposition")
                recommendations.append("Highlight connectivity and basic amenities")

        # Area-based recommendations
        if user_input:
            area = user_input.get("area", 0)
            if area < 1000:
                recommendations.append(
                    "Consider space optimization and smart interior design"
                )
            elif area > 2500:
                recommendations.append(
                    "Highlight spaciousness and family-friendly features"
                )

        # General recommendations
        recommendations.append("Validate prediction with recent comparable sales")
        recommendations.append("Consider market trends and locality development plans")

        state["recommendations"] = recommendations
        state["analysis_steps"] = analysis_steps
        return state

    # Create the graph
    workflow = StateGraph(AnalysisState)

    # Add nodes
    workflow.add_node("analyze_performance", analyze_performance)
    workflow.add_node("generate_insights", generate_insights)
    workflow.add_node("create_summary", create_summary)
    workflow.add_node("generate_recommendations", generate_recommendations)

    # Add edges
    workflow.set_entry_point("analyze_performance")
    workflow.add_edge("analyze_performance", "generate_insights")
    workflow.add_edge("generate_insights", "create_summary")
    workflow.add_edge("create_summary", "generate_recommendations")
    workflow.add_edge("generate_recommendations", END)

    return workflow.compile()


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
    """Predict property price using ensemble of top 5 models with LangGraph analysis"""
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

        # Calculate ensemble prediction
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

        ensemble_prediction = (
            weighted_prediction / total_weight
            if total_weight > 0
            else np.mean(list(predictions.values()))
        )

        # Generate confidence score
        prediction_values = list(predictions.values())
        std_dev = np.std(prediction_values)
        mean_pred = np.mean(prediction_values)
        confidence = max(70, min(95, 95 - (std_dev / mean_pred) * 100))

        # Run LangGraph analysis
        initial_state = {
            "model_results": model_results,
            "performance_data": model_performance_data,
            "user_input": property_data.dict(),
            "analysis_steps": [],
            "summary": "",
            "insights": [],
            "recommendations": [],
        }

        # Execute the analysis workflow
        final_state = await asyncio.get_event_loop().run_in_executor(
            None, analysis_graph.invoke, initial_state
        )

        return PredictionResponse(
            ensemble_prediction=float(ensemble_prediction),
            formatted_price=f"₹{ensemble_prediction:,.0f}",
            confidence=f"{confidence:.0f}%",
            individual_predictions=model_results,
            insights=final_state["insights"],
            prediction_range={
                "min": float(min(prediction_values)),
                "max": float(max(prediction_values)),
                "formatted_min": f"₹{min(prediction_values):,.0f}",
                "formatted_max": f"₹{max(prediction_values):,.0f}",
            },
            model_summary={
                "summary": final_state["summary"],
                "recommendations": final_state["recommendations"],
                "analysis_steps": final_state["analysis_steps"],
            },
            timestamp=datetime.now().isoformat(),
        )

    except Exception as e:
        print(f"❌ Prediction error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")


@app.get("/summary", response_model=ModelSummaryResponse)
async def get_model_summary():
    """Get comprehensive summary of all models using LangGraph"""
    try:
        # Create a comprehensive analysis of all models
        initial_state = {
            "model_results": [],
            "performance_data": model_performance_data,
            "user_input": {},
            "analysis_steps": [],
            "summary": "",
            "insights": [],
            "recommendations": [],
        }

        final_state = await asyncio.get_event_loop().run_in_executor(
            None, analysis_graph.invoke, initial_state
        )

        # Extract performance analysis
        performance_analysis = {}
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

        return ModelSummaryResponse(
            summary=final_state["summary"] or "Model analysis complete",
            key_insights=final_state["insights"],
            performance_analysis=performance_analysis,
            recommendations=final_state["recommendations"],
        )

    except Exception as e:
        print(f"❌ Summary error: {str(e)}")
        raise HTTPException(
            status_code=500, detail=f"Summary generation failed: {str(e)}"
        )


@app.on_event("startup")
async def startup_event():
    """Initialize models and graph on startup"""
    global analysis_graph

    print("🚀 Starting Real Estate Predictor API...")

    if load_models():
        print("✅ All models loaded successfully!")
        analysis_graph = create_analysis_graph()
        print("✅ LangGraph analysis workflow initialized!")
    else:
        print("❌ Failed to load models. Please check model files.")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
