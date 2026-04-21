import pandas as pd
import random

foods = pd.read_csv("datasets/nutrition_foods.csv")

def generate_diet_plan(days=7):
    plan = {}

    for day in range(1, days + 1):
        plan[f"Day {day}"] = {
            "Breakfast": random.sample(list(foods["food"]), 2),
            "Lunch": random.sample(list(foods["food"]), 2),
            "Dinner": random.sample(list(foods["food"]), 2)
        }

    return plan
