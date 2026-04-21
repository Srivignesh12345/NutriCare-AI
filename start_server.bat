@echo off
echo ========================================
echo  NutriCare AI - Starting Backend Server
echo ========================================
echo.

cd backend

echo Checking if ML model exists...
if not exist "ml\model.pkl" (
    echo Model not found! Training model...
    cd ml
    python train_model.py
    cd ..
    echo.
)

echo Starting Flask server...
echo Server will run at: http://127.0.0.1:5000
echo.
echo Press Ctrl+C to stop the server
echo ========================================
echo.

python app.py

pause
