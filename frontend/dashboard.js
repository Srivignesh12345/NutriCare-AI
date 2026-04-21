const API_BASE_URL = "http://127.0.0.1:5000";

let currentHealthData = null;
let nutritionChart = null;
let currentDuration = "week";
let currentWeek = 1;
let nutritionData = null;

// Navigation
document.addEventListener("DOMContentLoaded", () => {
    const navBtns = document.querySelectorAll(".nav-btn");
    const views = document.querySelectorAll(".dashboard-view");

    navBtns.forEach(btn => {
        btn.addEventListener("click", () => {
            const view = btn.dataset.view;
            
            navBtns.forEach(b => b.classList.remove("active"));
            btn.classList.add("active");
            
            views.forEach(v => v.classList.remove("active"));
            document.getElementById(view + "View").classList.add("active");
        });
    });

    document.getElementById("analyzeBtn").addEventListener("click", analyzeHealth);
    
    // Food preference change listener
    document.getElementById("foodPreference").addEventListener("change", updateFoodIntakeFields);
    
    initNutritionChart();
    updateFoodIntakeFields(); // Initialize on load
    
    // Initialize time-based meal tracker
    updateMealTimeDisplay();
    setInterval(updateMealTimeDisplay, 60000); // Update every minute
    loadSavedMeals();
});

// Update Food Intake Fields based on preference
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
    // For vegetarian, everything stays hidden
}

// Analyze Health
async function analyzeHealth() {
    const data = {
        age: Number(document.getElementById("age").value),
        systolicbp: Number(document.getElementById("systolicbp").value),
        diastolicbp: Number(document.getElementById("diastolicbp").value),
        bs: Number(document.getElementById("bs").value),
        bodytemp: Number(document.getElementById("bodytemp").value),
        heartrate: Number(document.getElementById("heartrate").value)
    };

    for (let key in data) {
        if (isNaN(data[key]) || data[key] === 0) {
            alert("Please fill all fields correctly");
            return;
        }
    }

    currentHealthData = data;
    currentDuration = document.getElementById("duration").value;

    try {
        const response = await fetch(`${API_BASE_URL}/analyze`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(data)
        });

        if (!response.ok) throw new Error("Analysis failed");

        const result = await response.json();
        
        displayHealthStatus(data);
        displayRiskLevel(result.risk);
        await fetchNutritionNeeds(result.risk, data.age);
        generateAlerts(data, result.risk);
        generateAIRecommendations(result.risk, data);
        await generateDietPlan(result.risk);
        updateNutritionChart();

    } catch (err) {
        console.error("Error:", err);
        alert("Backend not reachable. Make sure Flask server is running.");
    }
}

// Fetch Nutrition Needs from API
async function fetchNutritionNeeds(risk, age) {
    try {
        const response = await fetch(`${API_BASE_URL}/nutrition-needs`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ risk, age })
        });

        if (!response.ok) throw new Error("Failed to fetch nutrition needs");

        nutritionData = await response.json();
        displayNutritionNeeds(nutritionData);

    } catch (err) {
        console.error("Error:", err);
    }
}

// Display Nutrition Needs
function displayNutritionNeeds(data) {
    const nutrients = [
        { name: "Calories", unit: "kcal", key: "calories" },
        { name: "Protein", unit: "g", key: "protein" },
        { name: "Iron", unit: "mg", key: "iron" },
        { name: "Calcium", unit: "mg", key: "calcium" },
        { name: "Folic Acid", unit: "mcg", key: "folic_acid" },
        { name: "Vitamin D", unit: "IU", key: "vitamin_d" },
        { name: "Vitamin C", unit: "mg", key: "vitamin_c" },
        { name: "Fiber", unit: "g", key: "fiber" }
    ];

    let html = "";
    nutrients.forEach(nutrient => {
        const required = data.required[nutrient.key];
        const current = data.current[nutrient.key];
        const percentage = (current / required) * 100;
        const status = percentage < 70 ? "Low" : percentage < 90 ? "Medium" : "Good";
        const statusClass = status === "Low" ? "status-low" : status === "Medium" ? "status-medium" : "status-good";

        html += `
            <tr>
                <td>${nutrient.name}</td>
                <td>${required} ${nutrient.unit}</td>
                <td>${current} ${nutrient.unit}</td>
                <td class="${statusClass}">${status}</td>
            </tr>
        `;
    });

    document.getElementById("deficiencyBody").innerHTML = html;
}

