# 🏃 EXERCISE FEATURE - NutriCare AI

## ✅ Feature Added: Daily Exercise Recommendations

The diet plan now includes **personalized daily exercise recommendations** based on the maternal health risk level.

---

## 🎯 How It Works

When you generate a diet plan (weekly or monthly), each day now includes:
- ✅ Breakfast
- ✅ Lunch
- ✅ Dinner
- ✅ **Daily Exercise** (NEW!)
- ✅ Nutritional Note

---

## 💪 Exercise Plans by Risk Level

### 🔴 HIGH RISK (Gentle & Safe)
Focus: Minimal exertion, stress relief, gentle movement

**Daily Exercises (Rotates through 7 options):**
1. Gentle Walking - 10 minutes (morning)
2. Deep Breathing - 5 minutes (3 times a day)
3. Prenatal Yoga - 15 minutes (evening)
4. Ankle Rotations - 10 reps (sitting)
5. Pelvic Tilts - 10 reps (lying down)
6. Shoulder Rolls - 10 reps (sitting)
7. Meditation - 10 minutes (before sleep)

**Safety Notes:**
- Very gentle movements only
- Can be done at home
- No strenuous activity
- Focus on breathing and relaxation

---

### 🟡 MEDIUM RISK (Moderate Activity)
Focus: Balanced exercise, building strength, flexibility

**Daily Exercises (Rotates through 7 options):**
1. Brisk Walking - 20 minutes (morning)
2. Prenatal Yoga - 20 minutes (evening)
3. Swimming - 15 minutes (if available)
4. Kegel Exercises - 10 reps (3 times a day)
5. Cat-Cow Stretch - 10 reps (morning)
6. Squats - 10 reps (with support)
7. Breathing Exercises - 10 minutes (evening)

**Safety Notes:**
- Moderate intensity
- Listen to your body
- Stay hydrated
- Stop if you feel dizzy

---

### 🟢 LOW RISK (Active & Healthy)
Focus: Maintaining fitness, preparing for delivery

**Daily Exercises (Rotates through 7 options):**
1. Walking - 30 minutes (morning/evening)
2. Prenatal Yoga - 30 minutes (daily)
3. Swimming - 20 minutes (3 times a week)
4. Squats - 15 reps (with support)
5. Pelvic Floor Exercises - 15 reps (daily)
6. Stretching - 15 minutes (morning)
7. Light Aerobics - 20 minutes (3 times a week)

**Safety Notes:**
- Stay active but don't overdo it
- Maintain regular routine
- Proper warm-up and cool-down
- Consult doctor before starting

---

## 📱 How to See Exercise Recommendations

### Method 1: Frontend Dashboard
1. Open `frontend/dashboard.html`
2. Enter health data
3. Click "Analyze Health"
4. View the diet plan
5. **Each day now shows exercise recommendation!**

### Method 2: API Response
```bash
curl -X POST http://127.0.0.1:5000/diet-plan \
  -H "Content-Type: application/json" \
  -d '{"risk":"Medium","duration":"week"}'
```

**Response includes Exercise field:**
```json
{
  "Day 1": {
    "Breakfast": "Milk + Dates + Almonds",
    "Lunch": "Brown Rice + Dal + Spinach",
    "Dinner": "Soup + Salad",
    "Exercise": "Brisk Walking - 20 minutes (morning)",
    "Note": "Maintain balanced nutrition"
  }
}
```

---

## 🎨 Frontend Display

The diet plan cards now show:

```
┌─────────────────────────────────────┐
│ Day 1                               │
├─────────────────────────────────────┤
│ 🌅 Breakfast: Milk + Dates         │
│ 🍛 Lunch: Brown Rice + Dal         │
│ 🌙 Dinner: Soup + Salad            │
│ 🏃 Exercise: Brisk Walking - 20min │
│ 💡 Maintain balanced nutrition     │
└─────────────────────────────────────┘
```

---

## 🔧 Technical Implementation

### Backend Changes:
**File: `backend/diet_engine.py`**
- Added `EXERCISES` dictionary with 7 exercises per risk level
- Updated `generate_diet()` function to include exercise
- Exercise rotates daily (Day 1 = Exercise 1, Day 2 = Exercise 2, etc.)

### Frontend Changes:
**File: `frontend/dashboard.js`**
- Updated `displayDietPlan()` function
- Added exercise display with 🏃 emoji
- Maintains existing layout and styling

---

## ✅ Testing

### Test Case 1: Medium Risk - 7 Days
```bash
cd backend
python -c "from diet_engine import generate_diet; import json; print(json.dumps(generate_diet(7, 'Medium'), indent=2))"
```

**Expected Output:**
- Day 1: Brisk Walking - 20 minutes
- Day 2: Prenatal Yoga - 20 minutes
- Day 3: Swimming - 15 minutes
- Day 4: Kegel Exercises - 10 reps
- Day 5: Cat-Cow Stretch - 10 reps
- Day 6: Squats - 10 reps
- Day 7: Breathing Exercises - 10 minutes

### Test Case 2: High Risk - 3 Days
```bash
python -c "from diet_engine import generate_diet; import json; print(json.dumps(generate_diet(3, 'High'), indent=2))"
```

**Expected Output:**
- Day 1: Gentle Walking - 10 minutes
- Day 2: Deep Breathing - 5 minutes
- Day 3: Prenatal Yoga - 15 minutes

---

## 🎯 Benefits

✅ **Personalized**: Exercises match risk level
✅ **Safe**: Pregnancy-safe movements only
✅ **Varied**: Different exercise each day
✅ **Practical**: Can be done at home
✅ **Timed**: Specific duration and timing
✅ **Integrated**: Part of daily routine with meals

---

## 📊 Exercise Rotation Logic

For a 30-day plan:
- Days 1-7: Exercises 1-7
- Days 8-14: Exercises 1-7 (repeats)
- Days 15-21: Exercises 1-7 (repeats)
- Days 22-28: Exercises 1-7 (repeats)
- Days 29-30: Exercises 1-2

This ensures variety while maintaining consistency.

---

## 🚀 Quick Demo

**Start Backend:**
```bash
cd backend
python app.py
```

**Open Frontend:**
```
Double-click: frontend/dashboard.html
```

**Test:**
1. Enter: Age=28, BP=120/80, BS=7.5, Temp=98.6, HR=75
2. Click "Analyze Health"
3. View diet plan
4. **See exercise for each day!**

---

## 📝 Future Enhancements

Potential additions:
- [ ] Video demonstrations for each exercise
- [ ] Exercise tracking/completion checkboxes
- [ ] Trimester-specific exercises
- [ ] Exercise intensity adjustment
- [ ] Integration with fitness trackers
- [ ] Reminder notifications

---

## ✅ Feature Complete!

The exercise recommendation feature is now fully integrated into the NutriCare AI system. Every diet plan (weekly or monthly) includes personalized daily exercises based on the maternal health risk level.

**Files Modified:**
- ✅ `backend/diet_engine.py` - Added exercise logic
- ✅ `frontend/dashboard.js` - Added exercise display

**No Breaking Changes:**
- ✅ Existing API endpoints work the same
- ✅ Frontend layout remains consistent
- ✅ Backward compatible with old code
