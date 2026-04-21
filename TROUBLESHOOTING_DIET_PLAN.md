# 🔧 Troubleshooting - Diet Plan Not Showing

## Quick Fixes

### Issue: Diet Plan Not Appearing After Health Analysis

#### ✅ Solution 1: Check Backend Server
```bash
# Make sure backend is running
cd backend
python app.py

# You should see:
# * Running on http://127.0.0.1:5000
```

#### ✅ Solution 2: Check Browser Console
1. Press **F12** to open Developer Tools
2. Go to **Console** tab
3. Look for errors (red text)
4. Common errors:
   - "Failed to fetch" → Backend not running
   - "CORS error" → Backend needs restart
   - "404 Not Found" → Wrong API endpoint

#### ✅ Solution 3: Verify All Fields Filled
Make sure you entered:
- ✓ Age
- ✓ Systolic BP
- ✓ Diastolic BP
- ✓ Blood Sugar
- ✓ Body Temperature
- ✓ Heart Rate

#### ✅ Solution 4: Check Network Tab
1. Press **F12** → **Network** tab
2. Click "Analyze My Health"
3. Look for `/diet-plan` request
4. Check if it returns 200 OK
5. Click on it to see response

---

### Issue: Diet Plan Not Appearing After Food Tracker

#### ✅ Solution 1: Enter Food Data
Make sure you:
- Uploaded at least one photo OR
- Typed food in at least one meal

#### ✅ Solution 2: Check Backend Endpoint
```bash
# Test the endpoint manually
curl -X POST http://127.0.0.1:5000/analyze-food-intake \
  -F "breakfast_text=2 idlis, 1 sambar" \
  -F "lunch_text=2 chapatis, 1 dal" \
  -F "dinner_text=1 rice, 1 curry"
```

#### ✅ Solution 3: Scroll Down
The diet plan appears below the food tracker results. Scroll down to see:
- Detected Foods
- Nutrition Summary
- Recommendations
- **Your Personalized Meal Plan** ← Here!

---

## Common Issues & Solutions

### 1. "Failed to generate diet plan"

**Cause**: Backend server not running or crashed

**Solution**:
```bash
# Restart backend
cd backend
python app.py
```

### 2. Diet plan shows loading forever

**Cause**: Backend endpoint not responding

**Solution**:
1. Check backend terminal for errors
2. Restart backend server
3. Clear browser cache (Ctrl+Shift+Delete)
4. Refresh page (F5)

### 3. Diet plan is empty

**Cause**: API returned empty response

**Solution**:
1. Check backend logs
2. Verify `diet_engine.py` exists
3. Test diet plan endpoint:
```bash
curl -X POST http://127.0.0.1:5000/diet-plan \
  -H "Content-Type: application/json" \
  -d '{"risk":"Medium","duration":"week","food_preference":"vegetarian"}'
```

### 4. Wrong diet plan showing

**Cause**: Food preference or duration not selected

**Solution**:
1. Select food preference (Vegetarian/Eggetarian/Non-Vegetarian)
2. Select duration (7-Day/30-Day)
3. Re-run analysis

---

## Step-by-Step Debugging

### For Health Analysis:

1. **Open browser console** (F12)
2. **Click "Analyze My Health"**
3. **Check console for**:
   ```
   ✓ POST /analyze → 200 OK
   ✓ POST /nutrition-needs → 200 OK
   ✓ POST /diet-plan → 200 OK
   ```
4. **If any fails**:
   - Check backend terminal
   - Look for Python errors
   - Verify all files exist

### For Food Tracker:

1. **Open browser console** (F12)
2. **Click "Analyze My Food Intake"**
3. **Check console for**:
   ```
   ✓ POST /analyze-food-intake → 200 OK
   ✓ POST /diet-plan → 200 OK
   ```
4. **If any fails**:
   - Check if `food_recognition.py` exists
   - Verify Pillow is installed
   - Check backend logs

---

## Verification Checklist