// Display Health Status
function displayHealthStatus(data) {
    const html = `
        <p><strong>Age:</strong> ${data.age} years</p>
        <p><strong>Blood Pressure:</strong> ${data.systolicbp}/${data.diastolicbp} mmHg</p>
        <p><strong>Blood Sugar:</strong> ${data.bs} mmol/L</p>
        <p><strong>Body Temp:</strong> ${data.bodytemp}°F</p>
        <p><strong>Heart Rate:</strong> ${data.heartrate} bpm</p>
    `;
    document.getElementById("healthDisplay").innerHTML = html;
}

// Display Risk Level
function displayRiskLevel(risk) {
    // Convert Low to Normal for display
    const displayRisk = risk.toLowerCase() === "low" ? "Normal" : risk;
    const riskClass = risk.toLowerCase() === "low" ? "risk-low" : risk.toLowerCase() === "high" ? "risk-high" : "risk-medium";
    const html = `
        <div class="risk-badge ${riskClass}">
            ${displayRisk.toUpperCase()} RISK
        </div>
        <p style="margin-top: 15px; color: #666;">
            ${getRiskMessage(risk)}
        </p>
    `;
    document.getElementById("riskDisplay").innerHTML = html;
}

function getRiskMessage(risk) {
    const messages = {
        "low": "Great news! Your health indicators look good. Keep up the healthy habits and continue with a balanced diet.",
        "medium": "Your health needs some attention. Don't worry - following our personalized nutrition plan will help improve your wellness.",
        "high": "We recommend consulting your doctor soon. Meanwhile, follow the nutrition plan carefully to support your health."
    };
    return messages[risk.toLowerCase()] || messages["medium"];
}

// Generate Health Alerts
function generateAlerts(data, risk) {
    const alerts = [];

    if (data.bs > 7.8) {
        alerts.push({
            type: "warning",
            message: "Your blood sugar is a bit high. Let's focus on low-sugar foods and avoid sweets for now."
        });
    }

    if (data.systolicbp > 130 || data.diastolicbp > 85) {
        alerts.push({
            type: "danger",
            message: "Your blood pressure needs attention. Try reducing salt intake and include more potassium-rich foods like bananas."
        });
    }

    if (risk.toLowerCase() === "high") {
        alerts.push({
            type: "danger",
            message: "Please consult your doctor soon. We've created a special iron-rich diet plan to support your health."
        });
    }

    if (data.heartrate > 100) {
        alerts.push({
            type: "warning",
            message: "Your heart rate is elevated. Make sure you're getting enough rest and staying hydrated."
        });
    }

    let html = "";
    alerts.forEach(alert => {
        html += `<div class="alert alert-${alert.type}">${alert.message}</div>`;
    });

    document.getElementById("alertsSection").innerHTML = html;
}

