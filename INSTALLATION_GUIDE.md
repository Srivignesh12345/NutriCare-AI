# 🚀 Installation & Testing Guide - Food Tracker

## Prerequisites

- Python 3.7 or higher
- pip (Python package manager)
- Modern web browser (Chrome, Firefox, Edge)
- Text editor or IDE

## Step-by-Step Installation

### Step 1: Verify Python Installation

```bash
python --version
# Should show: Python 3.7.x or higher

pip --version
# Should show pip version
```

### Step 2: Navigate to Project Directory

```bash
cd C:\Users\Admin\Desktop\NutriCare-AI
```

### Step 3: Install Backend Dependencies

```bash
cd backend
pip install -r requirements.txt
```

This will install:
- Flask (web framework)
- Flask-CORS (cross-origin support)
- Pillow (image processing) ← NEW!
- NumPy (numerical operations)
- scikit-learn (ML models)
- pandas (data processing)
- firebase-admin (optional)

### Step 4: Verify Installation

```bash
python -c "from PIL import Image; print('Pillow installed successfully!')"
```

Expected output: `Pillow installed successfully!`

### Step 5: Test the Food Recognition Module

```bash
cd ..
python test_food_tracker.py
```

Expected output:
```
🧪 FOOD TRACKER TEST SUITE

==================================================
TEST 1: Text Parsing
==================================================

Input: 2 idlis, 1 bowl sambar, 1 glass milk
Detected: [{'food': 'idli', 'quantity': 2.0}, ...]

==================================================
TEST 2: Nutrition Calculation
==================================================

Total Nutrition:
  Calories: 1650 kcal
  Protein: 58 g
  Iron: 16 mg
  Calcium: 780 mg

==================================================
TEST 3: Recommendations
==================================================

Scenario: Low Nutrition Intake
...

==================================================
✅ ALL TESTS PASSED!
==================================================
```

### Step 6: Start Backend Server

```bash
cd backend
python app.py
```

Expected output:
```
 * Serving Flask app 'app'
 * Debug mode: off
WARNING: This is a development server.
 * Running on http://127.0.0.1:5000
Press CTRL+C to quit
```

**Keep this terminal window open!**

### Step 7: Open Frontend

Open a new terminal/command prompt:

```bash
cd C:\Users\Admin\Desktop\NutriCare-AI\frontend
```

Then open in browser:
- **Option 1**: Double-click `dashboard.html`
- **Option 2**: Right-click → Open with → Chrome/Firefox
- **Option 3**: Use VS Code Live Server

### Step 8: Access Food Tracker

1. Dashboard should open automatically
2. Click the green **"Food Tracker"** button in navigation
3. Or directly open: `food-tracker.html`

---

## Testing the Food Tracker

### Test 1: Text Input Only

1. **Breakfast** text box:
   ```
   2 idlis, 1 bowl sambar, 1 glass milk
   ```

2. **Lunch** text box:
   ```
   2 chapatis, 1 bowl dal, 1 bowl spinach
   ```

3. **Dinner** text box:
   ```
   1 bowl rice, 1 bowl curry, 2 eggs
   ```

4. Click **"Analyze My Food Intake"**

5. **Expected Results**:
   - Detected Foods: Shows all items
   - Nutrition Summary: ~1650 kcal, 58g protein, 16mg iron, 780mg calcium
   - Recommendations: Suggests increasing iron and calcium

### Test 2: Image Upload Only

1. Prepare 3 food images (any food photos)
2. Click camera icon for Breakfast → Upload image
3. Click camera icon for Lunch → Upload image
4. Click camera icon for Dinner → Upload image
5. Click **"Analyze My Food Intake"**

**Expected Results**:
- Images preview immediately
- System detects foods based on colors
- Shows nutrition summary
- Provides recommendations

### Test 3: Combined (Image + Text)

1. Upload breakfast image + type "2 idlis, 1 sambar"
2. Upload lunch image + type "2 chapatis, 1 dal"
3. Upload dinner image + type "1 rice, 1 curry"
4. Click **"Analyze My Food Intake"**

**Expected Results**:
- Combines detections from both sources
- More accurate nutrition calculation
- Better recommendations

### Test 4: View Demo Results

1. Open `food-tracker-demo.html` in browser
2. See sample results without uploading
3. Understand expected output format

---

## Verification Checklist

### Backend Verification:

- [ ] Python 3.7+ installed
- [ ] All dependencies installed
- [ ] Test script passes
- [ ] Backend server starts on port 5000
- [ ] No errors in terminal

### Frontend Verification:

- [ ] Dashboard opens in browser
- [ ] Food Tracker button visible
- [ ] Food tracker page loads
- [ ] Image upload works
- [ ] Text input works
- [ ] Analyze button works

### API Verification:

Test the API directly:

```bash
curl -X POST http://127.0.0.1:5000/analyze-food-intake \
  -F "breakfast_text=2 idlis, 1 sambar" \
  -F "lunch_text=2 chapatis, 1 dal" \
  -F "dinner_text=1 rice, 1 curry"
```

