import os
import joblib
import numpy as np
from datetime import datetime

from flask import Flask, request, jsonify
from flask_cors import CORS

from diet_engine import generate_diet
from food_recognition import analyze_image_simple, parse_text_input, calculate_nutrition, generate_recommendations

# =====================================================
# Load ML Model
# =====================================================
MODEL_PATH = os.path.join("ml", "model.pkl")
ENCODER_PATH = os.path.join("ml", "label_encoder.pkl")

model = joblib.load(MODEL_PATH)
label_encoder = joblib.load(ENCODER_PATH)

# =====================================================
# Flask App
# =====================================================
app = Flask(__name__)

CORS(
    app,
    resources={r"/*": {"origins": "*"}},
    supports_credentials=True,
    allow_headers=["Content-Type", "Authorization"],
    methods=["GET", "POST", "OPTIONS"]
)

# =====================================================
# Force CORS headers on every response
# =====================================================
@app.after_request
def after_request(response):
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add("Access-Control-Allow-Headers", "Content-Type,Authorization")
    response.headers.add("Access-Control-Allow-Methods", "GET,POST,OPTIONS")
    return response

# =====================================================
# Firebase (Safe Initialization)
# =====================================================
db = None
firestore = None

try:
    import firebase_admin
    from firebase_admin import credentials, firestore

    if not firebase_admin._apps:
        cred_path = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
        if cred_path and os.path.exists(cred_path):
            cred = credentials.Certificate(cred_path)
            firebase_admin.initialize_app(cred)
            db = firestore.client()
            print("Firebase connected")
        else:
            print("Firebase disabled: No credentials found")

except Exception as e:
    print("Firebase disabled:", str(e))

# =====================================================
# Analyze API
# =====================================================
@app.route("/analyze", methods=["POST", "OPTIONS"])
def analyze():
    if request.method == "OPTIONS":
        return "", 204
    
    data = request.get_json()

    required_fields = [
        "age", "systolicbp", "diastolicbp",
        "bs", "bodytemp", "heartrate"
    ]

    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Missing field: {field}"}), 400

    features = np.array([[  
        data["age"],
        data["systolicbp"],
        data["diastolicbp"],
        data["bs"],
        data["bodytemp"],
        data["heartrate"]
    ]])

    prediction = model.predict(features)
    risk = label_encoder.inverse_transform(prediction)[0]

    record = {
        **data,
        "risk": risk,
        "timestamp": datetime.utcnow().isoformat()
    }

    if db:
        db.collection("nutrition_reports").add(record)

    return jsonify({
        "risk": risk,
        "message": f"Predicted maternal health risk: {risk}"
    })

# =====================================================
# Diet Plan API
# =====================================================
@app.route("/diet-plan", methods=["POST", "OPTIONS"])
def diet_plan():
    if request.method == "OPTIONS":
        return "", 204
    
    data = request.get_json()

    risk = data.get("risk", "Medium")
    duration = data.get("duration", "week")
    food_preference = data.get("food_preference", "vegetarian")

    days = 7 if duration == "week" else 30
    diet = generate_diet(days, risk, food_preference)

    response = {
        "risk": risk,
        "duration": duration,
        "food_preference": food_preference,
        "diet_plan": diet,
        "generated_at": datetime.utcnow().isoformat()
    }

    if db:
        db.collection("diet_plans").add(response)

    return jsonify(response)

# =====================================================
# History API
# =====================================================
@app.route("/history", methods=["GET"])
def history():
    if not db:
        return jsonify([])

    docs = (
        db.collection("nutrition_reports")
        .order_by("timestamp", direction=firestore.Query.DESCENDING)
        .stream()
    )

    return jsonify([doc.to_dict() for doc in docs])

