# 🎯 COMPLETE OUTPUT GUIDE - NutriCare AI

This guide shows you how to see ALL outputs from the NutriCare AI project.

---

## 📊 OUTPUT 1: ML MODEL COMPARISON (Already Generated)

### View Method 1: HTML Dashboard
1. Navigate to: `backend/ml/`
2. Double-click: `model_comparison.html`
3. Opens in browser with:
   - Performance metrics table
   - Visual comparison charts
   - Key insights

### View Method 2: PNG Image
1. Navigate to: `backend/ml/`
2. Open: `model_comparison.png`
3. Shows 6 visualizations:
   - Bar chart (all metrics)
   - Accuracy comparison
   - 3 Confusion matrices
   - Radar chart

### Command Line View:
```bash
cd backend/ml
start model_comparison.html
```

**What You'll See:**
- Decision Tree: 100% accuracy ✅
- Random Forest: 98% accuracy
- Logistic Regression: 93% accuracy

---

## 🔬 OUTPUT 2: ML MODEL TRAINING RESULTS

### Run Training:
```bash
cd backend/ml
python train_model.py
```

**Output:**
```
ML model trained successfully
```

**Files Created:**
- `model.pkl` - Trained Decision Tree model
- `label_encoder.pkl` - Risk level encoder

---

## 📈 OUTPUT 3: MODEL COMPARISON (Console)

### Run Comparison:
```bash
cd backend/ml
python compare_models.py
```

**Output Shows:**
```
============================================================
ML MODEL COMPARISON - MATERNAL HEALTH RISK PREDICTION
============================================================

Dataset Info:
   Total samples: 500
   Training samples: 400
   Testing samples: 100
   Risk levels: ['High', 'Low', 'Medium']

============================================================
MODEL 1: DECISION TREE CLASSIFIER
============================================================
Accuracy:  1.0000 (100.00%)
Precision: 1.0000
Recall:    1.0000
F1-Score:  1.0000

============================================================
MODEL 2: RANDOM FOREST CLASSIFIER
============================================================
Accuracy:  0.9800 (98.00%)
Precision: 0.9701
Recall:    0.9800
F1-Score:  0.9750

============================================================
MODEL 3: LOGISTIC REGRESSION
============================================================
Accuracy:  0.9300 (93.00%)
Precision: 0.9113
Recall:    0.9300
F1-Score:  0.9125

============================================================
COMPARISON SUMMARY
============================================================

              Model  Accuracy  Precision  Recall  F1-Score
      Decision Tree      1.00    1.00000    1.00  1.000000
      Random Forest      0.98    0.97011    0.98  0.975028
Logistic Regression      0.93    0.91125    0.93  0.912506

============================================================
*** BEST MODEL: Decision Tree ***
   Accuracy: 1.0000 (100.00%)
============================================================
```

---

## 🌐 OUTPUT 4: BACKEND API (Flask Server)

### Start Backend:
```bash
cd backend
python app.py
```

**Output:**
```
 * Serving Flask app 'app'
 * Debug mode: off
WARNING: This is a development server.
 * Running on http://0.0.0.0:5000
Press CTRL+C to quit
```

### Test API Endpoints:

#### 1. Health Check:
Open browser: `http://127.0.0.1:5000/`

**Output:**
```json
{
  "status": "running",
  "service": "Maternal Nutrition AI Backend"
}
```

#### 2. Analyze Health (POST):
Use Postman or curl:
```bash
curl -X POST http://127.0.0.1:5000/analyze ^
  -H "Content-Type: application/json" ^
  -d "{\"age\":28,\"systolicbp\":120,\"diastolicbp\":80,\"bs\":7.5,\"bodytemp\":98.6,\"heartrate\":75}"
```

**Output:**
```json
{
  "risk": "Medium",
  "message": "Predicted maternal health risk: Medium"
}
```

#### 3. Diet Plan (POST):
```bash
curl -X POST http://127.0.0.1:5000/diet-plan ^
  -H "Content-Type: application/json" ^
  -d "{\"risk\":\"Medium\",\"duration\":\"week\"}"
```

**Output:**
```json
{
  "risk": "Medium",
  "duration": "week",
  "diet_plan": {
    "Day 1": {
      "Breakfast": "Milk + Dates",
      "Lunch": "Brown Rice + Dal + Spinach",
      "Dinner": "Soup + Salad",
      "Note": "Balanced nutrition recommended"
    },
    "Day 2": { ... },
    ...
  },
  "generated_at": "2026-04-03T08:30:00.000000"
}
```

---

## 🎨 OUTPUT 5: FRONTEND DASHBOARD (Main Application)

### Method 1: Direct Open
1. Navigate to: `frontend/`
2. Double-click: `dashboard.html`
3. Or open: `index.html` (auto-redirects)

### Method 2: Live Server (VS Code)
1. Right-click `dashboard.html`
2. Select "Open with Live Server"
3. Opens at: `http://127.0.0.1:5500/frontend/dashboard.html`

