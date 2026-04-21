import pandas as pd
from nutrition_rules import NUTRITION_STANDARDS

food_data = pd.DataFrame([
    {"food": "Ragi", "calories": 336, "protein": 7.3, "iron": 3.9, "calcium": 344},
    {"food": "Spinach", "calories": 23, "protein": 2.9, "iron": 2.7, "calcium": 99},
    {"food": "Egg", "calories": 155, "protein": 13, "iron": 1.2, "calcium": 50},
    {"food": "Milk", "calories": 60, "protein": 3.2, "iron": 0.1, "calcium": 120},
    {"food": "Dates", "calories": 277, "protein": 1.8, "iron": 1.0, "calcium": 39}
])

def check_deficiency(user_type, intake):
    required = NUTRITION_STANDARDS[user_type]
    deficiency = {}

    for n in required:
        if intake.get(n, 0) < required[n]:
            deficiency[n] = required[n] - intake.get(n, 0)
    return deficiency

def recommend_foods(deficiency):
    recommendations = []
    for nutrient in deficiency:
        top_foods = food_data.sort_values(by=nutrient, ascending=False).head(3)
        recommendations.append({
            "nutrient": nutrient,
            "foods": top_foods["food"].tolist()
        })
    return recommendations
