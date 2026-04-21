# 🚀 QUICK START GUIDE

## Step 1: Install Python Dependencies

Open Command Prompt in the project folder and run:

```bash
cd backend
pip install flask firebase-admin pandas numpy scikit-learn flask-cors joblib openpyxl
```

## Step 2: Start the Server

**Option A: Double-click**
- Double-click `start_server.bat`

**Option B: Command line**
```bash
cd backend
python app.py
```

You should see:
```
Firebase disabled: No credentials found
 * Running on http://127.0.0.1:5000
```

## Step 3: Open Dashboard

**Option A: Live Server (Recommended)**
1. Install "Live Server" extension in VS Code
2. Right-click `frontend/dashboard.html`
3. Select "Open with Live Server"

**Option B: Direct Open**
- Double-click `frontend/dashboard.html`

## Step 4: Test the Dashboard

### Pregnancy View:
1. Enter sample data:
   - Age: 28
   - Systolic BP: 120
   - Diastolic BP: 80
   - Blood Sugar: 7.5
   - Body Temp: 98.6
   - Heart Rate: 75

2. Click "Analyze Health"

3. You'll see:
   - ✅ Health status summary
   - ✅ Risk level (Low/Medium/High)
   - ✅ Nutritional deficiencies
   - ✅ Health alerts
   - ✅ Personalized diet plan
   - ✅ Nutrition chart
   - ✅ AI food recommendations

### Post-Pregnancy View:
1. Click "Post-Pregnancy" button at top
2. View:
   - Mother recovery nutrition
   - Breastfeeding guidelines
   - Baby feeding planner

## 🎯 Sample Test Cases

**Low Risk Patient:**
- Age: 25
- BP: 115/75
- Blood Sugar: 6.5
- Temp: 98.6
- Heart Rate: 72

**Medium Risk Patient:**
- Age: 30
- BP: 125/82
- Blood Sugar: 7.8
- Temp: 98.8
- Heart Rate: 80

**High Risk Patient:**
- Age: 35
- BP: 140/95
- Blood Sugar: 9.5
- Temp: 99.2
- Heart Rate: 95

## ❌ Troubleshooting

### Backend not starting?
- Make sure Python is installed
- Install all dependencies: `pip install -r backend/requirements.txt`
- Check if port 5000 is free

### CORS Error?
- Make sure backend is running
- Check console for errors
- Verify API_BASE_URL in dashboard.js is "http://127.0.0.1:5000"

### Model not found?
```bash
cd backend/ml
python train_model.py
```

## 📱 Features Overview

### 🤰 Pregnancy Dashboard
- Real-time health monitoring
- AI risk prediction
- Nutritional gap analysis
- Smart alerts
- Weekly/Monthly diet plans
- Progress tracking
- Food recommendations

### 👶 Post-Pregnancy Dashboard
- Recovery nutrition guide
- Breastfeeding nutrition
- Baby feeding by age (0-2 years)
- Sample meal plans

## 🎨 Dashboard Highlights

✨ **Modern UI** - Clean, professional design
📊 **Charts** - Visual nutrition tracking
🤖 **AI-Powered** - Smart recommendations
📱 **Responsive** - Works on all devices
🎯 **Medical Focus** - Evidence-based nutrition

## 🔥 Next Steps

1. ✅ Test with different health data
2. ✅ Explore both dashboard views
3. ✅ Try weekly vs monthly diet plans
4. ✅ Check AI recommendations
5. ✅ View nutrition progress charts

## 💡 Tips

- Use realistic health values
- Try different risk levels
- Switch between weekly/monthly plans
- Explore post-pregnancy features
- Check the nutrition chart updates

## 📞 Need Help?

Check the main README.md for detailed documentation!

---

**Enjoy using NutriCare AI! 🎉**