### Method 3: Command Line
```bash
cd frontend
start dashboard.html
```

### What You'll See:

#### Pregnancy View:
1. **Input Form:**
   - Age, Blood Pressure, Blood Sugar
   - Body Temperature, Heart Rate
   - Duration selector (Week/Month)

2. **After Clicking "Analyze Health":**
   - Risk Level (Low/Medium/High)
   - Health status message
   - "Get Diet Plan" button

3. **After Clicking "Get Diet Plan":**
   - Day-by-day meal plan
   - Breakfast, Lunch, Dinner
   - Nutritional notes

#### Post-Pregnancy View:
- Mother recovery nutrition
- Breastfeeding guidelines
- Baby feeding plans (0-2 years)
- Stage-wise meal suggestions

---

## 🧪 OUTPUT 6: SAMPLE TEST CASES

### Test Case 1: Low Risk
**Input:**
```json
{
  "age": 25,
  "systolicbp": 115,
  "diastolicbp": 75,
  "bs": 6.5,
  "bodytemp": 98.6,
  "heartrate": 72
}
```
**Expected Output:** Risk = "Low"

### Test Case 2: Medium Risk
**Input:**
```json
{
  "age": 30,
  "systolicbp": 125,
  "diastolicbp": 82,
  "bs": 7.8,
  "bodytemp": 98.8,
  "heartrate": 80
}
```
**Expected Output:** Risk = "Medium"

### Test Case 3: High Risk
**Input:**
```json
{
  "age": 35,
  "systolicbp": 140,
  "diastolicbp": 95,
  "bs": 9.5,
  "bodytemp": 99.2,
  "heartrate": 95
}
```
**Expected Output:** Risk = "High"

---

## 📸 COMPLETE DEMO WORKFLOW

### Step-by-Step Full Demo:

1. **Start Backend:**
   ```bash
   cd backend
   python app.py
   ```
   ✅ See: Server running message

2. **Open Frontend:**
   ```bash
   cd frontend
   start dashboard.html
   ```
   ✅ See: Dashboard UI

3. **Test Analysis:**
   - Enter test data (Age: 28, BP: 120/80, BS: 7.5, Temp: 98.6, HR: 75)
   - Click "Analyze Health"
   ✅ See: Risk level prediction

4. **Get Diet Plan:**
   - Click "Get Weekly Diet Plan"
   ✅ See: 7-day meal plan

5. **View ML Comparison:**
   ```bash
   cd backend/ml
   start model_comparison.html
   ```
   ✅ See: Model performance charts

6. **Run Model Comparison:**
   ```bash
   cd backend/ml
   python compare_models.py
   ```
   ✅ See: Console output with metrics

---

## 📁 ALL OUTPUT FILES LOCATION

```
NutriCare-AI/
├── backend/
│   ├── ml/
│   │   ├── model.pkl                    ← Trained model
│   │   ├── label_encoder.pkl            ← Label encoder
│   │   ├── model_comparison.png         ← Visualization chart
│   │   └── model_comparison.html        ← Interactive dashboard
│   └── app.py                           ← API server (console output)
└── frontend/
    └── dashboard.html                   ← Main UI (browser output)
```

---

## 🎬 QUICK START (All Outputs in 5 Minutes)

```bash
# Terminal 1: Start Backend
cd backend
python app.py

# Terminal 2: Run Model Comparison
cd backend/ml
python compare_models.py

# Terminal 3: Open Visualizations
cd backend/ml
start model_comparison.html

# Browser: Open Dashboard
# Navigate to frontend/dashboard.html
```

---

## ✅ CHECKLIST: All Outputs Verified

- [ ] Backend API running (http://127.0.0.1:5000)
- [ ] Frontend dashboard opened
- [ ] Health analysis working
- [ ] Diet plan generation working
- [ ] Model comparison console output
- [ ] Model comparison HTML dashboard
- [ ] Model comparison PNG chart
- [ ] All 3 models trained successfully

---

## 🆘 TROUBLESHOOTING

### Backend Not Reachable:
```bash
# Check if port 5000 is free
netstat -ano | findstr :5000

# If blocked, change port in app.py to 5001
```

### Frontend Not Connecting:
- Ensure backend is running first
- Check console for CORS errors
- Verify API_BASE_URL in dashboard.js

### Visualization Not Showing:
```bash
# Reinstall dependencies
cd backend
python -m pip install matplotlib seaborn openpyxl
```

---

## 📞 SUMMARY

**Total Outputs Available:**
1. ✅ ML Model Comparison (HTML + PNG)
2. ✅ Console Training Results
3. ✅ Backend API Responses (JSON)
4. ✅ Frontend Dashboard (Interactive UI)
5. ✅ Diet Plans (JSON + UI)
6. ✅ Risk Predictions (JSON + UI)

**All outputs are ready to view!**
