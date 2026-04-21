@echo off
echo ============================================================
echo    NUTRICARE AI - SHOW ALL OUTPUTS
echo ============================================================
echo.

echo [1/5] Opening ML Model Comparison (HTML Dashboard)...
start backend\ml\model_comparison.html
timeout /t 2 /nobreak >nul

echo [2/5] Opening ML Model Comparison (PNG Chart)...
start backend\ml\model_comparison.png
timeout /t 2 /nobreak >nul

echo [3/5] Opening Frontend Dashboard...
start frontend\dashboard.html
timeout /t 2 /nobreak >nul

echo [4/5] Running Model Comparison (Console Output)...
echo.
cd backend\ml
python compare_models.py
cd ..\..
echo.

echo [5/5] Testing Backend API...
echo.
echo Starting Flask server in background...
echo Please wait 5 seconds for server to start...
start /B python backend\app.py
timeout /t 5 /nobreak >nul

echo.
echo Testing API endpoint...
curl -X GET http://127.0.0.1:5000/
echo.
echo.

echo ============================================================
echo    ALL OUTPUTS DISPLAYED!
echo ============================================================
echo.
echo What's Open:
echo   - ML Comparison Dashboard (Browser)
echo   - ML Comparison Chart (Image Viewer)
echo   - Frontend Dashboard (Browser)
echo   - Console Output (This Window)
echo   - Backend API (Running in Background)
echo.
echo To test the full workflow:
echo   1. Go to the Frontend Dashboard
echo   2. Enter health data
echo   3. Click "Analyze Health"
echo   4. Click "Get Diet Plan"
echo.
echo Press any key to stop the backend server...
pause >nul

echo.
echo Stopping backend server...
taskkill /F /IM python.exe /FI "WINDOWTITLE eq *app.py*" 2>nul
echo.
echo Done!
pause