# =====================================================
# AI Recommendations API
# =====================================================
@app.route("/recommendations", methods=["POST", "OPTIONS"])
def recommendations():
    if request.method == "OPTIONS":
        return "", 204
    
    data = request.get_json()
    risk = data.get("risk", "Medium")
    bs = data.get("bs", 7.0)
    systolicbp = data.get("systolicbp", 120)
    
    recs = []
    
    if risk == "High" or bs > 8:
        recs.append({
            "title": "Iron Deficiency Detected",
            "foods": ["Spinach", "Dates", "Ragi", "Pomegranate", "Beetroot"]
        })
    
    if bs > 7.8:
        recs.append({
            "title": "Blood Sugar Control",
            "foods": ["Oats", "Brown Rice", "Quinoa", "Vegetables"]
        })
    
    if systolicbp > 130:
        recs.append({
            "title": "Blood Pressure Management",
            "foods": ["Banana", "Spinach", "Garlic", "Beetroot"]
        })
    
    return jsonify({"recommendations": recs})

# =====================================================
# Nutrition Needs API
# =====================================================
@app.route("/nutrition-needs", methods=["POST", "OPTIONS"])
def nutrition_needs():
    if request.method == "OPTIONS":
        return "", 204
    
    data = request.get_json()
    risk = data.get("risk", "Medium").lower()
    age = data.get("age", 28)
    
    # Pregnancy nutrition standards
    standards = {
        "calories": 2200,
        "protein": 80,
        "iron": 27,
        "calcium": 1200,
        "folic_acid": 600,
        "vitamin_d": 600,
        "vitamin_c": 85,
        "fiber": 28
    }
    
    # Estimate current intake based on risk
    factor = 0.7 if risk == "high" else 0.8 if risk == "medium" else 0.9
    
    current = {
        "calories": round(standards["calories"] * factor),
        "protein": round(standards["protein"] * factor),
        "iron": round(standards["iron"] * factor),
        "calcium": round(standards["calcium"] * factor),
        "folic_acid": round(standards["folic_acid"] * factor),
        "vitamin_d": round(standards["vitamin_d"] * factor),
        "vitamin_c": round(standards["vitamin_c"] * factor),
        "fiber": round(standards["fiber"] * factor)
    }
    
    return jsonify({
        "required": standards,
        "current": current
    })

# =====================================================
# Food Intake Analysis API
# =====================================================
@app.route("/analyze-food-intake", methods=["POST", "OPTIONS"])
def analyze_food_intake():
    if request.method == "OPTIONS":
        return "", 204
    
    detected_foods = {'breakfast': {'items': []}, 'lunch': {'items': []}, 'dinner': {'items': []}}
    all_food_items = []
    
    for meal in ['breakfast', 'lunch', 'dinner']:
        # Process image if uploaded
        if f'{meal}_image' in request.files:
            image_file = request.files[f'{meal}_image']
            if image_file.filename:
                foods_from_image = analyze_image_simple(image_file)
                detected_foods[meal]['items'].extend(foods_from_image)
                all_food_items.extend([{'food': f, 'quantity': 1} for f in foods_from_image])
        
        # Process text input
        text_input = request.form.get(f'{meal}_text', '')
        if text_input:
            foods_from_text = parse_text_input(text_input)
            detected_foods[meal]['items'].extend([f"{item['quantity']} {item['food']}" for item in foods_from_text])
            all_food_items.extend(foods_from_text)
    
    # Calculate total nutrition
    nutrition_summary = calculate_nutrition(all_food_items)
    
    # Generate recommendations
    recommendations = generate_recommendations(nutrition_summary)
    
    return jsonify({
        'detected_foods': detected_foods,
        'nutrition_summary': nutrition_summary,
        'recommendations': recommendations
    })

# =====================================================
# Health Check
# =====================================================
@app.route("/", methods=["GET"])
def health():
    return jsonify({
        "status": "running",
        "service": "Maternal Nutrition AI Backend"
    })

# =====================================================
# Run Server (LOCAL + RENDER)
# =====================================================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
