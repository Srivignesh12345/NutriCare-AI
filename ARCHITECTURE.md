# 🏗️ Food Tracker System Architecture

## System Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                         USER INTERFACE                          │
│                     (food-tracker.html)                         │
└─────────────────────────────────────────────────────────────────┘
                                │
                                │ User Actions
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                    MEAL INPUT SECTIONS                          │
├─────────────────────────────────────────────────────────────────┤
│  🌅 BREAKFAST          ☀️ LUNCH           🌙 DINNER            │
│  ┌──────────┐         ┌──────────┐        ┌──────────┐         │
│  │ 📷 Image │         │ 📷 Image │        │ 📷 Image │         │
│  │  Upload  │         │  Upload  │        │  Upload  │         │
│  └──────────┘         └──────────┘        └──────────┘         │
│  ┌──────────┐         ┌──────────┐        ┌──────────┐         │
│  │ ✍️ Text  │         │ ✍️ Text  │        │ ✍️ Text  │         │
│  │  Input   │         │  Input   │        │  Input   │         │
│  └──────────┘         └──────────┘        └──────────┘         │
└─────────────────────────────────────────────────────────────────┘
                                │
                                │ Click "Analyze"
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                    FRONTEND PROCESSING                          │
│                    (food-tracker.js)                            │
├─────────────────────────────────────────────────────────────────┤
│  1. Capture uploaded images                                     │
│  2. Collect text inputs                                         │
│  3. Create FormData object                                      │
│  4. Send POST request to backend                                │
└─────────────────────────────────────────────────────────────────┘
                                │
                                │ HTTP POST
                                │ multipart/form-data
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                      BACKEND API                                │
│                  (Flask - app.py)                               │
├─────────────────────────────────────────────────────────────────┤
│  Endpoint: POST /analyze-food-intake                            │
│                                                                 │
│  Receives:                                                      │
│  - breakfast_image, breakfast_text                              │
│  - lunch_image, lunch_text                                      │
│  - dinner_image, dinner_text                                    │
└─────────────────────────────────────────────────────────────────┘
                                │
                                │ Process Request
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                   ML PROCESSING MODULE                          │
│                 (food_recognition.py)                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  IMAGE ANALYSIS                                         │   │
│  │  analyze_image_simple()                                 │   │
│  │  ┌──────────────────────────────────────────────────┐   │   │
│  │  │ 1. Open image with PIL                           │   │   │
│  │  │ 2. Resize to 100x100                             │   │   │
│  │  │ 3. Calculate average RGB values                  │   │   │
│  │  │ 4. Apply color heuristics:                       │   │   │
│  │  │    - Reddish → Tomato                            │   │   │
│  │  │    - Greenish → Spinach                          │   │   │
│  │  │    - Yellowish → Rice, Chapati                   │   │   │
│  │  │    - Brownish → Dal, Curry                       │   │   │
│  │  │ 5. Return detected foods                         │   │   │
│  │  └──────────────────────────────────────────────────┘   │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  TEXT PARSING                                           │   │
│  │  parse_text_input()                                     │   │
│  │  ┌──────────────────────────────────────────────────┐   │   │
│  │  │ 1. Convert text to lowercase                     │   │   │
│  │  │ 2. Search for food keywords                      │   │   │
│  │  │ 3. Extract quantities using regex                │   │   │
│  │  │    Pattern: "2 bowls rice" → {rice: 2}           │   │   │
│  │  │ 4. Return list of {food, quantity}               │   │   │
│  │  └──────────────────────────────────────────────────┘   │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  NUTRITION CALCULATION                                  │   │
│  │  calculate_nutrition()                                  │   │
│  │  ┌──────────────────────────────────────────────────┐   │   │
│  │  │ 1. Loop through detected foods                   │   │   │
│  │  │ 2. Lookup in FOOD_DATABASE                       │   │   │
│  │  │ 3. Multiply by quantity                          │   │   │
│  │  │ 4. Sum up: calories, protein, iron, calcium      │   │   │
│  │  │ 5. Return total nutrition                        │   │   │
│  │  └──────────────────────────────────────────────────┘   │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  RECOMMENDATION ENGINE                                  │   │
│  │  generate_recommendations()                             │   │
│  │  ┌──────────────────────────────────────────────────┐   │   │
│  │  │ 1. Compare intake vs. pregnancy targets          │   │   │
│  │  │    - Calories: 2200 kcal                         │   │   │
│  │  │    - Protein: 80g                                │   │   │
│  │  │    - Iron: 27mg                                  │   │   │
│  │  │    - Calcium: 1200mg                             │   │   │
│  │  │ 2. Identify deficiencies (< 70% of target)       │   │   │
│  │  │ 3. Generate recommendations for each             │   │   │
│  │  │ 4. Suggest specific foods                        │   │   │
│  │  └──────────────────────────────────────────────────┘   │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
                                │
                                │ Return JSON
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                      API RESPONSE                               │
├─────────────────────────────────────────────────────────────────┤
│  {                                                              │
│    "detected_foods": {                                          │
│      "breakfast": {"items": ["2 idli", "1 sambar"]},           │
│      "lunch": {"items": ["2 chapati", "1 dal"]},               │
│      "dinner": {"items": ["1 rice", "1 curry"]}                │
│    },                                                           │
│    "nutrition_summary": {                                       │
│      "calories": 1450,                                          │
│      "protein": 52,                                             │
│      "iron": 15,                                                │
│      "calcium": 680                                             │
│    },                                                           │
│    "recommendations": [                                         │
│      {                                                          │
│        "title": "Increase Iron-Rich Foods",                     │
│        "message": "You need more iron...",                      │
│        "foods": ["Spinach", "Dates", "Ragi"]                   │
│      }                                                          │
│    ]                                                            │
│  }                                                              │
└─────────────────────────────────────────────────────────────────┘
                                │
                                │ Parse Response
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                   RESULTS DISPLAY                               │
│                  (food-tracker.js)                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  🍽️ DETECTED FOODS                                      │   │
│  │  ┌─────────┐  ┌─────────┐  ┌─────────┐                 │   │
│  │  │Breakfast│  │  Lunch  │  │ Dinner  │                 │   │
│  │  │ Items   │  │  Items  │  │ Items   │                 │   │
│  │  └─────────┘  └─────────┘  └─────────┘                 │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  📊 NUTRITION SUMMARY                                   │   │
│  │  ┌──────┐  ┌──────┐  ┌──────┐  ┌──────┐               │   │
│  │  │Calor │  │Protei│  │ Iron │  │Calciu│               │   │
│  │  │ ies  │  │  n   │  │      │  │  m   │               │   │
│  │  │[====]│  │[====]│  │[===] │  │[====]│               │   │
│  │  └──────┘  └──────┘  └──────┘  └──────┘               │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  💡 RECOMMENDATIONS                                     │   │
│  │  ┌─────────────────────────────────────────────────┐   │   │
│  │  │ ⚡ Increase Calorie Intake                      │   │   │
│  │  │    → Banana, Dates, Nuts                        │   │   │
│  │  └─────────────────────────────────────────────────┘   │   │
│  │  ┌─────────────────────────────────────────────────┐   │   │
│  │  │ 🩸 Increase Iron-Rich Foods                     │   │   │
│  │  │    → Spinach, Dates, Ragi                       │   │   │
│  │  └─────────────────────────────────────────────────┘   │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## Data Flow Diagram

