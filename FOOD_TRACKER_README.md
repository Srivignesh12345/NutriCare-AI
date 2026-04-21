# 📸 Food Intake Tracker - Setup Guide

## Overview
The Food Intake Tracker allows users to:
- Upload photos of their meals (Breakfast, Lunch, Dinner)
- Type what they ate as text input
- Get AI-powered food recognition
- See nutrition analysis
- Receive personalized recommendations

## Installation

### 1. Install Required Dependencies

```bash
cd backend
pip install Pillow
```

Or install all dependencies:
```bash
pip install -r requirements.txt
```

### 2. Start Backend Server

```bash
cd backend
python app.py
```

Server runs at: `http://127.0.0.1:5000`

### 3. Access Food Tracker

Open your browser and go to:
- Main Dashboard: `frontend/dashboard.html`
- Click "Food Tracker" button in navigation
- Or directly: `frontend/food-tracker.html`

## How to Use

### Step 1: Upload Meal Photos
1. Click on the camera icon for each meal (Breakfast, Lunch, Dinner)
2. Select a photo from your device
3. Preview will show immediately

### Step 2: Add Text Description (Optional)
- Type what you ate in the text box
- Example: "2 idlis, 1 bowl sambar, 1 glass milk"
- The system will extract quantities automatically

### Step 3: Analyze
- Click "Analyze My Food Intake" button
- Wait for AI processing

### Step 4: View Results
You'll see:
1. **Detected Foods** - What the AI recognized from images and text
2. **Nutrition Summary** - Total calories, protein, iron, calcium
3. **Recommendations** - What you should eat next based on deficiencies

## Features

### 🤖 AI Food Recognition
- Analyzes image colors to detect food types
- Extracts food items from text descriptions
- Recognizes quantities (bowls, pieces, glasses)

### 📊 Nutrition Calculation
Tracks essential nutrients:
- **Calories**: Target 2200 kcal/day
- **Protein**: Target 80g/day
- **Iron**: Target 27mg/day
- **Calcium**: Target 1200mg/day

### 💡 Smart Recommendations
Based on your intake, suggests:
- Foods to increase calories
- Protein-rich foods
- Iron-rich foods
- Calcium sources

## Supported Foods

### Common Indian Foods:
- **Breakfast**: Idli, Dosa, Sambar, Milk
- **Lunch/Dinner**: Rice, Chapati, Dal, Curry, Vegetables
- **Proteins**: Egg, Chicken, Fish, Paneer
- **Vegetables**: Spinach, Potato, Tomato, Carrot
- **Fruits**: Banana, Apple, Orange

### Text Input Examples:
```
"2 idlis, 1 bowl sambar, 1 glass milk"
"2 chapatis, 1 bowl dal, 1 bowl vegetables"
"1 bowl rice, 1 bowl curry, salad"
"2 eggs, 2 bread slices, 1 banana"
```

## API Endpoint

### POST /analyze-food-intake

**Request (multipart/form-data):**
```
breakfast_image: [File]
breakfast_text: "2 idlis, 1 bowl sambar"
lunch_image: [File]
lunch_text: "2 chapatis, 1 bowl dal"
dinner_image: [File]
dinner_text: "1 bowl rice, 1 bowl curry"
```

**Response:**
```json
{
  "detected_foods": {
    "breakfast": {
      "items": ["2 idli", "1 sambar"]
    },
    "lunch": {
      "items": ["2 chapati", "1 dal"]
    },
    "dinner": {
      "items": ["1 rice", "1 curry"]
    }
  },
  "nutrition_summary": {
    "calories": 1450,
    "protein": 52,
    "iron": 15,
    "calcium": 680
  },
  "recommendations": [
    {
      "title": "Increase Iron-Rich Foods",
      "message": "You've consumed 15mg iron. Target: 27mg daily.",
      "foods": ["Spinach", "Dates", "Ragi", "Pomegranate"]
    }
  ]
}
```

## Technical Details

### Image Processing
- Uses PIL (Pillow) for image analysis
- Analyzes RGB color values
- Simple heuristic-based detection
- Can be upgraded to deep learning models (TensorFlow/PyTorch)

### Text Parsing
- Regular expressions to extract food items
- Quantity detection (numbers + units)
- Case-insensitive matching

### Nutrition Database
- 20+ common Indian foods
- Nutrition per serving
- Easily extensible

## Future Enhancements

### Advanced ML Models
Replace simple color analysis with:
- **TensorFlow/Keras** - Food image classification
- **YOLO** - Object detection for multiple foods
- **ResNet/MobileNet** - Pre-trained models

### Example with TensorFlow:
```python
# Install: pip install tensorflow
import tensorflow as tf
model = tf.keras.models.load_model('food_classifier.h5')
predictions = model.predict(image_array)
```

### Additional Features
- [ ] Barcode scanning for packaged foods
- [ ] Voice input for food logging
- [ ] Historical tracking (weekly/monthly)
- [ ] Export reports as PDF
- [ ] Integration with fitness trackers
- [ ] Multi-language support

## Troubleshooting

### Issue: Images not uploading
- Check file size (max 10MB recommended)
- Supported formats: JPG, PNG, JPEG
- Ensure backend server is running

### Issue: No foods detected
- Try adding text description
- Use clear, well-lit photos
- Describe foods in text box

### Issue: CORS errors
- Ensure Flask-CORS is installed
- Check API_BASE_URL in food-tracker.js
- Verify backend is running on port 5000

## Upgrading to Production ML Model

For better accuracy, train a custom model:

```bash
# Install TensorFlow
pip install tensorflow

# Use Food-101 dataset or custom dataset
# Train CNN model
# Save model as .h5 file
# Update food_recognition.py to use the model
```

## Support

For issues or questions:
1. Check console logs (F12 in browser)
2. Check backend terminal for errors
3. Verify all dependencies are installed
4. Ensure images are valid format

---

Built with ❤️ for maternal health
