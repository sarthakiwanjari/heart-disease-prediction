const form = document.getElementById("predictionForm");
const resultBox = document.getElementById("result");

form.addEventListener("submit", async function (event) {

    event.preventDefault();

    // Show loading state
    resultBox.className = "result";
    resultBox.innerHTML = `
        <div class="result-loading">
            <div class="loading-heart">♥</div>
            <h3>Analyzing Your Health Data...</h3>
            <p>Please wait while the model processes the 13 health parameters.</p>
        </div>
    `;

    // Collect form data
    const data = {
        age: document.getElementById("age").value,
        sex: document.getElementById("sex").value,
        cp: document.getElementById("cp").value,
        trestbps: document.getElementById("trestbps").value,
        chol: document.getElementById("chol").value,
        fbs: document.getElementById("fbs").value,
        restecg: document.getElementById("restecg").value,
        thalach: document.getElementById("thalach").value,
        exang: document.getElementById("exang").value,
        oldpeak: document.getElementById("oldpeak").value,
        slope: document.getElementById("slope").value,
        ca: document.getElementById("ca").value,
        thal: document.getElementById("thal").value
    };

    try {

        const response = await fetch("/api/predict", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(data)
        });

        const result = await response.json();

        console.log("Prediction response:", result);

        if (!response.ok) {
            throw new Error(result.error || "Prediction failed");
        }

        const isDetected = Number(result.prediction) === 1;

        resultBox.className =
            "result " + (isDetected ? "risk-result" : "safe-result");

        resultBox.innerHTML = `

            <div class="result-icon">
                ${isDetected ? "!" : "✓"}
            </div>

            <div class="result-percentage">
                ${result.confidence}%
            </div>

            <div class="confidence-text">
                PREDICTION CONFIDENCE
            </div>

            <div class="result-title">
                ${
                    isDetected
                    ? "Heart Disease Risk Detected"
                    : "No Heart Disease Risk Detected"
                }
            </div>

            <div class="result-subtitle">
                ${
                    isDetected
                    ? "The submitted health parameters indicate a potential cardiovascular risk."
                    : "The submitted health parameters do not indicate a predicted cardiovascular risk."
                }
            </div>

            <div class="result-line"></div>

            <div class="care-message">

                <strong>
                    ${
                        isDetected
                        ? "⚠ Please Take Care of Your Heart"
                        : "♥ Keep Taking Care of Your Heart"
                    }
                </strong>

                <p>
                    ${
                        isDetected
                        ? "Consider discussing these results with a qualified healthcare professional for appropriate evaluation. This prediction is for educational purposes and is not a medical diagnosis."
                        : "Continue maintaining healthy habits including regular physical activity, balanced nutrition, adequate sleep, and routine health check-ups."
                    }
                </p>

            </div>

            <div class="medical-note">
                ⚕ Model prediction only • Not a medical diagnosis
            </div>
        `;

    } catch (error) {

        console.error("Prediction error:", error);

        resultBox.className = "result error-result";

        resultBox.innerHTML = `
            <div class="result-icon">×</div>

            <div class="result-title">
                Prediction Failed
            </div>

            <div class="result-subtitle">
                ${error.message}
            </div>

            <p class="error-help">
                Please make sure the Flask server is running
                and try again.
            </p>
        `;
    }

});