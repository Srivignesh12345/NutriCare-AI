// Ensure JS is loaded
console.log("script.js loaded");

// Attach event after page loads
document.addEventListener("DOMContentLoaded", () => {
    const btn = document.getElementById("analyzeBtn");

    btn.addEventListener("click", analyze);
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
        // Call Analyze API
        const response = await fetch("http://127.0.0.1:5000/analyze", {
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
            "❌ Backend not reachable. Is Flask running?";
    }
}

async function getDiet(risk, duration) {
    document.getElementById("result").innerHTML += "<p>🍽️ Loading diet plan...</p>";

    try {
        const response = await fetch("http://127.0.0.1:5000/diet-plan", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ risk, duration })
        });

        const data = await response.json();

        // 🔹 Sort days numerically (Day 1, Day 2, ..., Day 30)
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

        document.getElementById("result").innerHTML += html;

    } catch (err) {
        console.error(err);
        alert("Failed to load diet plan");
    }
}
