# 🚀 Quick Start - Food Intake Tracker

## What's New?

You now have a **Food Intake Tracker** that allows users to:
1. **Upload photos** of their meals (Breakfast, Lunch, Dinner)
2. **Type what they ate** as an alternative or supplement
3. Get **AI-powered food recognition** from images
4. See **nutrition analysis** (calories, protein, iron, calcium)
5. Receive **personalized recommendations** on what to eat next

## Files Created

### Frontend:
- `frontend/food-tracker.html` - Main food tracker page
- `frontend/food-tracker.css` - Styling for food tracker
- `frontend/food-tracker.js` - JavaScript logic

### Backend:
- `backend/food_recognition.py` - ML module for food detection
- Updated `backend/app.py` - Added `/analyze-food-intake` endpoint
- Updated `backend/requirements.txt` - Added Pillow library

### Documentation:
- `FOOD_TRACKER_README.md` - Detailed documentation
- `test_food_tracker.py` - Test script
- Updated main `README.md`

## Installation Steps

### 1. Install Dependencies
```bash
cd backend
pip install Pillow
```

### 2. Test the Module (Optional)
```bash
python test_food_tracker.py
```

### 3. Start Backend
```bash
cd backend
python app.py
```

### 4. Open Frontend
- Open `frontend/dashboard.html` in browser
- Click the green "Food Tracker" button
- Or directly open `frontend/food-tracker.html`

## How It Works

### User Flow:
1. User uploads meal photos (or types food items)
2. Frontend sends images + text to backend
3. Backend processes:
   - Analyzes image colors to detect food types
   - Parses text to extract food items and quantities
   - Calculates total nutrition
   - Generates recommendations based on deficiencies
4. Frontend displays results with visual cards

### Example Usage:

**Breakfast:**
- Upload: Photo of idlis and sambar
- Type: "2 idlis, 1 bowl sambar, 1 glass milk"

**Lunch:**
- Upload: Photo of rice and dal
- Type: "2 bowls rice, 1 bowl dal, vegetables"

**Dinner:**
- Upload: Photo of chapatis
- Type: "2 chapatis, 1 bowl curry, salad"

**Results:**
- Detected Foods: Lists all items from each meal
- Nutrition Summary: Total calories (1450), protein (52g), iron (15mg), calcium (680mg)
- Recommendations: "Increase Iron-Rich Foods - Add Spinach, Dates, Ragi"

## Key Features

### 🤖 AI Food Recognition
- Simple color-based detection (can be upgraded to deep learning)
- Recognizes 20+ common Indian foods
- Extracts quantities from text

### 📊 Nutrition Tracking
- Compares intake vs. pregnancy requirements
- Visual progress bars
- Real-time calculations

### 💡 Smart Recommendations
- Identifies nutrient deficiencies
- Suggests specific foods to add
- Pregnancy-focused advice

## Supported Foods

**Breakfast Items:** Idli, Dosa, Sambar, Milk, Egg
**Main Meals:** Rice, Chapati, Roti, Dal, Curry, Vegetables
**Proteins:** Egg, Chicken, Fish, Paneer
**Vegetables:** Spinach, Potato, Tomato, Carrot
**Fruits:** Banana, Apple, Orange
**Dairy:** Milk, Curd, Paneer

## API Endpoint

```
POST http://127.0.0.1:5000/analyze-food-intake

Content-Type: multipart/form-data

Fields:
- breakfast_image (file)
- breakfast_text (string)
- lunch_image (file)
- lunch_text (string)
- dinner_image (file)
- dinner_text (string)
```

## Upgrading to Advanced ML

Current implementation uses simple color analysis. To upgrade:

### Option 1: TensorFlow/Keras
```bash
pip install tensorflow
# Use pre-trained models like MobileNet, ResNet
# Train on Food-101 dataset
```

### Option 2: PyTorch
```bash
pip install torch torchvision
# Use pre-trained models
# Fine-tune on Indian food dataset
```

### Option 3: Cloud APIs
- Google Cloud Vision API
- AWS Rekognition
- Clarifai Food Model

## Testing

Run the test script:
```bash
python test_food_tracker.py
```

Expected output:
- ✅ Text parsing works
- ✅ Nutrition calculation works
- ✅ Recommendations generated

## Troubleshooting

**Issue:** Module not found
```bash
cd backend
pip install -r requirements.txt
```

**Issue:** CORS error
- Check backend is running on port 5000
- Verify API_BASE_URL in food-tracker.js

**Issue:** Images not uploading
- Check file size (< 10MB)
- Use JPG/PNG format
- Ensure backend has write permissions

## Next Steps

1. ✅ Test the basic functionality
2. 🔄 Collect user feedback
3. 📈 Upgrade to deep learning model (optional)
4. 🗄️ Add database to store history
5. 📱 Create mobile app version

## Demo Data

Try these text inputs:

**Healthy Day:**
```
Breakfast: 2 idlis, 1 bowl sambar, 1 glass milk, 1 banana
Lunch: 2 chapatis, 1 bowl dal, 1 bowl spinach, 1 bowl curd
Dinner: 1 bowl rice, 1 bowl fish curry, salad, 1 orange
```

**Low Nutrition Day:**
```
Breakfast: 1 idli, tea
Lunch: 1 chapati, vegetables
Dinner: 1 bowl rice
```

The system will detect deficiencies and recommend foods!

---

**Ready to use!** 🎉

Start the backend and open the food tracker to begin tracking meals.