```
┌──────────┐
│  User    │
└────┬─────┘
     │ 1. Upload images + text
     ▼
┌──────────────┐
│  Frontend    │
│  (HTML/JS)   │
└────┬─────────┘
     │ 2. POST /analyze-food-intake
     ▼
┌──────────────┐
│   Flask      │
│   Server     │
└────┬─────────┘
     │ 3. Process request
     ▼
┌──────────────┐
│   Image      │──────┐
│  Analysis    │      │
└──────────────┘      │
                      │ 4. Detect foods
┌──────────────┐      │
│    Text      │──────┤
│   Parsing    │      │
└──────────────┘      │
                      ▼
                ┌──────────────┐
                │  Nutrition   │
                │ Calculation  │
                └────┬─────────┘
                     │ 5. Calculate totals
                     ▼
                ┌──────────────┐
                │Recommenda-   │
                │tion Engine   │
                └────┬─────────┘
                     │ 6. Generate suggestions
                     ▼
                ┌──────────────┐
                │    JSON      │
                │  Response    │
                └────┬─────────┘
                     │ 7. Return to frontend
                     ▼
                ┌──────────────┐
                │   Display    │
                │   Results    │
                └──────────────┘
```

## Component Interaction

```
┌─────────────────────────────────────────────────────────────┐
│                    FRONTEND LAYER                           │
├─────────────────────────────────────────────────────────────┤
│  food-tracker.html  │  food-tracker.css  │  food-tracker.js │
│  (Structure)        │  (Styling)         │  (Logic)         │
└─────────────────────────────────────────────────────────────┘
                              │
                              │ HTTP/REST
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    BACKEND LAYER                            │
├─────────────────────────────────────────────────────────────┤
│  app.py             │  food_recognition.py                  │
│  (API Routes)       │  (ML Processing)                      │
└─────────────────────────────────────────────────────────────┘
                              │
                              │ Data Access
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    DATA LAYER                               │
├─────────────────────────────────────────────────────────────┤
│  FOOD_DATABASE (In-memory dictionary)                       │
│  - Food items with nutrition values                         │
│  - 20+ common Indian foods                                  │
└─────────────────────────────────────────────────────────────┘
```

