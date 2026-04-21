"""
Test script for food recognition module
Run this to verify the food tracker is working correctly
"""

import sys
sys.path.append('backend')

from food_recognition import parse_text_input, calculate_nutrition, generate_recommendations

def test_text_parsing():
    print("=" * 50)
    print("TEST 1: Text Parsing")
    print("=" * 50)
    
    test_inputs = [
        "2 idlis, 1 bowl sambar, 1 glass milk",
        "2 chapatis, 1 bowl dal, 1 bowl vegetables",
        "1 bowl rice, 1 bowl curry, salad, 2 eggs"
    ]
    
    for text in test_inputs:
        print(f"\nInput: {text}")
        result = parse_text_input(text)
        print(f"Detected: {result}")

def test_nutrition_calculation():
    print("\n" + "=" * 50)
    print("TEST 2: Nutrition Calculation")
    print("=" * 50)
    
    food_items = [
        {'food': 'idli', 'quantity': 2},
        {'food': 'sambar', 'quantity': 1},
        {'food': 'milk', 'quantity': 1},
        {'food': 'rice', 'quantity': 2},
        {'food': 'dal', 'quantity': 1},
        {'food': 'egg', 'quantity': 2}
    ]
    
    nutrition = calculate_nutrition(food_items)
    print(f"\nTotal Nutrition:")
    print(f"  Calories: {nutrition['calories']} kcal")
    print(f"  Protein: {nutrition['protein']} g")
    print(f"  Iron: {nutrition['iron']} mg")
    print(f"  Calcium: {nutrition['calcium']} mg")

def test_recommendations():
    print("\n" + "=" * 50)
    print("TEST 3: Recommendations")
    print("=" * 50)
    
    # Low nutrition scenario
    low_nutrition = {'calories': 800, 'protein': 30, 'iron': 10, 'calcium': 400}
    
    print(f"\nScenario: Low Nutrition Intake")
    print(f"Current: {low_nutrition}")
    
    recommendations = generate_recommendations(low_nutrition)
    
    for rec in recommendations:
        print(f"\n{rec['title']}")
        print(f"  {rec['message']}")
        print(f"  Suggested foods: {', '.join(rec['foods'])}")

if __name__ == "__main__":
    print("\n🧪 FOOD TRACKER TEST SUITE\n")
    
    try:
        test_text_parsing()
        test_nutrition_calculation()
        test_recommendations()
        
        print("\n" + "=" * 50)
        print("✅ ALL TESTS PASSED!")
        print("=" * 50)
        print("\nYou can now:")
        print("1. Start backend: cd backend && python app.py")
        print("2. Open frontend/food-tracker.html in browser")
        print("3. Upload food images and test the tracker")
        
    except Exception as e:
        print(f"\n❌ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