// AI Recommendations
function generateAIRecommendations(risk, data) {
    const recommendations = [];

    if (risk.toLowerCase() === "high" || data.bs > 8) {
        recommendations.push({
            title: "Boost Your Iron Levels",
            foods: ["Spinach", "Dates", "Ragi", "Pomegranate", "Beetroot"],
            note: "These foods will help increase your hemoglobin naturally"
        });
    }

    if (data.age > 30) {
        recommendations.push({
            title: "Strengthen Your Bones",
            foods: ["Milk", "Yogurt", "Cheese", "Sesame Seeds", "Almonds"],
            note: "Essential for your bones and your baby's development"
        });
    }

    if (data.bs > 7.8) {
        recommendations.push({
            title: "Manage Blood Sugar Naturally",
            foods: ["Oats", "Brown Rice", "Quinoa", "Green Vegetables"],
            note: "Avoid: White sugar, white rice, and processed foods"
        });
    }

    if (data.systolicbp > 130) {
        recommendations.push({
            title: "Keep Your Blood Pressure Healthy",
            foods: ["Banana", "Spinach", "Garlic", "Beetroot"],
            note: "Avoid: Excess salt, pickles, and processed snacks"
        });
    }

    recommendations.push({
        title: "Essential Pregnancy Superfoods",
        foods: ["Eggs", "Dal", "Green Vegetables", "Fresh Fruits", "Nuts"],
        note: "Include these daily for complete nutrition"
    });

    let html = "";
    recommendations.forEach(rec => {
        html += `
            <div class="recommendation-card">
                <h4>${rec.title}</h4>
                <ul>
                    ${rec.foods.map(food => `<li>${food}</li>`).join("")}
                </ul>
                ${rec.note ? `<p style="margin-top: 10px; font-size: 12px; opacity: 0.9;">${rec.note}</p>` : ''}
            </div>
        `;
    });

    document.getElementById("aiRecommendations").innerHTML = html;
}

// Generate Diet Plan
async function generateDietPlan(risk) {
    const duration = document.getElementById("duration").value;
    const foodPreference = document.getElementById("foodPreference").value;
    
    // Show loading state
    document.getElementById("dietPlan").innerHTML = '<p class="placeholder-text">🔄 Generating your personalized diet plan...</p>';

    try {
        const response = await fetch(`${API_BASE_URL}/diet-plan`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ risk, duration, food_preference: foodPreference })
        });

        if (!response.ok) throw new Error("Diet plan generation failed");

        const data = await response.json();
        displayDietPlan(data.diet_plan, duration);

    } catch (err) {
        console.error("Error:", err);
        document.getElementById("dietPlan").innerHTML = "<p class='placeholder-text'>❌ Failed to generate diet plan. Please check if the backend server is running.</p>";
    }
}

function displayDietPlan(plan, duration) {
    const sortedDays = Object.keys(plan).sort((a, b) => {
        const numA = parseInt(a.replace(/\D/g, ""));
        const numB = parseInt(b.replace(/\D/g, ""));
        return numA - numB;
    });

    let html = "";
    sortedDays.forEach(day => {
        const meal = plan[day];
        html += `
            <div class="day-card">
                <h4>${day}</h4>
                <p><strong>Breakfast:</strong> ${meal.Breakfast}</p>
                <p><strong>Lunch:</strong> ${meal.Lunch}</p>
                <p><strong>Dinner:</strong> ${meal.Dinner}</p>
                <p><strong>Exercise:</strong> ${meal.Exercise}</p>
                <p style="margin-top: 10px; font-style: italic; opacity: 0.9;">${meal.Note}</p>
            </div>
        `;
    });

    document.getElementById("dietPlan").innerHTML = html;
    
    // Show chart controls for 30-day plan
    if (duration === "month") {
        document.getElementById("chartControls").style.display = "block";
        document.getElementById("weekSelector").style.display = "block";
    } else {
        document.getElementById("chartControls").style.display = "block";
        document.getElementById("weekSelector").style.display = "none";
    }
}

// Nutrition Progress Chart
function initNutritionChart() {
    const ctx = document.getElementById("nutritionChart").getContext("2d");
    
    nutritionChart = new Chart(ctx, {
        type: "line",
        data: {
            labels: ["Day 1", "Day 2", "Day 3", "Day 4", "Day 5", "Day 6", "Day 7"],
            datasets: [
                {
                    label: "Iron (mg)",
                    data: [0, 0, 0, 0, 0, 0, 0],
                    borderColor: "#e74c3c",
                    backgroundColor: "rgba(231, 76, 60, 0.1)",
                    tension: 0.4,
                    fill: true
                },
                {
                    label: "Calcium (mg)",
                    data: [0, 0, 0, 0, 0, 0, 0],
                    borderColor: "#3498db",
                    backgroundColor: "rgba(52, 152, 219, 0.1)",
                    tension: 0.4,
                    fill: true
                },
                {
                    label: "Protein (g)",
                    data: [0, 0, 0, 0, 0, 0, 0],
                    borderColor: "#2ecc71",
                    backgroundColor: "rgba(46, 204, 113, 0.1)",
                    tension: 0.4,
                    fill: true
                }
            ]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: "top"
                },
                title: {
                    display: true,
                    text: "7-Day Nutrition Progress"
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: "Nutrient Amount"
                    }
                }
            }
        }
    });
}

