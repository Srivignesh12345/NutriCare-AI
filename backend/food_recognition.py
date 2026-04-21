import re
from PIL import Image
import numpy as np

# Indian food database with nutrition per serving
FOOD_DATABASE = {
    'idli': {'calories': 39, 'protein': 2, 'iron': 0.5, 'calcium': 10},
    'dosa': {'calories': 133, 'protein': 3, 'iron': 1.2, 'calcium': 15},
    'sambar': {'calories': 80, 'protein': 4, 'iron': 1.5, 'calcium': 30},
    'rice': {'calories': 130, 'protein': 2.7, 'iron': 0.2, 'calcium': 10},
    'chapati': {'calories': 71, 'protein': 3, 'iron': 0.7, 'calcium': 8},
    'roti': {'calories': 71, 'protein': 3, 'iron': 0.7, 'calcium': 8},
    'dal': {'calories': 110, 'protein': 9, 'iron': 2.5, 'calcium': 40},
    'milk': {'calories': 103, 'protein': 8, 'iron': 0.1, 'calcium': 300},
    'curd': {'calories': 60, 'protein': 3.5, 'iron': 0.1, 'calcium': 150},
    'egg': {'calories': 78, 'protein': 6, 'iron': 1.2, 'calcium': 28},
    'chicken': {'calories': 165, 'protein': 27, 'iron': 1, 'calcium': 15},
    'fish': {'calories': 206, 'protein': 22, 'iron': 1.5, 'calcium': 20},
    'spinach': {'calories': 23, 'protein': 2.9, 'iron': 2.7, 'calcium': 99},
    'potato': {'calories': 77, 'protein': 2, 'iron': 0.8, 'calcium': 12},
    'tomato': {'calories': 18, 'protein': 0.9, 'iron': 0.3, 'calcium': 10},
    'carrot': {'calories': 41, 'protein': 0.9, 'iron': 0.3, 'calcium': 33},
    'banana': {'calories': 89, 'protein': 1.1, 'iron': 0.3, 'calcium': 5},
    'apple': {'calories': 52, 'protein': 0.3, 'iron': 0.1, 'calcium': 6},
    'orange': {'calories': 47, 'protein': 0.9, 'iron': 0.1, 'calcium': 40},
    'paneer': {'calories': 265, 'protein': 18, 'iron': 0.2, 'calcium': 480},
    'vegetables': {'calories': 50, 'protein': 2, 'iron': 1, 'calcium': 40},
    'salad': {'calories': 30, 'protein': 1, 'iron': 0.5, 'calcium': 20},
    'curry': {'calories': 120, 'protein': 5, 'iron': 2, 'calcium': 50},
}

def analyze_image_simple(image_file):
    """Simple image analysis - detects dominant colors to guess food type"""
    try:
        img = Image.open(image_file)
        img = img.resize((100, 100))
        img_array = np.array(img)
        
        # Calculate average RGB
        avg_color = img_array.mean(axis=(0, 1))
        
        # Simple heuristic based on color
        detected = []
        if avg_color[0] > 150 and avg_color[1] < 100:  # Reddish
            detected.append('tomato')
        if avg_color[1] > 150:  # Greenish
            detected.append('spinach')
        if avg_color[0] > 200 and avg_color[1] > 150:  # Yellowish/White
            detected.extend(['rice', 'chapati'])
        if avg_color[0] > 100 and avg_color[1] > 80 and avg_color[2] < 80:  # Brownish
            detected.extend(['dal', 'curry'])
            
        return detected if detected else ['rice', 'dal', 'vegetables']
    except:
        return ['rice', 'dal', 'vegetables']

def parse_text_input(text):
    """Extract food items and quantities from text"""
    text = text.lower()
    detected = []
    
    for food in FOOD_DATABASE.keys():
        if food in text:
            # Extract quantity
            pattern = rf'(\d+(?:\.\d+)?)\s*(?:bowl|glass|piece|cup)?s?\s*(?:of\s+)?{food}'
            match = re.search(pattern, text)
            quantity = float(match.group(1)) if match else 1
            detected.append({'food': food, 'quantity': quantity})
    
    return detected

def calculate_nutrition(food_items):
    """Calculate total nutrition from food items"""
    total = {'calories': 0, 'protein': 0, 'iron': 0, 'calcium': 0}
    
    for item in food_items:
        food = item['food']
        quantity = item['quantity']
        if food in FOOD_DATABASE:
            for nutrient in total.keys():
                total[nutrient] += FOOD_DATABASE[food][nutrient] * quantity
    
    return {k: round(v, 1) for k, v in total.items()}

def generate_recommendations(nutrition_summary):
    """Generate food recommendations based on deficiencies"""
    recommendations = []
    
    # Pregnancy standards
    targets = {'calories': 2200, 'protein': 80, 'iron': 27, 'calcium': 1200}
    
    if nutrition_summary['calories'] < targets['calories'] * 0.7:
        recommendations.append({
            'title': '⚡ Increase Calorie Intake',
            'message': f"You've consumed {nutrition_summary['calories']} kcal. You need {targets['calories']} kcal daily.",
            'foods': ['Banana', 'Dates', 'Nuts', 'Ghee', 'Brown Rice']
        })
    
    if nutrition_summary['protein'] < targets['protein'] * 0.7:
        recommendations.append({
            'title': '💪 Boost Protein Intake',
            'message': f"You've consumed {nutrition_summary['protein']}g protein. Target: {targets['protein']}g daily.",
            'foods': ['Dal', 'Paneer', 'Eggs', 'Chicken', 'Fish', 'Rajma']
        })
    
    if nutrition_summary['iron'] < targets['iron'] * 0.7:
        recommendations.append({
            'title': '🩸 Increase Iron-Rich Foods',
            'message': f"You've consumed {nutrition_summary['iron']}mg iron. Target: {targets['iron']}mg daily.",
            'foods': ['Spinach', 'Dates', 'Ragi', 'Pomegranate', 'Beetroot', 'Jaggery']
        })
    
    if nutrition_summary['calcium'] < targets['calcium'] * 0.7:
        recommendations.append({
            'title': '🦴 Add More Calcium',
            'message': f"You've consumed {nutrition_summary['calcium']}mg calcium. Target: {targets['calcium']}mg daily.",
            'foods': ['Milk', 'Curd', 'Paneer', 'Sesame Seeds', 'Ragi', 'Cheese']
        })
    
    if not recommendations:
        recommendations.append({
            'title': '✅ Great Job!',
            'message': 'Your nutrition intake is well-balanced. Keep it up!',
            'foods': ['Continue your current diet', 'Stay hydrated', 'Add variety']
        })
    
    return recommendations
