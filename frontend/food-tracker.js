const API_BASE_URL = 'http://127.0.0.1:5000';

function previewImage(mealType) {
    const input = document.getElementById(`${mealType}-image`);
    const preview = document.getElementById(`${mealType}-preview`);
    
    if (input.files && input.files[0]) {
        const reader = new FileReader();
        reader.onload = function(e) {
            preview.innerHTML = `<img src="${e.target.result}" alt="${mealType}">`;
        };
        reader.readAsDataURL(input.files[0]);
    }
}

async function analyzeFoodIntake() {
    const btn = document.getElementById('analyzeBtn');
    btn.disabled = true;
    btn.textContent = '🔄 Analyzing...';

    const formData = new FormData();
    
    // Collect images
    ['breakfast', 'lunch', 'dinner'].forEach(meal => {
        const imageInput = document.getElementById(`${meal}-image`);
        const textInput = document.getElementById(`${meal}-text`).value;
        
        if (imageInput.files[0]) {
            formData.append(`${meal}_image`, imageInput.files[0]);
        }
        formData.append(`${meal}_text`, textInput);
    });

    try {
        const response = await fetch(`${API_BASE_URL}/analyze-food-intake`, {
            method: 'POST',
            body: formData
        });

        const data = await response.json();
        displayResults(data);
        
        document.getElementById('resultsSection').style.display = 'block';
        document.getElementById('resultsSection').scrollIntoView({ behavior: 'smooth' });
    } catch (error) {
        alert('Error analyzing food intake. Please try again.');
        console.error(error);
    } finally {
        btn.disabled = false;
        btn.textContent = '🔍 Analyze My Food Intake';
    }
}

function displayResults(data) {
    displayDetectedFoods(data.detected_foods);
    displayNutritionSummary(data.nutrition_summary);
    displayRecommendations(data.recommendations);
}

function displayDetectedFoods(foods) {
    const container = document.getElementById('detectedFoods');
    container.innerHTML = '';

    Object.keys(foods).forEach(meal => {
        const mealData = foods[meal];
        const card = document.createElement('div');
        card.className = 'food-card';
        
        const mealIcon = meal === 'breakfast' ? '🌅' : meal === 'lunch' ? '☀️' : '🌙';
        
        card.innerHTML = `
            <span class="meal-type">${mealIcon} ${meal.toUpperCase()}</span>
            <h4>Detected Items</h4>
            <ul>
                ${mealData.items.map(item => `<li>${item}</li>`).join('')}
            </ul>
        `;
        container.appendChild(card);
    });
}

function displayNutritionSummary(summary) {
    const container = document.getElementById('nutritionSummary');
    container.innerHTML = '';

    const nutrients = [
        { name: 'Calories', value: summary.calories, target: 2200, unit: 'kcal' },
        { name: 'Protein', value: summary.protein, target: 80, unit: 'g' },
        { name: 'Iron', value: summary.iron, target: 27, unit: 'mg' },
        { name: 'Calcium', value: summary.calcium, target: 1200, unit: 'mg' }
    ];

    nutrients.forEach(nutrient => {
        const percentage = Math.min((nutrient.value / nutrient.target) * 100, 100);
        const item = document.createElement('div');
        item.className = 'nutrition-item';
        
        item.innerHTML = `
            <h4>${nutrient.name}</h4>
            <div class="nutrition-value">${nutrient.value}</div>
            <div class="nutrition-target">Target: ${nutrient.target} ${nutrient.unit}</div>
            <div class="progress-bar">
                <div class="progress-fill" style="width: ${percentage}%"></div>
            </div>
        `;
        container.appendChild(item);
    });
}

function displayRecommendations(recommendations) {
    const container = document.getElementById('recommendations');
    container.innerHTML = '';

    recommendations.forEach(rec => {
        const item = document.createElement('div');
        item.className = 'recommendation-item';
        
        item.innerHTML = `
            <h4>${rec.title}</h4>
            <p>${rec.message}</p>
            <ul>
                ${rec.foods.map(food => `<li>${food}</li>`).join('')}
            </ul>
        `;
        container.appendChild(item);
    });
}
