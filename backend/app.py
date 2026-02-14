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
CORS(app)

# =====================================================
# Firebase (Safe Initialization)
# =====================================================
db = None
firestore = None

try:
    import firebase_admin
    from firebase_admin import credentials, firestore

    if not firebase_admin._apps:
        cred = credentials.Certificate("firebase_key.json")
        firebase_admin.initialize_app(cred)

    db = firestore.client()
    print("✅ Firebase connected")

except Exception as e:
    print("⚠️ Firebase disabled:", e)

# =====================================================
# Analyze API (ML Prediction)
# =====================================================
@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.json

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
        "age": data["age"],
        "systolicbp": data["systolicbp"],
        "diastolicbp": data["diastolicbp"],
        "bs": data["bs"],
        "bodytemp": data["bodytemp"],
        "heartrate": data["heartrate"],
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
# Diet Plan API (Weekly / Monthly)
# =====================================================
@app.route("/diet-plan", methods=["POST"])
def diet_plan():
    data = request.json

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

    docs = db.collection("nutrition_reports") \
             .order_by("timestamp", direction=firestore.Query.DESCENDING) \
             .stream()

    return jsonify([doc.to_dict() for doc in docs])

# =====================================================
# Health Check API (Optional but Professional)
# =====================================================
@app.route("/", methods=["GET"])
def health():
    return jsonify({
        "status": "running",
        "service": "Maternal Nutrition AI Backend"
    })

# =====================================================
# Run Server
# =====================================================
if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
