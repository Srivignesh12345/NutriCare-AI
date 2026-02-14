import os
import joblib
import numpy as np
from datetime import datetime

from flask import Flask, request, jsonify
from flask_cors import CORS

from diet_engine import generate_diet

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
        cred = credentials.Certificate(
            os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
        )
        firebase_admin.initialize_app(cred)

    db = firestore.client()
    print("✅ Firebase connected")

except Exception as e:
    print("⚠️ Firebase disabled:", e)

# =====================================================
# Analyze API
# =====================================================
@app.route("/analyze", methods=["POST", "OPTIONS"])
def analyze():
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
    data = request.get_json()

    risk = data.get("risk", "Medium")
    duration = data.get("duration", "week")

    days = 7 if duration == "week" else 30
    diet = generate_diet(days, risk)

    response = {
        "risk": risk,
        "duration": duration,
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
