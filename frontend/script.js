// ===============================
// CONFIG (CHANGE ONLY THIS LATER)
// ===============================
const API_BASE_URL =
    window.location.hostname === "localhost"
        ? "http://127.0.0.1:5000"
        : "https://nutricare-api.onrender.com"; // 🔁 replace after Render deploy

// Ensure JS is loaded
console.log("script.js loaded");

// Attach event after page loads
document.addEventListener("DOMContentLoaded", () => {
    document
        .getElementById("analyzeBtn")
        .addEventListener("click", analyze);
});

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

    document.getElementById("result").innerHTML = "⏳ Analyzing...";

    try {
        const response = await fetch(`${API_BASE_URL}/analyze`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(data)
        });

        const result = await response.json();

        document.getElementById("result").innerHTML = `
            <h3>🩺 Risk Level: <span class="risk">${result.risk}</span></h3>
            <p>${result.message}</p>
            <button onclick="getDiet('${result.risk}', '${duration}')">
                Get ${duration === "week" ? "Weekly" : "Monthly"} Diet Plan
            </button>
        `;
    } catch (err) {
        console.error(err);
        document.getElementById("result").innerHTML =
            "❌ Backend not reachable";
    }
}

async function getDiet(risk, duration) {
    document.getElementById("result").innerHTML += "<p>🍽️ Loading diet plan...</p>";

    try {
        const response = await fetch(`${API_BASE_URL}/diet-plan`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ risk, duration })
        });

        const data = await response.json();

        // Sort Day 1 → Day N correctly
        const sortedDays = Object.keys(data.diet_plan).sort((a, b) => {
            return parseInt(a.replace(/\D/g, "")) -
                   parseInt(b.replace(/\D/g, ""));
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

        document.getElementById("result").innerHTML += html;
    } catch (err) {
        console.error(err);
        alert("Failed to load diet plan");
    }
}
