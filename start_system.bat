@echo off
echo ================================================
echo   Real Estate Price Predictor - Full System
echo ================================================
echo.
echo Starting Backend and Frontend servers...
echo.

REM Start Backend in new window
start "Backend Server" cmd /k "cd /d %~dp0 && start_backend.bat"

REM Wait 5 seconds for backend to start
timeout /t 5 /nobreak

REM Start Frontend in new window
start "Frontend Server" cmd /k "cd /d %~dp0 && start_frontend.bat"

echo.
echo ================================================
echo   Servers are starting in separate windows
echo ================================================
echo   Backend API: http://localhost:8000
echo   API Docs: http://localhost:8000/docs
echo   Frontend: http://localhost:5173
echo ================================================
echo.
echo Close this window when done.
echo Press any key to exit this launcher...
pause > nul
