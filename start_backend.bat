@echo off
echo ================================================
echo   Real Estate Price Predictor - Backend Server
echo ================================================
echo.

cd backend

echo Checking Python virtual environment...
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

echo Activating virtual environment...
call venv\Scripts\activate.bat

echo Installing/Updating dependencies...
pip install -r requirements.txt --quiet

echo.
echo ================================================
echo   Starting FastAPI Server on port 8000
echo ================================================
echo   API Documentation: http://localhost:8000/docs
echo   Health Check: http://localhost:8000/health
echo ================================================
echo.

uvicorn main:app --host 0.0.0.0 --port 8000 --reload

pause
