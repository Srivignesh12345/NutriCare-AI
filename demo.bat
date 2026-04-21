@echo off
color 0A
title NutriCare AI - Complete Demo

:MENU
cls
echo.
echo ============================================================
echo           NUTRICARE AI - OUTPUT DEMONSTRATION
echo ============================================================
echo.
echo Select what you want to see:
echo.
echo  [1] ML Model Comparison (HTML Dashboard)
echo  [2] ML Model Comparison (PNG Chart)
echo  [3] Run Model Comparison (Console Output)
echo  [4] Start Backend API Server
echo  [5] Open Frontend Dashboard
echo  [6] Show All Outputs (Automated)
echo  [7] Quick Test Workflow
echo  [8] View Documentation
echo  [0] Exit
echo.
echo ============================================================
set /p choice="Enter your choice (0-8): "

if "%choice%"=="1" goto ML_HTML
if "%choice%"=="2" goto ML_PNG
if "%choice%"=="3" goto ML_CONSOLE
if "%choice%"=="4" goto BACKEND
if "%choice%"=="5" goto FRONTEND
if "%choice%"=="6" goto ALL_OUTPUTS
if "%choice%"=="7" goto WORKFLOW
if "%choice%"=="8" goto DOCS
if "%choice%"=="0" goto EXIT
goto MENU

:ML_HTML
cls
echo.
echo [Opening ML Model Comparison Dashboard...]
echo.
start backend\ml\model_comparison.html
echo ✅ Opened in browser!
echo.
echo You should see:
echo   - Performance metrics table
echo   - Decision Tree: 100%% accuracy
echo   - Random Forest: 98%% accuracy
echo   - Logistic Regression: 93%% accuracy
echo   - Visual comparison charts
echo.
pause
goto MENU

:ML_PNG
cls
echo.
echo [Opening ML Model Comparison Chart...]
echo.
start backend\ml\model_comparison.png
echo ✅ Opened in image viewer!
echo.
echo You should see 6 visualizations:
echo   1. Bar chart - All metrics comparison
echo   2. Accuracy comparison
echo   3. Decision Tree confusion matrix
echo   4. Random Forest confusion matrix
echo   5. Logistic Regression confusion matrix
echo   6. Radar chart - Multi-metric view
echo.
pause
goto MENU

:ML_CONSOLE
cls
echo.
echo [Running Model Comparison...]
echo.
cd backend\ml
python compare_models.py
cd ..\..
echo.
echo ✅ Comparison complete!
echo.
pause
goto MENU

:BACKEND
cls
echo.
echo [Starting Backend API Server...]
echo.
echo Server will run on: http://127.0.0.1:5000
echo.
echo Press CTRL+C to stop the server
echo.
cd backend
python app.py
cd ..
pause
goto MENU

:FRONTEND
cls
echo.
echo [Opening Frontend Dashboard...]
echo.
start frontend\dashboard.html
echo ✅ Opened in browser!
echo.
echo You should see:
echo   - Health input form
echo   - Pregnancy/Post-Pregnancy tabs
echo   - Analyze Health button
echo.
echo NOTE: Make sure backend is running (Option 4)
echo.
pause
goto MENU

:ALL_OUTPUTS
cls
echo.
echo [Opening All Outputs...]
echo.
echo Step 1/5: ML Comparison Dashboard...
start backend\ml\model_comparison.html
timeout /t 2 /nobreak >nul

echo Step 2/5: ML Comparison Chart...
start backend\ml\model_comparison.png
timeout /t 2 /nobreak >nul

echo Step 3/5: Frontend Dashboard...
start frontend\dashboard.html
timeout /t 2 /nobreak >nul

echo Step 4/5: Running Console Comparison...
echo.
cd backend\ml
python compare_models.py
cd ..\..
echo.

echo Step 5/5: Starting Backend Server...
echo.
echo Backend will start in a new window...
start cmd /k "cd backend && python app.py"
echo.

echo ============================================================
echo ✅ ALL OUTPUTS OPENED!
echo ============================================================
echo.
echo What's now available:
echo   ✓ ML Comparison Dashboard (Browser)
echo   ✓ ML Comparison Chart (Image)
echo   ✓ Frontend Dashboard (Browser)
echo   ✓ Backend API (New Window)
echo   ✓ Console Output (This Window)
echo.
echo Next: Go to Frontend Dashboard and test the workflow!
echo.
pause
goto MENU

:WORKFLOW
cls
echo.
echo ============================================================
echo              QUICK TEST WORKFLOW GUIDE
echo ============================================================
echo.
echo STEP 1: Start Backend
echo ─────────────────────────────────────────
echo   Press any key to start backend server...
pause >nul
start cmd /k "cd backend && python app.py"
echo   ✅ Backend starting in new window...
echo   ⏳ Waiting 5 seconds for server to start...
timeout /t 5 /nobreak >nul
echo.

echo STEP 2: Open Frontend
echo ─────────────────────────────────────────
start frontend\dashboard.html
echo   ✅ Frontend opened in browser
echo.

echo STEP 3: Test Analysis
echo ─────────────────────────────────────────
echo   In the browser, enter these values:
echo.
echo   • Age: 28
echo   • Systolic BP: 120
echo   • Diastolic BP: 80
echo   • Blood Sugar: 7.5
echo   • Body Temp: 98.6
echo   • Heart Rate: 75
echo.
echo   Then click "Analyze Health"
echo   Expected Result: Risk = "Medium"
echo.
pause

echo STEP 4: Get Diet Plan
echo ─────────────────────────────────────────
echo   Click "Get Weekly Diet Plan" button
echo   Expected Result: 7-day meal plan displayed
echo.
pause

echo STEP 5: View ML Comparison
echo ─────────────────────────────────────────
start backend\ml\model_comparison.html
echo   ✅ ML Comparison opened
echo   Expected Result: Decision Tree = 100%% accuracy
echo.
echo ============================================================
echo ✅ WORKFLOW COMPLETE!
echo ============================================================
echo.
pause
goto MENU

:DOCS
cls
echo.
echo [Opening Documentation...]
echo.
start OUTPUT_GUIDE.md
timeout /t 1 /nobreak >nul
start QUICK_REFERENCE.txt
timeout /t 1 /nobreak >nul
start README.md
echo.
echo ✅ Documentation opened!
echo.
echo Files opened:
echo   - OUTPUT_GUIDE.md (Complete guide)
echo   - QUICK_REFERENCE.txt (Quick reference)
echo   - README.md (Project overview)
echo.
pause
goto MENU

:EXIT
cls
echo.
echo ============================================================
echo              Thank you for using NutriCare AI!
echo ============================================================
echo.
echo Cleaning up...
echo.
echo If backend is still running, close the server window manually.
echo.
timeout /t 2 /nobreak >nul
exit