function updateNutritionChart() {
    if (nutritionChart && nutritionData) {
        const ironGoal = nutritionData.required.iron;
        const calciumGoal = nutritionData.required.calcium;
        const proteinGoal = nutritionData.required.protein;
        
        const ironStart = nutritionData.current.iron;
        const calciumStart = nutritionData.current.calcium;
        const proteinStart = nutritionData.current.protein;
        
        const ironData = [];
        const calciumData = [];
        const proteinData = [];
        
        for (let day = 0; day < 7; day++) {
            const progress = day / 6;
            ironData.push(Math.round(ironStart + (ironGoal - ironStart) * progress));
            calciumData.push(Math.round(calciumStart + (calciumGoal - calciumStart) * progress));
            proteinData.push(Math.round(proteinStart + (proteinGoal - proteinStart) * progress));
        }
        
        nutritionChart.data.datasets[0].data = ironData;
        nutritionChart.data.datasets[1].data = calciumData;
        nutritionChart.data.datasets[2].data = proteinData;
        
        nutritionChart.update();
    }
}

// Update Chart from Food Intake
function updateChartFromFoodIntake() {
    const spinach = Number(document.getElementById("spinach").value) || 0;
    const ragi = Number(document.getElementById("ragi").value) || 0;
    const milk = Number(document.getElementById("milk").value) || 0;
    const curd = Number(document.getElementById("curd").value) || 0;
    const dal = Number(document.getElementById("dal").value) || 0;
    const rice = Number(document.getElementById("rice").value) || 0;
    const rajma = Number(document.getElementById("rajma").value) || 0;
    const potato = Number(document.getElementById("potato").value) || 0;
    const tomato = Number(document.getElementById("tomato").value) || 0;
    const carrot = Number(document.getElementById("carrot").value) || 0;
    const banana = Number(document.getElementById("banana").value) || 0;
    const peas = Number(document.getElementById("peas").value) || 0;
    const egg = Number(document.getElementById("egg").value) || 0;
    const chicken = Number(document.getElementById("chicken").value) || 0;
    const fish = Number(document.getElementById("fish").value) || 0;

    if (spinach === 0 && ragi === 0 && milk === 0 && curd === 0 && dal === 0 && 
        rice === 0 && rajma === 0 && potato === 0 && tomato === 0 && carrot === 0 &&
        banana === 0 && peas === 0 && egg === 0 && chicken === 0 && fish === 0) {
        alert("Please enter your food intake first!");
        return;
    }

    // Iron calculation (mg)
    const currentIron = (spinach * 2.7) + (ragi * 3.9) + (rajma * 2) + (egg * 1.2) + (peas * 1.5);
    
    // Calcium calculation (mg)
    const currentCalcium = (milk * 300) + (curd * 150) + (spinach * 100);
    
    // Protein calculation (g)
    const currentProtein = (dal * 9) + (rajma * 8) + (peas * 5) + (egg * 6) + (chicken * 13.5) + (fish * 11);
    
    // Vitamin C calculation (mg)
    const currentVitaminC = (potato * 20) + (tomato * 15) + (banana * 10);
    
    // Fiber calculation (g)
    const currentFiber = (dal * 8) + (rajma * 7) + (peas * 4) + (rice * 0.6) + (banana * 3);

    const ironGoal = 27;
    const calciumGoal = 1200;
    const proteinGoal = 80;

    const ironData = [];
    const calciumData = [];
    const proteinData = [];

    for (let day = 0; day < 7; day++) {
        const progress = day / 6;
        ironData.push(Math.round(currentIron + (ironGoal - currentIron) * progress));
        calciumData.push(Math.round(currentCalcium + (calciumGoal - currentCalcium) * progress));
        proteinData.push(Math.round(currentProtein + (proteinGoal - currentProtein) * progress));
    }

    nutritionChart.data.datasets[0].data = ironData;
    nutritionChart.data.datasets[1].data = calciumData;
    nutritionChart.data.datasets[2].data = proteinData;
    nutritionChart.update();

    alert(`Nutrition calculated!\n\nYour current intake:\nIron: ${currentIron.toFixed(1)} mg (Goal: 27 mg)\nCalcium: ${currentCalcium} mg (Goal: 1200 mg)\nProtein: ${currentProtein.toFixed(1)} g (Goal: 80 g)\nVitamin C: ${currentVitaminC.toFixed(1)} mg (Goal: 85 mg)\nFiber: ${currentFiber.toFixed(1)} g (Goal: 28 g)`);
}