### Backend:
- [ ] Backend server is running
- [ ] No errors in terminal
- [ ] Port 5000 is accessible
- [ ] All Python files exist
- [ ] Dependencies installed

### Frontend:
- [ ] Dashboard.html opens
- [ ] No console errors
- [ ] API_BASE_URL is correct
- [ ] All buttons work
- [ ] Forms submit properly

### Files:
- [ ] `backend/app.py` exists
- [ ] `backend/diet_engine.py` exists
- [ ] `backend/food_recognition.py` exists
- [ ] `frontend/dashboard.js` exists
- [ ] `frontend/dashboard.html` exists

---

## Manual Testing

### Test Health Analysis:
```javascript
// Open browser console and run:
fetch('http://127.0.0.1:5000/analyze', {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({
    age: 28,
    systolicbp: 120,
    diastolicbp: 80,
    bs: 7.5,
    bodytemp: 98.6,
    heartrate: 75
  })
}).then(r => r.json()).then(console.log);
```

### Test Diet Plan:
```javascript
// Open browser console and run:
fetch('http://127.0.0.1:5000/diet-plan', {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({
    risk: 'Medium',
    duration: 'week',
    food_preference: 'vegetarian'
  })
}).then(r => r.json()).then(console.log);
```

### Test Food Tracker:
```javascript
// Open browser console and run:
const formData = new FormData();
formData.append('breakfast_text', '2 idlis, 1 sambar');
formData.append('lunch_text', '2 chapatis, 1 dal');
formData.append('dinner_text', '1 rice, 1 curry');

fetch('http://127.0.0.1:5000/analyze-food-intake', {
  method: 'POST',
  body: formData
}).then(r => r.json()).then(console.log);
```

---

## Expected Behavior

### Health Analysis:
1. Click "Analyze My Health"
2. Button shows "Analyzing..."
3. Health summary appears
4. Risk level appears
5. Nutrition table fills
6. Alerts appear (if any)
7. **Diet plan appears** ← Should see this!
8. Chart updates
9. AI recommendations appear

### Food Tracker:
1. Enter food data
2. Click "Analyze My Food Intake"
3. Button shows "Analyzing..."
4. Detected foods appear
5. Nutrition summary appears
6. Recommendations appear
7. **Diet plan appears** ← Should see this!

---

## Still Not Working?

### Check These:

1. **Backend logs**:
   - Look at terminal where backend is running
   - Check for Python errors
   - Verify all imports work

2. **Browser console**:
   - Press F12
   - Look for JavaScript errors
   - Check Network tab for failed requests

3. **File permissions**:
   - Make sure all files are readable
   - Check if backend can write logs

4. **Port conflicts**:
   - Make sure port 5000 is not used by another app
   - Try changing port in `app.py`

5. **Dependencies**:
   ```bash
   pip install -r backend/requirements.txt
   ```

---

## Quick Test Script

Create `test_diet_plan.py`:

```python
import requests

# Test health analysis
print("Testing health analysis...")
response = requests.post('http://127.0.0.1:5000/analyze', json={
    'age': 28,
    'systolicbp': 120,
    'diastolicbp': 80,
    'bs': 7.5,
    'bodytemp': 98.6,
    'heartrate': 75
})
print(f"Status: {response.status_code}")
print(f"Risk: {response.json()['risk']}")

# Test diet plan
print("\nTesting diet plan...")
response = requests.post('http://127.0.0.1:5000/diet-plan', json={
    'risk': 'Medium',
    'duration': 'week',
    'food_preference': 'vegetarian'
})
print(f"Status: {response.status_code}")
print(f"Days: {len(response.json()['diet_plan'])}")

print("\n✅ All tests passed!")
```

Run:
```bash
python test_diet_plan.py
```

---

## Contact Support

If nothing works:
1. Check all documentation files
2. Review `INSTALLATION_GUIDE.md`
3. Check `ARCHITECTURE.md` for system overview
4. Verify all files from `FILE_STRUCTURE.md` exist

---

**Most common fix: Just restart the backend server!** 🔄