Expected: JSON response with detected_foods, nutrition_summary, recommendations

### Results Verification:

- [ ] Detected foods display correctly
- [ ] Nutrition values are reasonable
- [ ] Progress bars show correctly
- [ ] Recommendations are relevant
- [ ] UI is responsive

---

## Troubleshooting

### Issue 1: "Module not found: PIL"

**Solution:**
```bash
pip install Pillow
```

### Issue 2: "Port 5000 already in use"

**Solution:**
```bash
# Windows
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# Or change port in app.py:
# app.run(host="0.0.0.0", port=5001)
```

### Issue 3: "CORS error in browser console"

**Solution:**
- Verify backend is running
- Check `API_BASE_URL` in `food-tracker.js`
- Ensure Flask-CORS is installed

### Issue 4: "Images not uploading"

**Solution:**
- Check file size (< 10MB)
- Use JPG or PNG format
- Check browser console for errors
- Verify backend is receiving files

### Issue 5: "No foods detected"

**Solution:**
- Add text description
- Use clear, well-lit photos
- Check supported foods list
- Verify FOOD_DATABASE in food_recognition.py

### Issue 6: "Test script fails"

**Solution:**
```bash
# Ensure you're in project root
cd C:\Users\Admin\Desktop\NutriCare-AI

# Check Python path
python -c "import sys; print(sys.path)"

# Run with explicit path
python -m pytest test_food_tracker.py
```

---

## Browser Console Testing

Open browser console (F12) and check:

### 1. Network Tab:
- POST request to `/analyze-food-intake`
- Status: 200 OK
- Response: JSON with data

### 2. Console Tab:
- No errors (red messages)
- May see CORS preflight (OPTIONS) - normal

### 3. Application Tab:
- Check FormData being sent
- Verify images are included

---

## Performance Testing

### Expected Performance:

- **Image Upload**: < 1 second
- **API Processing**: 1-2 seconds
- **Results Display**: < 1 second
- **Total Time**: 2-4 seconds

### Load Testing:

```bash
# Install Apache Bench
# Windows: Download from Apache website
# Test API endpoint
ab -n 100 -c 10 http://127.0.0.1:5000/
```

---

## Database Testing (Optional)

If using Firebase:

```bash
# Set environment variable
set GOOGLE_APPLICATION_CREDENTIALS=path\to\key.json

# Restart backend
python backend/app.py

# Check Firebase console for stored data
```

---

## Production Deployment Testing

### Frontend (Netlify):

1. Update `API_BASE_URL` in `food-tracker.js`
2. Deploy frontend folder
3. Test live URL

### Backend (Render):

1. Create `render.yaml`:
```yaml
services:
  - type: web
    name: nutricare-backend
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: python app.py
```

2. Deploy to Render
3. Update frontend API_BASE_URL
4. Test production API

---

## Automated Testing Script

Create `run_tests.bat` (Windows):

```batch
@echo off
echo Testing NutriCare Food Tracker...
echo.

echo [1/4] Testing Python installation...
python --version
if %errorlevel% neq 0 exit /b %errorlevel%

echo [2/4] Testing dependencies...
python -c "from PIL import Image; print('OK')"
if %errorlevel% neq 0 exit /b %errorlevel%

echo [3/4] Running test suite...
python test_food_tracker.py
if %errorlevel% neq 0 exit /b %errorlevel%

echo [4/4] Starting backend...
cd backend
start python app.py

echo.
echo ✅ All tests passed!
echo Backend is running on http://127.0.0.1:5000
echo Open frontend/food-tracker.html in your browser
pause
```

Run: `run_tests.bat`

---

## Success Criteria

### ✅ Installation Successful When:

1. All dependencies installed without errors
2. Test script passes all tests
3. Backend starts without errors
4. Frontend loads in browser
5. Food tracker page accessible
6. Can upload images
7. Can enter text
8. Analysis returns results
9. Results display correctly
10. Recommendations are relevant

---

## Next Steps After Installation

1. **Test with real data**: Upload actual food photos
2. **Customize food database**: Add more Indian foods
3. **Adjust recommendations**: Tune thresholds
4. **Upgrade ML model**: Implement deep learning
5. **Add features**: Historical tracking, reports
6. **Deploy to production**: Netlify + Render
7. **Collect feedback**: From real users
8. **Iterate**: Improve based on feedback

---

## Support & Resources

### Documentation:
- `FOOD_TRACKER_README.md` - Full documentation
- `QUICK_START_FOOD_TRACKER.md` - Quick start
- `ARCHITECTURE.md` - System architecture
- `IMPLEMENTATION_SUMMARY.md` - Implementation details

### Demo:
- `frontend/food-tracker-demo.html` - Sample results

### Code:
- `backend/food_recognition.py` - ML module
- `frontend/food-tracker.js` - Frontend logic

---

## Contact

For issues or questions:
1. Check documentation files
2. Review troubleshooting section
3. Check browser console (F12)
4. Check backend terminal logs
5. Verify all dependencies installed

---

**You're all set! 🎉**

Start the backend, open the food tracker, and begin tracking meals!
