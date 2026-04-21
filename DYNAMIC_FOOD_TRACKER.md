# 🍽️ DYNAMIC FOOD INTAKE TRACKER - Feature Update

## ✅ Feature: Food Intake Tracker Based on Food Preference

### Overview:
The food intake tracker now dynamically shows/hides food items based on the selected food preference (Vegetarian/Eggetarian/Non-Vegetarian).

---

## 🎯 How It Works

### Food Categories:

**1. Common Foods (Always Visible)**
- ✅ Spinach
- ✅ Dates
- ✅ Ragi
- ✅ Milk
- ✅ Curd
- ✅ Paneer
- ✅ Dal

**2. Eggetarian Foods (Visible for Eggetarian & Non-Vegetarian)**
- 🥚 Egg

**3. Non-Vegetarian Foods (Visible for Non-Vegetarian Only)**
- 🍗 Chicken
- 🐟 Fish

---

## 📊 Visibility Matrix

| Food Item | Vegetarian | Eggetarian | Non-Vegetarian |
|-----------|------------|------------|----------------|
| Spinach   | ✅ Visible | ✅ Visible | ✅ Visible     |
| Dates     | ✅ Visible | ✅ Visible | ✅ Visible     |
| Ragi      | ✅ Visible | ✅ Visible | ✅ Visible     |
| Milk      | ✅ Visible | ✅ Visible | ✅ Visible     |
| Curd      | ✅ Visible | ✅ Visible | ✅ Visible     |
| Paneer    | ✅ Visible | ✅ Visible | ✅ Visible     |
| Dal       | ✅ Visible | ✅ Visible | ✅ Visible     |
| **Egg**   | ❌ Hidden  | ✅ Visible | ✅ Visible     |
| **Chicken** | ❌ Hidden | ❌ Hidden  | ✅ Visible     |
| **Fish**  | ❌ Hidden  | ❌ Hidden  | ✅ Visible     |

---

## 🔧 Technical Implementation

### HTML Changes:
```html
<!-- Common foods - always visible -->
<div class="input-group food-all">
    <label>🥬 Spinach (bowls)</label>
    <input type="number" id="spinach">
</div>

<!-- Eggetarian and Non-Vegetarian only -->
<div class="input-group food-egg food-nonveg" style="display: none;">
    <label>🥚 Egg (pieces)</label>
    <input type="number" id="egg">
</div>

<!-- Non-Vegetarian only -->
<div class="input-group food-nonveg" style="display: none;">
    <label>🍗 Chicken (pieces)</label>
    <input type="number" id="chicken">
</div>

<div class="input-group food-nonveg" style="display: none;">
    <label>🐟 Fish (pieces)</label>
    <input type="number" id="fish">
</div>
```

### JavaScript Logic:
```javascript
function updateFoodIntakeFields() {
    const preference = document.getElementById("foodPreference").value;
    
    // Hide all optional foods first
    document.querySelectorAll(".food-egg, .food-nonveg").forEach(el => {
        el.style.display = "none";
        // Clear values when hiding
        const input = el.querySelector("input");
        if (input) input.value = "";
    });
    
    // Show based on preference
    if (preference === "eggetarian") {
        // Show eggs only
        document.querySelectorAll(".food-egg").forEach(el => {
            el.style.display = "block";
        });
    } else if (preference === "nonvegetarian") {
        // Show eggs, chicken, and fish
        document.querySelectorAll(".food-egg, .food-nonveg").forEach(el => {
            el.style.display = "block";
        });
    }
}
```

### Event Listener:
```javascript
// Trigger on food preference change
document.getElementById("foodPreference").addEventListener("change", updateFoodIntakeFields);

// Initialize on page load
updateFoodIntakeFields();
```

---

## 🧪 Testing Instructions

### Test 1: Vegetarian Mode
1. Select "Vegetarian" from food preference dropdown
2. Scroll to "Track Your Daily Food Intake"
3. ✅ Verify visible: Spinach, Dates, Ragi, Milk, Curd, Paneer, Dal
4. ✅ Verify hidden: Egg, Chicken, Fish
5. Enter values for visible foods
6. Click "Calculate My Nutrition"
7. ✅ Verify calculation works correctly

### Test 2: Eggetarian Mode
1. Select "Eggetarian" from food preference dropdown
2. Scroll to "Track Your Daily Food Intake"
3. ✅ Verify visible: All vegetarian foods + Egg
4. ✅ Verify hidden: Chicken, Fish
5. Enter values including eggs
6. Click "Calculate My Nutrition"
7. ✅ Verify egg protein/iron included in calculation

