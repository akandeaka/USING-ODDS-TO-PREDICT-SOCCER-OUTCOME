import os
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
import joblib

LOG_FILE = "performance_log.csv"
MODEL_PATH = "engine/ml_model.pkl"

if not os.path.exists(LOG_FILE):
    raise FileNotFoundError("performance_log.csv not found. Generate some predictions first.")

df = pd.read_csv(LOG_FILE)
df = df[df["status"].isin(["Correct", "Wrong"])]

if df.empty:
    raise ValueError("No completed results to train on yet.")

df["target"] = (df["status"] == "Correct").astype(int)
df["signals"] = df["signals"].astype(str)

X = df[["league", "signals", "ml_confidence"]]
y = df["target"]

preprocess = ColumnTransformer(
    [("cat", OneHotEncoder(handle_unknown="ignore"), ["league", "signals"])],
    remainder="passthrough",
)

model = Pipeline(
    [
        ("prep", preprocess),
        ("clf", RandomForestClassifier(n_estimators=200, random_state=42)),
    ]
)

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)
model.fit(X_train, y_train)

print("Test accuracy:", model.score(X_test, y_test))
os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
joblib.dump(model, MODEL_PATH)
print("Saved model to", MODEL_PATH)