// Weekly Chart View
function showWeeklyChart() {
    if (currentDuration === "month") {
        nutritionChart.data.labels = ["Week 1", "Week 2", "Week 3", "Week 4"];
        nutritionChart.data.datasets[0].data = [15, 20, 24, 27];
        nutritionChart.data.datasets[1].data = [800, 950, 1100, 1200];
        nutritionChart.data.datasets[2].data = [55, 65, 72, 80];
        nutritionChart.options.plugins.title.text = "Monthly Nutrition Progress (Weekly View)";
        nutritionChart.update();
    }
}

// Daily Chart View
function showDailyChart() {
    if (currentDuration === "month") {
        selectWeek(currentWeek);
    } else {
        updateNutritionChart();
    }
}

// Select Week for 30-day plan
function selectWeek(week) {
    currentWeek = week;
    const startDay = (week - 1) * 7 + 1;
    const labels = [];
    for (let i = 0; i < 7; i++) {
        labels.push(`Day ${startDay + i}`);
    }
    
    nutritionChart.data.labels = labels;
    
    // Simulate weekly progression
    const baseIron = 15 + (week - 1) * 3;
    const baseCalcium = 800 + (week - 1) * 100;
    const baseProtein = 55 + (week - 1) * 6;
    
    const ironData = [];
    const calciumData = [];
    const proteinData = [];
    
    for (let i = 0; i < 7; i++) {
        ironData.push(baseIron + i);
        calciumData.push(baseCalcium + i * 15);
        proteinData.push(baseProtein + i * 1);
    }
    
    nutritionChart.data.datasets[0].data = ironData;
    nutritionChart.data.datasets[1].data = calciumData;
    nutritionChart.data.datasets[2].data = proteinData;
    nutritionChart.options.plugins.title.text = `Week ${week} - Daily Nutrition Progress`;
    nutritionChart.update();
}

// Download Chart
function downloadChart() {
    const link = document.createElement('a');
    link.download = `nutrition-chart-${new Date().toISOString().split('T')[0]}.png`;
    link.href = nutritionChart.toBase64Image();
    link.click();
    alert("Chart downloaded successfully!");
}

// =====================================================
// Time-Based Meal Tracker Functions
// =====================================================

let savedMeals = {
    breakfast: { image: null, text: '', saved: false },
    lunch: { image: null, text: '', saved: false },
    dinner: { image: null, text: '', saved: false }
};

function updateMealTimeDisplay() {
    const now = new Date();
    const hours = now.getHours();
    const minutes = now.getMinutes();
    const timeString = now.toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit', hour12: true });
    
    document.getElementById('currentTime').textContent = timeString;
    
    // Hide all sections first
    document.getElementById('breakfastSection').style.display = 'none';
    document.getElementById('lunchSection').style.display = 'none';
    document.getElementById('dinnerSection').style.display = 'none';
    document.getElementById('outsideMealTime').style.display = 'none';
    
    // Breakfast: 8:00 AM - 11:00 AM (8-11)
    if (hours >= 8 && hours < 11) {
        document.getElementById('breakfastSection').style.display = 'block';
        document.getElementById('activeMeal').textContent = '🌅 Breakfast Time';
    }
    // Lunch: 12:00 PM - 3:00 PM (12-15)
    else if (hours >= 12 && hours < 15) {
        document.getElementById('lunchSection').style.display = 'block';
        document.getElementById('activeMeal').textContent = '☀️ Lunch Time';
    }
    // Dinner: 7:30 PM - 10:00 PM (19:30-22:00)
    else if ((hours === 19 && minutes >= 30) || (hours >= 20 && hours < 22)) {
        document.getElementById('dinnerSection').style.display = 'block';
        document.getElementById('activeMeal').textContent = '🌙 Dinner Time';
    }
    // Outside meal times
    else {
        document.getElementById('outsideMealTime').style.display = 'block';
        document.getElementById('activeMeal').textContent = 'No Active Meal Time';
    }
}

