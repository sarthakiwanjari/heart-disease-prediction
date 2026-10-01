from flask import Flask, render_template, request, jsonify
import pickle
import numpy as np
import os

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

MODEL_PATH = os.path.join(
    BASE_DIR,
    "model",
    "heart_disease_model.pkl"
)

SCALER_PATH = os.path.join(
    BASE_DIR,
    "model",
    "scaler.pkl"
)

# Load trained model
with open(MODEL_PATH, "rb") as file:
    model = pickle.load(file)

# Load scaler
with open(SCALER_PATH, "rb") as file:
    scaler = pickle.load(file)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/api/predict", methods=["POST"])
def predict():

    try:
        data = request.get_json()

        features = [
            float(data["age"]),
            float(data["sex"]),
            float(data["cp"]),
            float(data["trestbps"]),
            float(data["chol"]),
            float(data["fbs"]),
            float(data["restecg"]),
            float(data["thalach"]),
            float(data["exang"]),
            float(data["oldpeak"]),
            float(data["slope"]),
            float(data["ca"]),
            float(data["thal"])
        ]

        input_data = np.array([features])

        # Scale input
        input_scaled = scaler.transform(input_data)

        # Prediction
        prediction = model.predict(input_scaled)[0]

        # Probability
        probability = model.predict_proba(input_scaled)[0]

        if prediction == 1:
            result = "Heart disease detected"
        else:
            result = "No heart disease detected"

        return jsonify({
            "prediction": int(prediction),
            "result": result,
            "confidence": round(float(max(probability)) * 100, 2)
        })

    except Exception as e:

        return jsonify({
            "error": str(e)
        }), 500


if __name__ == "__main__":
    app.run(debug=True)