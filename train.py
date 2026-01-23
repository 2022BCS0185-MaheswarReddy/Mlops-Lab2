import os
import json
import joblib
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score

# -------------------------
# Load dataset
# -------------------------
df = pd.read_csv("dataset/winequality-red.csv", sep=";")

#  Use ALL 11 features (except target)
X = df.drop("quality", axis=1)
y = df["quality"]

# -------------------------
# Train-test split
# -------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# -------------------------
# Model
# -------------------------
model = RandomForestRegressor(
    n_estimators=100,
    max_depth=15,
    random_state=42
)
model.fit(X_train, y_train)

# -------------------------
# Evaluation
# -------------------------
preds = model.predict(X_test)
mse = mean_squared_error(y_test, preds)
r2 = r2_score(y_test, preds)

print(f"MSE: {mse}")
print(f"R2 Score: {r2}")

# -------------------------
# Save artifacts
# -------------------------
os.makedirs("artifacts", exist_ok=True)

joblib.dump(model, "artifacts/model.pkl")

metrics = {
    "mse": mse,
    "r2": r2
}
with open("artifacts/metrics.json", "w") as f:
    json.dump(metrics, f, indent=4)

print("Saved model to artifacts/model.pkl")
print("Saved metrics to artifacts/metrics.json")