function showAllMeals() {
    // Show all meal sections for manual tracking
    document.getElementById('breakfastSection').style.display = 'block';
    document.getElementById('lunchSection').style.display = 'block';
    document.getElementById('dinnerSection').style.display = 'block';
    document.getElementById('outsideMealTime').style.display = 'none';
    document.getElementById('activeMeal').textContent = 'Manual Tracking Mode';
}

function saveMeal(mealType) {
    const imageInput = document.getElementById(`${mealType}-image`);
    const textInput = document.getElementById(`${mealType}-text`);
    
    if (!imageInput.files[0] && !textInput.value.trim()) {
        alert('Please upload a photo or type what you ate!');
        return;
    }
    
    // Save meal data
    savedMeals[mealType] = {
        image: imageInput.files[0] || null,
        text: textInput.value.trim(),
        saved: true,
        time: new Date().toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit', hour12: true })
    };
    
    // Store in localStorage (text only, images stored in memory)
    const storageData = {
        text: textInput.value.trim(),
        time: savedMeals[mealType].time,
        saved: true
    };
    localStorage.setItem(`meal_${mealType}`, JSON.stringify(storageData));
    
    alert(`✅ ${mealType.charAt(0).toUpperCase() + mealType.slice(1)} saved successfully!`);
    updateSavedMealsSummary();
}

function loadSavedMeals() {
    // Load saved meals from localStorage
    ['breakfast', 'lunch', 'dinner'].forEach(meal => {
        const saved = localStorage.getItem(`meal_${meal}`);
        if (saved) {
            const data = JSON.parse(saved);
            savedMeals[meal] = {
                image: null,
                text: data.text,
                saved: data.saved,
                time: data.time
            };
            // Restore text in input
            document.getElementById(`${meal}-text`).value = data.text;
        }
    });
    updateSavedMealsSummary();
}

function updateSavedMealsSummary() {
    const summary = document.getElementById('savedMealsSummary');
    const list = document.getElementById('savedMealsList');
    
    const savedCount = Object.values(savedMeals).filter(m => m.saved).length;
    
    if (savedCount === 0) {
        summary.style.display = 'none';
        return;
    }
    
    summary.style.display = 'block';
    
    let html = '<div style="display: grid; gap: 10px; margin-top: 10px;">';
    
    ['breakfast', 'lunch', 'dinner'].forEach(meal => {
        if (savedMeals[meal].saved) {
            const icon = meal === 'breakfast' ? '🌅' : meal === 'lunch' ? '☀️' : '🌙';
            html += `
                <div style="background: white; padding: 15px; border-radius: 8px; border-left: 4px solid #667eea;">
                    <strong>${icon} ${meal.charAt(0).toUpperCase() + meal.slice(1)}</strong>
                    <span style="float: right; color: #888; font-size: 12px;">${savedMeals[meal].time}</span>
                    <p style="margin: 5px 0 0 0; color: #666; font-size: 14px;">${savedMeals[meal].text || 'Photo uploaded'}</p>
                </div>
            `;
        }
    });
    
    html += '</div>';
    list.innerHTML = html;
}

function clearSavedMeals() {
    savedMeals = {
        breakfast: { image: null, text: '', saved: false },
        lunch: { image: null, text: '', saved: false },
        dinner: { image: null, text: '', saved: false }
    };
    localStorage.removeItem('meal_breakfast');
    localStorage.removeItem('meal_lunch');
    localStorage.removeItem('meal_dinner');
    updateSavedMealsSummary();
}