### Test 3: Non-Vegetarian Mode
1. Select "Non-Vegetarian" from food preference dropdown
2. Scroll to "Track Your Daily Food Intake"
3. ✅ Verify visible: All foods (10 items total)
4. ✅ Verify: Egg, Chicken, Fish all visible
5. Enter values for all foods
6. Click "Calculate My Nutrition"
7. ✅ Verify all foods included in calculation

### Test 4: Dynamic Switching
1. Select "Non-Vegetarian"
2. Enter values for Egg: 2, Chicken: 2, Fish: 1
3. Switch to "Vegetarian"
4. ✅ Verify: Egg, Chicken, Fish fields disappear
5. ✅ Verify: Values are cleared
6. Switch back to "Non-Vegetarian"
7. ✅ Verify: Fields reappear (empty)
8. Re-enter values
9. ✅ Verify: Calculation works

---

## 📊 Nutrition Calculations

### Iron Sources:
- Spinach: 2.7 mg per bowl
- Dates: 0.2 mg per 5 pieces
- Ragi: 3.9 mg per bowl
- Egg: 1.2 mg per piece

### Calcium Sources:
- Milk: 300 mg per glass
- Curd: 150 mg per bowl
- Paneer: 100 mg per 4 pieces

### Protein Sources:
- Paneer: 1.8 g per 4 pieces
- Dal: 9 g per bowl
- Egg: 6 g per piece
- Chicken: 13.5 g per 2 pieces (100g)
- Fish: 11 g per 2 pieces (100g)

### Formula:
```javascript
Iron = (spinach × 2.7) + (dates × 0.2) + (ragi × 3.9) + (egg × 1.2)
Calcium = (milk × 300) + (curd × 150) + (paneer × 100)
Protein = (paneer × 1.8) + (dal × 9) + (egg × 6) + (chicken × 13.5) + (fish × 11)
```

---

## 🎯 User Experience

### Vegetarian User:
- Sees only plant-based and dairy foods
- Clean, focused interface
- No confusion about non-applicable foods

### Eggetarian User:
- Sees vegetarian foods + eggs
- Can track egg consumption
- Egg protein and iron counted

### Non-Vegetarian User:
- Sees all food options
- Can track complete diet
- All protein sources available

---

## 🔄 Automatic Behavior

### On Preference Change:
1. Hidden fields are cleared automatically
2. Only relevant foods shown
3. Grid layout adjusts automatically
4. No manual intervention needed

### On Page Load:
1. Reads current preference
2. Shows appropriate fields
3. Ready for input immediately

---

## 📱 Responsive Design

The food intake grid automatically adjusts:
- **Desktop**: 3 columns
- **Tablet**: 2 columns
- **Mobile**: 1 column

Hidden fields don't affect layout.

---

## ✅ Benefits

1. **Cleaner Interface**: Users only see relevant foods
2. **No Confusion**: Vegetarians don't see meat options
3. **Accurate Tracking**: Only applicable foods counted
4. **Better UX**: Preference-aware interface
5. **Automatic Clearing**: No stale data when switching
6. **Flexible**: Easy to add more foods

---

## 🚀 Future Enhancements

Potential additions:
- [ ] Add more vegetarian protein sources (tofu, quinoa)
- [ ] Add more non-veg options (mutton, prawns)
- [ ] Regional food preferences (North Indian, South Indian)
- [ ] Custom food addition
- [ ] Barcode scanning for packaged foods
- [ ] Meal photo upload with AI recognition

---

## 📝 Files Modified

1. **frontend/dashboard.html**
   - Added CSS classes: `food-all`, `food-egg`, `food-nonveg`
   - Added Fish input field
   - Set initial display states

2. **frontend/dashboard.js**
   - Added `updateFoodIntakeFields()` function
   - Added event listener for preference change
   - Updated calculation to include fish
   - Added auto-clear on hide

---

## 🧪 Complete Test Scenario

```
1. Open dashboard
2. Select "Vegetarian"
3. Count visible food fields → Should be 7
4. Select "Eggetarian"
5. Count visible food fields → Should be 8 (7 + egg)
6. Select "Non-Vegetarian"
7. Count visible food fields → Should be 10 (7 + egg + chicken + fish)
8. Enter values in all fields
9. Switch to "Vegetarian"
10. Verify egg/chicken/fish disappeared
11. Switch back to "Non-Vegetarian"
12. Verify fields reappeared but empty
13. Enter new values
14. Click "Calculate My Nutrition"
15. Verify all foods included in calculation
```

---

## ✅ Feature Status: COMPLETE

The food intake tracker now intelligently adapts to the user's dietary preference, providing a personalized and relevant tracking experience.

**Test Command:**
```bash
cd backend
python app.py
# Open frontend/dashboard.html
# Test all 3 preferences
```

---

**Implementation Date**: 2026-04-03
**Status**: ✅ COMPLETE
**Quality**: Production Ready
