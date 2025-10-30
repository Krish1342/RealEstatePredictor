# 🚀 Quick Setup Guide - Real Estate Price Predictor

## Prerequisites Installation

### 1. Install Python (if not already installed)

- Download Python 3.8+ from https://www.python.org/downloads/
- During installation, check "Add Python to PATH"
- Verify: Open PowerShell and run `python --version`

### 2. Install Node.js (if not already installed)

- Download Node.js 16+ from https://nodejs.org/
- Install with default settings
- Verify: Open PowerShell and run `node --version`

## Project Setup

### Step 1: Extract/Clone the Project

```powershell
# If you cloned from Git
cd RealEstatePredictor

# If you extracted from ZIP
cd path\to\RealEstatePredictor
```

### Step 2: Verify Model Files

Ensure these model files exist in `ensemble_learning/saved_models/`:

- `extra_trees_model.pkl`
- `random_forest_model.pkl`
- `decision_tree_model.pkl`
- `lightgbm_model.pkl`
- `xgboost_model.pkl`
- `feature_importance.csv`
- `ensemble_learning_results.csv`

**Note**: If model files are missing, you'll need to train them first using the notebooks in `ensemble_learning/`.

### Step 3: Run the Application

#### Option A: One-Click Start (Easiest)

Simply double-click: **`start_system.bat`**

This will:

- Create Python virtual environment (first time only)
- Install all Python dependencies (first time only)
- Install all Node.js dependencies (first time only)
- Start backend server on port 8000
- Start frontend server on port 5173
- Open both in separate command windows

#### Option B: Manual Start

**Terminal 1 - Backend:**

```powershell
# Open PowerShell in project root
.\start_backend.bat
```

**Terminal 2 - Frontend:**

```powershell
# Open another PowerShell in project root
.\start_frontend.bat
```

### Step 4: Access the Application

Once both servers are running:

1. **Open your browser** and go to: **http://localhost:5173**
2. You should see the Real Estate Predictor homepage
3. The API status indicator in the navbar should show "API Online" (green dot)

### Step 5: Test the Prediction

1. Click **"Predict"** in the navigation bar
2. Fill in the property details form:
   - Select property type (e.g., Apartment)
   - Choose location (e.g., Koramangala)
   - Enter BHK (e.g., 3)
   - Enter size (e.g., 1500 sq ft)
   - Fill in other details
3. Click **"Predict Price"**
4. View the results with:
   - Predicted price
   - Confidence score
   - Price range
   - AI insights
   - Model breakdown
   - Charts and visualizations

## Troubleshooting

### Backend Issues

**"Python not recognized"**

- Ensure Python is installed and added to PATH
- Restart PowerShell after installing Python

**"No module named 'fastapi'"**

- The virtual environment might not have activated
- Manually run:
  ```powershell
  cd backend
  .\venv\Scripts\activate
  pip install -r requirements.txt
  ```

**"Model file not found"**

- Check if model files exist in `ensemble_learning/saved_models/`
- If missing, you need to train the models first

**Port 8000 already in use**

- Another application is using port 8000
- Close the other application or change the port in `backend/main.py`

### Frontend Issues

**"npm not recognized"**

- Ensure Node.js is installed
- Restart PowerShell after installing Node.js

**Port 5173 already in use**

- Change the port in `frontend/vite.config.js`:
  ```javascript
  server: {
    port: 3000;
  }
  ```

**"API Offline" in navbar**

- Ensure backend is running on port 8000
- Check backend console for errors
- Try accessing http://localhost:8000/health directly

**Blank page or errors in browser**

- Open browser console (F12) to see errors
- Ensure all dependencies installed: `npm install` in frontend folder
- Clear browser cache and reload

### General Issues

**Both servers won't start**

- Make sure you're in the project root directory
- Try running each server manually (see Option B above)
- Check the console output for specific error messages

**Slow first-time startup**

- First run installs all dependencies (Python packages ~500MB, Node modules ~200MB)
- Subsequent runs will be much faster
- This is normal and expected

## Default Credentials & Settings

- **Backend URL**: http://localhost:8000
- **Frontend URL**: http://localhost:5173
- **API Docs**: http://localhost:8000/docs
- **No authentication required** (development mode)

## Next Steps

1. **Explore the Application**:

   - Try different property configurations
   - Check the Analytics page for model performance
   - Read the About page for system details

2. **Customize**:

   - Add your own locations in `frontend/src/pages/Predict.jsx`
   - Modify colors in `frontend/tailwind.config.js`
   - Adjust model weights in `backend/main.py`

3. **Integrate Real-time Data** (Optional):
   - Sign up for free API keys (OpenWeatherMap, IQAir)
   - Add keys to backend `.env` file
   - Uncomment environmental data fetching code

## Getting Help

1. **Check Documentation**:

   - Main README: `README.md`
   - Backend README: `backend/README.md`
   - Frontend README: `frontend/README.md`

2. **Common Paths**:

   - Backend code: `backend/main.py`
   - Frontend pages: `frontend/src/pages/`
   - Models: `ensemble_learning/saved_models/`

3. **API Documentation**:

   - Swagger UI: http://localhost:8000/docs
   - Try API endpoints directly from Swagger interface

4. **Console Logs**:
   - Backend: Check the PowerShell window running backend
   - Frontend: Check browser console (F12 → Console tab)

## Video Walkthroughs (If Available)

- Setup and Installation: [Link to video]
- Making Predictions: [Link to video]
- Understanding Results: [Link to video]

---

## Success Checklist

- [ ] Python 3.8+ installed
- [ ] Node.js 16+ installed
- [ ] Project downloaded/cloned
- [ ] Model files present in `ensemble_learning/saved_models/`
- [ ] Backend started successfully (port 8000)
- [ ] Frontend started successfully (port 5173)
- [ ] Can access http://localhost:5173 in browser
- [ ] API status shows "Online" (green dot)
- [ ] Successfully made a test prediction

If all items are checked, you're ready to go! 🎉

---

**Need Help?** Open an issue on GitHub or contact support.