## Technology Stack

```
┌─────────────────────────────────────────────────────────────┐
│                      FRONTEND                               │
├─────────────────────────────────────────────────────────────┤
│  HTML5          │  Modern semantic markup                   │
│  CSS3           │  Gradients, flexbox, grid                 │
│  JavaScript     │  ES6+, async/await, FormData             │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│                      BACKEND                                │
├─────────────────────────────────────────────────────────────┤
│  Flask          │  Web framework                            │
│  Flask-CORS     │  Cross-origin requests                    │
│  Pillow (PIL)   │  Image processing                         │
│  NumPy          │  Array operations                         │
│  Python 3.7+    │  Core language                            │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│                      ML/AI                                  │
├─────────────────────────────────────────────────────────────┤
│  Color Analysis │  RGB-based food detection                 │
│  Regex Parsing  │  Text extraction                          │
│  Rule Engine    │  Recommendation logic                     │
│  (Future: TensorFlow, PyTorch for deep learning)            │
└─────────────────────────────────────────────────────────────┘
```

## File Dependencies

```
food-tracker.html
    ├── Imports: dashboard.css
    ├── Imports: food-tracker.css
    └── Imports: food-tracker.js
            └── Calls: API_BASE_URL/analyze-food-intake

app.py
    ├── Imports: Flask, CORS
    ├── Imports: food_recognition
    └── Exposes: /analyze-food-intake endpoint

food_recognition.py
    ├── Imports: PIL (Pillow)
    ├── Imports: NumPy
    ├── Imports: re (regex)
    └── Contains: FOOD_DATABASE
```

## Deployment Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    DEVELOPMENT                              │
├─────────────────────────────────────────────────────────────┤
│  Frontend: file:///frontend/food-tracker.html              │
│  Backend:  http://127.0.0.1:5000                           │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│                    PRODUCTION                               │
├─────────────────────────────────────────────────────────────┤
│  Frontend: Netlify/Vercel                                   │
│  Backend:  Render/Heroku/AWS                                │
│  Database: Firebase/PostgreSQL (future)                     │
│  Storage:  AWS S3 for images (future)                       │
└─────────────────────────────────────────────────────────────┘
```

---

This architecture provides a clear, scalable foundation for the food tracking system!
