import random

FOODS = {
    "Breakfast": [
        "Milk + Dates",
        "Oats + Banana",
        "Boiled Egg + Toast",
        "Fruit Bowl",
        "Vegetable Omelette"
    ],
    "Lunch": [
        "Brown Rice + Dal + Spinach",
        "Chapati + Vegetable Curry",
        "Rice + Sambar",
        "Vegetable Khichdi",
        "Curd Rice"
    ],
    "Dinner": [
        "Soup + Salad",
        "Chapati + Paneer",
        "Steamed Vegetables",
        "Light Rice + Dal",
        "Vegetable Stir Fry"
    ]
}

def generate_diet(days, risk):
    plan = {}

    for day in range(1, days + 1):
        plan[f"Day {day}"] = {
            "Breakfast": random.choice(FOODS["Breakfast"]),
            "Lunch": random.choice(FOODS["Lunch"]),
            "Dinner": random.choice(FOODS["Dinner"]),
            "Note": (
                "Iron-rich foods recommended"
                if risk == "High"
                else "Balanced nutrition recommended"
            )
        }

    return plan
