import pickle
import os
import numpy as np


BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)


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


with open(MODEL_PATH, "rb") as file:
    model = pickle.load(file)


with open(SCALER_PATH, "rb") as file:
    scaler = pickle.load(file)


def predict_heart_disease(values):

    input_data = np.array([values])

    input_scaled = scaler.transform(input_data)

    prediction = model.predict(input_scaled)[0]

    probability = model.predict_proba(input_scaled)[0]

    if prediction == 1:
        result = "Heart disease detected"
    else:
        result = "No heart disease detected"

    return {
        "prediction": int(prediction),
        "result": result,
        "confidence": round(
            float(max(probability)) * 100,
            2
        )
    }