import joblib
import numpy as np

model = joblib.load('ml/model.pkl')
le = joblib.load('ml/label_encoder.pkl')

print("Testing different health values to find Low risk patterns:\n")

test_cases = [
    [20, 100, 60, 6.0, 98.0, 70],
    [22, 105, 65, 6.2, 98.2, 68],
    [24, 110, 70, 6.5, 98.4, 72],
    [25, 115, 75, 6.5, 98.6, 72],
    [28, 120, 80, 7.5, 98.6, 75],
    [30, 125, 82, 7.8, 98.8, 80],
    [35, 140, 95, 9.5, 99.2, 95],
    [23, 108, 68, 6.3, 98.3, 70],
    [26, 112, 72, 6.8, 98.5, 74]
]

for i, features in enumerate(test_cases, 1):
    pred = model.predict([features])
    risk = le.inverse_transform(pred)[0]
    print(f"Test {i}: Age={features[0]}, BP={features[1]}/{features[2]}, BS={features[3]}, Temp={features[4]}, HR={features[5]}")
    print(f"   → Risk: {risk}\n")
