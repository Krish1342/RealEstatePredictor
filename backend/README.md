# FastAPI Backend - Real Estate Predictor

A high-performance FastAPI backend for real estate price prediction using ensemble machine learning models.

## Features

- **Ensemble ML Models**: Top 5 performing models (Extra Trees, Random Forest, Decision Tree, LightGBM, XGBoost)
- **Weighted Predictions**: Performance-based model weighting
- **RESTful API**: Clean, documented endpoints
- **Auto Documentation**: Swagger UI at `/docs`
- **Health Monitoring**: Built-in health check endpoint
- **CORS Enabled**: Ready for frontend integration

## Quick Start

### Installation

```powershell
# Create virtual environment
python -m venv venv

# Activate virtual environment
.\venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Running the Server

```powershell
# Development mode (with auto-reload)
python main.py

# Or using uvicorn directly
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## API Endpoints

### Health Check

```
GET /health
```

### Predict Price

```
POST /predict
```

**Request Body:**

```json
{
  "BHK": 3,
  "Size_in_SqFt": 1500,
  "Year_Built": 2015,
  "Floor_No": 5,
  "Total_Floors": 15,
  "Nearby_Schools": 3,
  "Nearby_Hospitals": 2,
  "Furnished_Status": "Semi-Furnished",
  "Public_Transport_Accessibility": "Good",
  "Parking_Space": "Yes",
  "Security": "Yes",
  "Availability_Status": "Ready to Move",
  "Baths": 2,
  "balcony": "Yes",
  "location": "Koramangala",
  "Property_Type": "Apartment",
  "Facing": "East",
  "Owner_Type": "Primary"
}
```

**Response:**

```json
{
  "ensemble_prediction": 7250000.0,
  "formatted_price": "₹72.50 Lakhs",
  "confidence": "92.5%",
  "individual_predictions": [...],
  "insights": [...],
  "prediction_range": {...},
  "feature_importance": [...],
  "model_performance": {...}
}
```

### Get Models Info

```
GET /models
```

### Get Features List

```
GET /features
```

## API Documentation

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Model Information

The backend uses 5 ensemble models with the following weights:

| Model         | Weight | R² Score | MAE     | RMSE     |
| ------------- | ------ | -------- | ------- | -------- |
| Extra Trees   | 40%    | 0.999999 | 130.67  | 1004.53  |
| Random Forest | 25%    | 0.999999 | 262.83  | 1866.99  |
| Decision Tree | 15%    | 0.999998 | 338.73  | 3252.90  |
| LightGBM      | 15%    | 0.999992 | 1677.42 | 6988.41  |
| XGBoost       | 5%     | 0.999942 | 7009.06 | 18394.10 |

## Environment Variables

Create a `.env` file in the backend directory:

```env
# API Configuration
API_HOST=0.0.0.0
API_PORT=8000
API_RELOAD=True

# Model Configuration
MODEL_DIR=../ensemble_learning/saved_models
```

## Error Handling

The API includes comprehensive error handling:

- 503: Service Unavailable (models not loaded)
- 500: Internal Server Error (prediction failures)
- 422: Validation Error (invalid input)

## Logging

Logs are output to console with INFO level by default. Configure logging in `main.py`.

## Development

```powershell
# Install dev dependencies
pip install pytest httpx

# Run tests (when implemented)
pytest

# Format code
black main.py
```

## Production Deployment

For production, use a production ASGI server:

```powershell
# Using Gunicorn (Windows compatible alternative: waitress)
pip install waitress
waitress-serve --listen=0.0.0.0:8000 main:app
```

## Troubleshooting

**Models not loading:**

- Ensure model files exist in `ensemble_learning/saved_models/`
- Check file permissions
- Verify model file names match expected names

**CORS errors:**

- Update `allow_origins` in CORS middleware
- For production, specify exact frontend URL

**Performance issues:**

- Consider model caching
- Use async operations for I/O
- Deploy behind a reverse proxy (nginx)

## License

MIT License
