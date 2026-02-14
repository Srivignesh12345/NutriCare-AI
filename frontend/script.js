// ===============================
// CONFIG (AUTO SWITCH LOCAL / PROD)
// ===============================
const API_BASE_URL =
    window.location.hostname === "localhost"
        ? "http://127.0.0.1:5000"
        : "https://nutricare-api.onrender.com";

// Ensure JS is loaded
console.log("script.js loaded");

// Attach event after page loads
document.addEventListener("DOMContentLoaded", () => {
    const btn = document.getElementById("analyzeBtn");
    btn.addEventListener("click", analyze);
});

// ===============================
// ANALYZE FUNCTION
// ===============================
async function analyze() {
    console.log("Analyze button clicked");

    const data = {
        age: Number(document.getElementById("age").value),
        systolicbp: Number(document.getElementById("systolicbp").value),
        diastolicbp: Number(document.getElementById("diastolicbp").value),
        bs: Number(document.getElementById("bs").value),
        bodytemp: Number(document.getElementById("bodytemp").value),
        heartrate: Number(document.getElementById("heartrate").value)
    };

    const duration = document.getElementById("duration").value;

    // Validation
    for (let key in data) {
        if (isNaN(data[key])) {
            alert("Please fill all fields correctly");
            return;
        }
    }

    const resultDiv = document.getElementById("result");
    resultDiv.innerHTML = "⏳ Analyzing...";

    try {
        console.log("Calling API:", `${API_BASE_URL}/analyze`, data);

        const response = await fetch(`${API_BASE_URL}/analyze`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(data)
        });

        if (!response.ok) {
            const errorText = await response.text();
            throw new Error(`Server error ${response.status}: ${errorText}`);
        }

        const result = await response.json();

        resultDiv.innerHTML = `
            <h3>🩺 Risk Level: <span class="risk">${result.risk}</span></h3>
            <p>${result.message}</p>
            <button id="dietBtn">
                Get ${duration === "week" ? "Weekly" : "Monthly"} Diet Plan
            </button>
        `;

        document
            .getElementById("dietBtn")
            .addEventListener("click", () =>
                getDiet(result.risk, duration)
            );

    } catch (err) {
        console.error("Analyze error:", err);
        resultDiv.innerHTML =
            "❌ Backend not reachable. Please try again later.";
    }
}

// ===============================
// DIET PLAN FUNCTION
// ===============================
async function getDiet(risk, duration) {
    const resultDiv = document.getElementById("result");
    resultDiv.innerHTML += "<p>🍽️ Loading diet plan...</p>";

    try {
        console.log("Fetching diet plan:", risk, duration);

        const response = await fetch(`${API_BASE_URL}/diet-plan`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ risk, duration })
        });

        if (!response.ok) {
            const errorText = await response.text();
            throw new Error(`Server error ${response.status}: ${errorText}`);
        }

        const data = await response.json();

        // Sort days correctly (Day 1 → Day N)
        const sortedDays = Object.keys(data.diet_plan).sort((a, b) => {
            const numA = parseInt(a.replace(/\D/g, ""));
            const numB = parseInt(b.replace(/\D/g, ""));
            return numA - numB;
        });

        let html = `<h3>📅 ${duration.toUpperCase()} DIET PLAN</h3>`;

        sortedDays.forEach(day => {
            const meal = data.diet_plan[day];

            html += `
                <div class="diet-card">
                    <h4>${day}</h4>
                    <p><b>Breakfast:</b> ${meal.Breakfast}</p>
                    <p><b>Lunch:</b> ${meal.Lunch}</p>
                    <p><b>Dinner:</b> ${meal.Dinner}</p>
                    <p><i>${meal.Note}</i></p>
                </div>
            `;
        });

        resultDiv.innerHTML += html;

    } catch (err) {
        console.error("Diet plan error:", err);
        alert("❌ Failed to load diet plan");
    }
}
