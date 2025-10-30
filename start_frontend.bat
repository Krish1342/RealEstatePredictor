@echo off
echo ================================================
echo   Real Estate Price Predictor - Frontend
echo ================================================
echo.

cd frontend

echo Checking Node modules...
if not exist "node_modules" (
    echo Installing dependencies...
    call npm install
) else (
    echo Dependencies already installed.
)

echo.
echo ================================================
echo   Starting React Development Server
echo ================================================
echo   Frontend: http://localhost:5173
echo   Connecting to API: http://localhost:8000
echo ================================================
echo.

call npm run dev

pause
