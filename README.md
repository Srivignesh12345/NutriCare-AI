# 🤰 NutriCare AI - Maternal & Child Nutrition Dashboard

AI-Driven Nutrition Planning for Mothers and Children with ML-powered health risk prediction.

## 🎯 Features

### Pregnancy Dashboard
- ✅ Health Status Monitoring (BP, Blood Sugar, Heart Rate, etc.)
- ✅ AI Risk Assessment (Low/Medium/High)
- ✅ Nutritional Deficiency Analysis
- ✅ Smart Health Alerts
- ✅ Personalized Diet Plans (Weekly/Monthly)
- ✅ Daily Exercise Recommendations (NEW!)
- ✅ Nutrition Progress Charts
- ✅ AI-Powered Food Recommendations
- ✅ **Food Intake Tracker with Image Upload (NEW!)**

### Post-Pregnancy Dashboard
- ✅ Mother Recovery Nutrition Guide
- ✅ Breastfeeding Nutrition Plan
- ✅ Baby Feeding Planner (0-2 years)
- ✅ Stage-wise Baby Meal Plans

## 🚀 Quick Start

### 1. Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 2. Train ML Model (First Time Only)

```bash
cd backend/ml
python train_model.py
```

This will create:
- `model.pkl` - Trained Decision Tree model
- `label_encoder.pkl` - Label encoder for risk levels

### 3. Start Backend Server

```bash
cd backend
python app.py
```

Server runs at: `http://127.0.0.1:5000`

### 4. Open Dashboard

Open `frontend/dashboard.html` in your browser

Or use Live Server in VS Code:
- Right-click on `dashboard.html`
- Select "Open with Live Server"

Or simply open `frontend/index.html` (auto-redirects to dashboard)

## 📸 Food Intake Tracker (NEW!)

### Track Your Daily Meals
1. Click "Food Tracker" button in dashboard
2. Upload photos of your meals (Breakfast, Lunch, Dinner)
3. Or type what you ate
4. Click "Analyze My Food Intake"
5. View:
   - Detected foods from images
   - Total nutrition summary
   - Personalized recommendations

### Features:
- 📸 Image upload for 3 meals
- ✍️ Text input option
- 🤖 AI food recognition
- 📊 Nutrition calculation
- 💡 Smart recommendations

See [FOOD_TRACKER_README.md](FOOD_TRACKER_README.md) for detailed guide.

## 📊 Dashboard Views

### Pregnancy View
1. Enter health metrics (Age, BP, Blood Sugar, etc.)
2. Click "Analyze Health"
3. View:
   - Health status summary
   - AI risk assessment
   - Nutritional deficiencies
   - Health alerts
   - Personalized diet plan
   - Nutrition progress chart
   - AI food recommendations

### Post-Pregnancy View
- Mother recovery nutrition guide
- Breastfeeding nutrition requirements
- Baby feeding guidelines by age
- Sample baby meal plans

## 🧠 AI Features

### 1. Risk Prediction
- Uses Decision Tree ML model
- Predicts: Normal/Medium/High risk
- Based on 6 health parameters

### 2. Deficiency Detection
- Estimates nutrient intake from health data
- Compares with pregnancy standards
- Highlights deficiencies

### 3. Smart Recommendations
- Iron-rich foods for high risk
- Blood sugar control foods
- Blood pressure management
- Pregnancy-specific nutrition

### 4. Personalized Diet Plans
- Adapts to risk level
- Weekly or monthly plans
- Balanced meal suggestions
- Daily exercise recommendations (pregnancy-safe)

## 📁 Project Structure

```
NutriCare-AI/
├── backend/
│   ├── app.py                 # Flask API
│   ├── diet_engine.py         # Diet plan generator
│   ├── diet_rules.py          # Diet rules logic
│   ├── nutrition_engine.py    # Nutrition calculator
│   ├── nutrition_rules.py     # Nutrition standards
│   ├── recommender.py         # Food recommender
│   ├── requirements.txt       # Python dependencies
│   ├── ml/
│   │   ├── train_model.py     # ML model training
│   │   ├── model.pkl          # Trained model
│   │   └── label_encoder.pkl  # Label encoder
│   └── datasets/
│       └── nutrition_foods.csv
├── frontend/
│   ├── dashboard.html         # Main dashboard UI
│   ├── dashboard.css          # Dashboard styles
│   ├── dashboard.js           # Dashboard logic
│   └── index.html             # Redirects to dashboard
└── README.md
```

## 🔧 API Endpoints

### POST /analyze
Analyzes health data and predicts risk level

**Request:**
```json
{
  "age": 28,
  "systolicbp": 120,
  "diastolicbp": 80,
  "bs": 7.5,
  "bodytemp": 98.6,
  "heartrate": 75
}
```

**Response:**
```json
{
  "risk": "Medium",
  "message": "Predicted maternal health risk: Medium"
}
```

### POST /diet-plan
Generates personalized diet plan

**Request:**
```json
{
  "risk": "Medium",
  "duration": "week"
}
```

**Response:**
```json
{
  "risk": "Medium",
  "duration": "week",
  "diet_plan": {
    "Day 1": {
      "Breakfast": "Milk + Dates",
      "Lunch": "Brown Rice + Dal + Spinach",
      "Dinner": "Soup + Salad",
      "Exercise": "Brisk Walking - 20 minutes (morning)",
      "Note": "Balanced nutrition recommended"
    }
  }
}
```

### POST /recommendations
Get AI food recommendations

**Request:**
```json
{
  "risk": "High",
  "bs": 8.5,
  "systolicbp": 135
}
```

## 🎨 Technologies Used

### Backend
- Flask (REST API)
- scikit-learn (ML)
- pandas, numpy (Data processing)
- Firebase Admin (Optional database)

### Frontend
- HTML5, CSS3, JavaScript
- Chart.js (Nutrition charts)
- Responsive design

### ML Model
- Decision Tree Classifier
- Features: Age, BP, Blood Sugar, Body Temp, Heart Rate
- Output: Low/Medium/High risk

## 🔐 Firebase Setup (Optional)

1. Create Firebase project
2. Download service account key
3. Set environment variable:
```bash
export GOOGLE_APPLICATION_CREDENTIALS="path/to/key.json"
```

## 📝 Sample Test Data

**Normal Risk:**
- Age: 20, BP: 100/60, BS: 6.0, Temp: 98.0, HR: 70

**Medium Risk:**
- Age: 28, BP: 120/80, BS: 7.5, Temp: 98.6, HR: 75

**High Risk:**
- Age: 35, BP: 140/95, BS: 9.5, Temp: 99.2, HR: 95

## 🚀 Deployment

### Backend (Render/Heroku)
1. Push code to GitHub
2. Connect to Render/Heroku
3. Set environment variables
4. Deploy

### Frontend (Netlify/Vercel)
1. Update API_BASE_URL in dashboard.js
2. Deploy frontend folder
3. Done!

## 📈 Future Enhancements

- [ ] User authentication
- [ ] Historical data tracking
- [ ] PDF report generation
- [ ] WhatsApp/SMS alerts
- [ ] Multi-language support
- [ ] Mobile app
- [ ] Doctor consultation integration

## 👨‍💻 Developer

Built with ❤️ for maternal and child health

## 📄 License

MIT License