// =====================================================
// Food Tracker Functions (Updated)
// =====================================================

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
    const btn = document.getElementById('analyzeFoodBtn');
    btn.disabled = true;
    btn.textContent = '🔄 Analyzing...';

    const formData = new FormData();
    
    // Collect data from saved meals or current inputs
    ['breakfast', 'lunch', 'dinner'].forEach(meal => {
        const imageInput = document.getElementById(`${meal}-image`);
        const textInput = document.getElementById(`${meal}-text`);
        
        // Use saved meal data if available
        if (savedMeals[meal].saved) {
            if (savedMeals[meal].image) {
                formData.append(`${meal}_image`, savedMeals[meal].image);
            }
            formData.append(`${meal}_text`, savedMeals[meal].text);
        } else {
            // Use current input
            if (imageInput.files[0]) {
                formData.append(`${meal}_image`, imageInput.files[0]);
            }
            formData.append(`${meal}_text`, textInput.value);
        }
    });

    try {
        const response = await fetch(`${API_BASE_URL}/analyze-food-intake`, {
            method: 'POST',
            body: formData
        });

        const data = await response.json();
        displayFoodTrackerResults(data);
        
        // Generate diet plan based on nutrition deficiencies
        await generateDietPlanFromFoodIntake(data.nutrition_summary);
        
        document.getElementById('foodTrackerResults').style.display = 'block';
        document.getElementById('foodTrackerResults').scrollIntoView({ behavior: 'smooth' });
        
        // Clear saved meals after analysis
        clearSavedMeals();
        
    } catch (error) {
        alert('Error analyzing food intake. Please make sure the backend server is running.');
        console.error(error);
    } finally {
        btn.disabled = false;
        btn.textContent = '🔍 Analyze My Food Intake';
    }
}

// Generate Diet Plan from Food Intake Analysis
async function generateDietPlanFromFoodIntake(nutritionSummary) {
    // Show loading state
    document.getElementById("dietPlan").innerHTML = '<p class="placeholder-text">🔄 Generating your personalized diet plan based on your food intake...</p>';
    
    // Determine risk level based on nutrition deficiencies
    let risk = 'Medium';
    
    const caloriesPercent = (nutritionSummary.calories / 2200) * 100;
    const proteinPercent = (nutritionSummary.protein / 80) * 100;
    const ironPercent = (nutritionSummary.iron / 27) * 100;
    const calciumPercent = (nutritionSummary.calcium / 1200) * 100;
    
    const avgPercent = (caloriesPercent + proteinPercent + ironPercent + calciumPercent) / 4;
    
    if (avgPercent < 60) {
        risk = 'High';
    } else if (avgPercent < 80) {
        risk = 'Medium';
    } else {
        risk = 'Low';
    }
    
    const duration = document.getElementById("duration").value;
    const foodPreference = document.getElementById("foodPreference").value;

    try {
        const response = await fetch(`${API_BASE_URL}/diet-plan`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ risk, duration, food_preference: foodPreference })
        });

        if (!response.ok) throw new Error("Diet plan generation failed");

        const data = await response.json();
        displayDietPlan(data.diet_plan, duration);
        
        // Scroll to diet plan after a short delay
        setTimeout(() => {
            document.getElementById("dietPlan").parentElement.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }, 500);

    } catch (err) {
        console.error("Error:", err);
        document.getElementById("dietPlan").innerHTML = "<p class='placeholder-text'>❌ Failed to generate diet plan. Please check if the backend server is running.</p>";
    }
}

function displayFoodTrackerResults(data) {
    displayDetectedFoods(data.detected_foods);
    displayNutritionSummaryFromFood(data.nutrition_summary);
    displayFoodRecommendations(data.recommendations);
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

function displayNutritionSummaryFromFood(summary) {
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

function displayFoodRecommendations(recommendations) {
    const container = document.getElementById('foodRecommendations');
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
