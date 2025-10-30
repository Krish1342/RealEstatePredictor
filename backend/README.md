# Real Estate Predictor FastAPI Backend

This backend service provides AI-powered property price predictions using ensemble learning with top 5 machine learning models integrated with LangGraph for intelligent analysis and summarization.

## Features

- **Ensemble Learning**: Uses top 5 performing models (Extra Trees, Random Forest, Decision Tree, LightGBM, XGBoost)
- **LangGraph Integration**: Intelligent analysis workflow for model predictions and insights
- **FastAPI**: Modern, fast web framework with automatic API documentation
- **Real-time Predictions**: Get instant property price predictions with confidence scores
- **Model Analytics**: Detailed performance metrics and individual model predictions
- **Smart Insights**: AI-generated insights and recommendations based on predictions

## Quick Start

### 1. Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 2. Verify Model Files

Ensure the following files exist in `../ensemble_learning/saved_models/`:

- `best_model_extra_trees.pkl`
- `model_3_random_forest.pkl`
- `model_4_decision_tree.pkl`
- `model_5_lightgbm.pkl`
- `model_1_extra_trees.pkl`
- `feature_scaler.pkl`
- `ensemble_learning_results.csv`
- `feature_importance.csv`

### 3. Start the Server

```bash
python start_server.py
```

Or directly with uvicorn:

```bash
uvicorn fastapi_app:app --host 0.0.0.0 --port 8000 --reload
```

### 4. Access the API

- **API Server**: http://localhost:8000
- **Interactive Documentation**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

## API Endpoints

### Health Check

```
GET /health
```

Returns server status and number of loaded models.

### Get Available Models

```
GET /models
```

Returns list of loaded models with performance metrics.

### Predict Property Price

```
POST /predict
```

Predicts property price using ensemble of models with LangGraph analysis.

**Request Body:**

```json
{
  "location": "Bangalore, Koramangala",
  "area": 1200.0,
  "bedrooms": 3,
  "bathrooms": 2,
  "age": 5,
  "furnished": true,
  "amenities": {
    "parking": true,
    "garden": false,
    "pool": true,
    "gym": true
  }
}
```

**Response:**

```json
{
  "ensemble_prediction": 7250000.0,
  "formatted_price": "₹72,50,000",
  "confidence": "89%",
  "individual_predictions": [...],
  "insights": [...],
  "prediction_range": {...},
  "model_summary": {...},
  "timestamp": "2025-10-09T..."
}
```

### Get Model Summary

```
GET /summary
```

Returns comprehensive analysis of all models using LangGraph.

## Model Architecture

### Top 5 Models Used:

1. **Extra Trees Regressor** (Primary) - 40% weight
2. **Random Forest** - 25% weight
3. **Decision Tree** - 15% weight
4. **LightGBM** - 15% weight
5. **Alternative Extra Trees** - 5% weight

### LangGraph Workflow:

1. **Performance Analysis** - Analyzes model metrics and rankings
2. **Insight Generation** - Creates intelligent insights based on predictions
3. **Summary Creation** - Generates comprehensive analysis reports
4. **Recommendations** - Provides actionable recommendations

## Features in Detail

### Ensemble Prediction

- Weighted average of top 5 models
- Confidence scoring based on prediction variance
- Individual model predictions for transparency

### LangGraph Analysis

- Automated workflow for intelligent analysis
- Context-aware insights generation
- Performance-based model ranking
- Actionable recommendations

### Error Handling

- Comprehensive error handling and logging
- Graceful fallbacks for missing models
- Input validation and sanitization

## Development

### Project Structure

```
backend/
├── fastapi_app.py          # Main FastAPI application
├── start_server.py         # Server launcher script
├── requirements.txt        # Python dependencies
└── README.md              # This file
```

### Adding New Models

1. Save model file in `../ensemble_learning/saved_models/`
2. Update model mapping in `fastapi_app.py`
3. Add to model weights configuration
4. Update performance data

### Extending LangGraph Workflow

1. Add new analysis nodes in `create_analysis_graph()`
2. Update state transitions
3. Modify insight generation logic

## Troubleshooting

### Common Issues

**Models not loading:**

- Check file paths in `MODEL_DIR`
- Verify model files exist and are readable
- Check scikit-learn version compatibility

**Prediction errors:**

- Verify input data format
- Check feature preprocessing pipeline
- Ensure scaler is loaded correctly

**LangGraph errors:**

- Verify langgraph installation
- Check state type definitions
- Review workflow configuration

### Logs

Server logs include:

- Model loading status
- Prediction requests and responses
- Error details and stack traces
- Performance metrics

## Production Deployment

### Environment Variables

```bash
export MODEL_DIR="/path/to/models"
export API_HOST="0.0.0.0"
export API_PORT="8000"
```

### Docker Deployment

```dockerfile
FROM python:3.9-slim
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn", "fastapi_app:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Performance Optimization

- Use gunicorn with multiple workers
- Implement model caching
- Add request rate limiting
- Monitor memory usage

## API Documentation

Once the server is running, visit http://localhost:8000/docs for interactive API documentation powered by Swagger UI.

## Support

For issues and questions:

1. Check the troubleshooting section
2. Review server logs for error details
3. Verify model files and dependencies
4. Test with the health check endpoint
