import random

FOODS = {
    "vegetarian": {
        "Breakfast": [
            "Ragi Porridge + Banana",
            "Poha + Peanuts + Tea",
            "Idli + Sambar + Chutney",
            "Upma + Vegetables",
            "Dosa + Potato Curry",
            "Paratha + Curd",
            "Daliya + Milk",
            "Bread + Peanut Butter + Banana"
        ],
        "Lunch": [
            "Rice + Dal + Spinach Curry",
            "Chapati + Rajma + Salad",
            "Rice + Sambar + Vegetable Stir Fry",
            "Chapati + Mixed Vegetable Curry + Curd",
            "Rice + Chole + Onion",
            "Chapati + Dal + Green Vegetables",
            "Rice + Kadhi + Aloo",
            "Chapati + Peas Curry + Raita"
        ],
        "Dinner": [
            "Khichdi + Curd + Pickle",
            "Chapati + Dal + Vegetable",
            "Rice + Sambar + Carrot Salad",
            "Vegetable Soup + Chapati",
            "Dal Rice + Tomato Chutney",
            "Chapati + Rajma + Salad",
            "Rice + Kadhi + Papad",
            "Vegetable Khichdi + Curd"
        ]
    },
    "eggetarian": {
        "Breakfast": [
            "Boiled Egg + Bread + Tea",
            "Egg Bhurji + Chapati",
            "Poha + Boiled Egg",
            "Idli + Egg Curry",
            "Bread Omelette + Banana",
            "Upma + Boiled Egg",
            "Paratha + Egg Curry",
            "Ragi Porridge + Boiled Egg"
        ],
        "Lunch": [
            "Rice + Dal + Egg Curry",
            "Chapati + Egg Masala + Salad",
            "Rice + Sambar + Egg Fry",
            "Chapati + Rajma + Boiled Egg",
            "Egg Fried Rice + Raita",
            "Rice + Egg Curry + Vegetables",
            "Chapati + Dal + Egg",
            "Rice + Chole + Egg"
        ],
        "Dinner": [
            "Khichdi + Boiled Egg + Curd",
            "Chapati + Egg Curry + Salad",
            "Rice + Dal + Egg",
            "Vegetable Soup + Boiled Egg",
            "Dal Rice + Egg Fry",
            "Chapati + Egg Masala",
            "Rice + Egg Curry + Papad",
            "Egg Khichdi + Curd"
        ]
    },
    "nonvegetarian": {
        "Breakfast": [
            "Boiled Egg + Bread + Tea",
            "Egg Bhurji + Chapati",
            "Poha + Boiled Egg",
            "Idli + Egg Curry",
            "Bread Omelette + Banana",
            "Upma + Boiled Egg",
            "Paratha + Egg Curry",
            "Ragi Porridge + Boiled Egg"
        ],
        "Lunch": [
            "Rice + Dal + Chicken Curry",
            "Chapati + Chicken Curry + Salad",
            "Rice + Fish Curry + Vegetables",
            "Chapati + Egg Curry + Dal",
            "Chicken Biryani + Raita",
            "Rice + Fish Fry + Sambar",
            "Chapati + Chicken + Rajma",
            "Rice + Egg Curry + Vegetables"
        ],
        "Dinner": [
            "Khichdi + Chicken + Curd",
            "Chapati + Chicken Curry + Salad",
            "Rice + Dal + Fish",
            "Chicken Soup + Chapati",
            "Dal Rice + Egg Fry",
            "Chapati + Fish Curry",
            "Rice + Chicken + Papad",
            "Egg Khichdi + Curd"
        ]
    }
}

RISK_NOTES = {
    "High": [
        "Focus on iron-rich foods (Spinach, Ragi, Rajma)",
        "Increase protein intake (Eggs, Dal, Chicken)",
        "Avoid high sugar and processed foods",
        "Stay hydrated - drink 8-10 glasses of water"
    ],
    "Medium": [
        "Maintain balanced nutrition",
        "Include variety of vegetables and fruits",
        "Ensure adequate calcium intake",
        "Regular small meals throughout the day"
    ],
    "Low": [
        "Continue healthy eating habits",
        "Include seasonal fruits and vegetables",
        "Maintain regular meal timings",
        "Stay active with light exercise"
    ],
    "Normal": [
        "Continue healthy eating habits",
        "Include seasonal fruits and vegetables",
        "Maintain regular meal timings",
        "Stay active with light exercise"
    ]
}

EXERCISES = {
    "High": [
        "Gentle Walking - 10 minutes (morning)",
        "Deep Breathing - 5 minutes (3 times a day)",
        "Prenatal Yoga - 15 minutes (evening)",
        "Ankle Rotations - 10 reps (sitting)",
        "Pelvic Tilts - 10 reps (lying down)",
        "Shoulder Rolls - 10 reps (sitting)",
        "Meditation - 10 minutes (before sleep)"
    ],
    "Medium": [
        "Brisk Walking - 20 minutes (morning)",
        "Prenatal Yoga - 20 minutes (evening)",
        "Swimming - 15 minutes (if available)",
        "Kegel Exercises - 10 reps (3 times a day)",
        "Cat-Cow Stretch - 10 reps (morning)",
        "Squats - 10 reps (with support)",
        "Breathing Exercises - 10 minutes (evening)"
    ],
    "Low": [
        "Walking - 30 minutes (morning/evening)",
        "Prenatal Yoga - 30 minutes (daily)",
        "Swimming - 20 minutes (3 times a week)",
        "Squats - 15 reps (with support)",
        "Pelvic Floor Exercises - 15 reps (daily)",
        "Stretching - 15 minutes (morning)",
        "Light Aerobics - 20 minutes (3 times a week)"
    ],
    "Normal": [
        "Walking - 30 minutes (morning/evening)",
        "Prenatal Yoga - 30 minutes (daily)",
        "Swimming - 20 minutes (3 times a week)",
        "Squats - 15 reps (with support)",
        "Pelvic Floor Exercises - 15 reps (daily)",
        "Stretching - 15 minutes (morning)",
        "Light Aerobics - 20 minutes (3 times a week)"
    ]
}

def generate_diet(days, risk, food_preference="vegetarian"):
    plan = {}
    # Support both "Low" and "Normal" for backward compatibility
    if risk.lower() == "normal":
        risk = "Low"
    risk_key = risk if risk in RISK_NOTES else "Medium"
    notes = RISK_NOTES[risk_key]
    exercises = EXERCISES[risk_key]
    
    # Get food list based on preference
    food_list = FOODS.get(food_preference.lower(), FOODS["vegetarian"])

    for day in range(1, days + 1):
        note_index = (day - 1) % len(notes)
        exercise_index = (day - 1) % len(exercises)
        plan[f"Day {day}"] = {
            "Breakfast": random.choice(food_list["Breakfast"]),
            "Lunch": random.choice(food_list["Lunch"]),
            "Dinner": random.choice(food_list["Dinner"]),
            "Exercise": exercises[exercise_index],
            "Note": notes[note_index]
        }

    return plan
