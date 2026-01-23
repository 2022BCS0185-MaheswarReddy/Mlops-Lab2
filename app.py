import os
import joblib
import numpy as np
from fastapi import FastAPI
from fastapi.responses import RedirectResponse

app = FastAPI()

# -----------------------------
# Model path (portable)
# -----------------------------
model_path = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "artifacts", "model.pkl")
)

# -----------------------------
# Load model ONCE
# -----------------------------
model = joblib.load(model_path)

# -----------------------------
# Redirect root to Swagger
# -----------------------------
@app.get("/", include_in_schema=False)
def read_root():
    return RedirectResponse(url="/docs")

# -----------------------------
# Prediction endpoint
# -----------------------------
@app.get("/predict")
def predict(
    fixed_acidity: float,
    volatile_acidity: float,
    citric_acid: float,
    alcohol: float
):
    #  Must match train.py features order
    features = np.array([[fixed_acidity, volatile_acidity, citric_acid, alcohol]])

    prediction = model.predict(features)[0]

    return {
        "name": "Panduga Maheswar Reddy",
        "roll_no": "2022BCS0185",
        "prediction": float(prediction)
    }
