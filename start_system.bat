@echo off
echo ==============================================
echo   Real Estate Predictor - Full Stack Setup
echo ==============================================
echo.

:: Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed or not in PATH
    echo Please install Python 3.8 or higher
    pause
    exit /b 1
)

:: Check if Node.js is installed
node --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Node.js is not installed or not in PATH
    echo Please install Node.js 16 or higher
    pause
    exit /b 1
)

echo ✅ Python and Node.js are available
echo.

:: Setup Backend
echo 🔧 Setting up FastAPI Backend...
cd backend
if not exist "venv" (
    echo Creating Python virtual environment...
    python -m venv venv
)

echo Activating virtual environment...
call venv\Scripts\activate.bat

echo Installing Python dependencies...
pip install -r requirements.txt

if errorlevel 1 (
    echo ❌ Failed to install Python dependencies
    pause
    exit /b 1
)

echo ✅ Backend dependencies installed
echo.

:: Setup Frontend
echo 🔧 Setting up React Frontend...
cd ..\UI

echo Installing Node.js dependencies...
npm install

if errorlevel 1 (
    echo ❌ Failed to install Node.js dependencies
    pause
    exit /b 1
)

echo ✅ Frontend dependencies installed
echo.

:: Start services
echo 🚀 Starting Real Estate Predictor...
echo.
echo Starting FastAPI backend on port 8000...
start "FastAPI Backend" cmd /k "cd /d %~dp0backend && venv\Scripts\activate && python start_server.py"

timeout /t 3 /nobreak >nul

echo Starting React frontend on port 3000...
start "React Frontend" cmd /k "cd /d %~dp0UI && npm run dev"

echo.
echo ==============================================
echo   🎉 Real Estate Predictor Started!
echo ==============================================
echo.
echo 📡 Backend API: http://localhost:8000
echo 📊 API Docs: http://localhost:8000/docs
echo 🖥️  Frontend: http://localhost:5173
echo.
echo Press any key to close this window...
pause >nul