import csv
import json
from pathlib import Path

import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

DATA = Path("data/synthetic_sellers.csv")
MODEL_DIR = Path("model")
MODEL_DIR.mkdir(exist_ok=True)

FEATURES = [
    "account_age_days",
    "followers",
    "following",
    "posts",
    "engagement_ratio",
    "has_contact_info",
    "match_count",
    "unique_domains",
    "listed_price",
    "market_median",
]

X_rows, y_rows = [], []

with DATA.open(newline="") as f:
    for row in csv.DictReader(f):
        X_rows.append([float(row[k]) for k in FEATURES])
        y_rows.append(int(row["label"]))

X = np.asarray(X_rows, dtype=float)
y = np.asarray(y_rows, dtype=int)

if len(set(y)) != 2:
    raise SystemExit("Training data must contain both label classes.")

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=42, stratify=y
)

model = make_pipeline(
    StandardScaler(),
    LogisticRegression(max_iter=1000, class_weight="balanced")
)
model.fit(X_train, y_train)

pred = model.predict(X_test)

print("DATASET: Synthetic; labels are rule-generated.")
print(f"Training records: {len(X_train)}")
print(f"Test records: {len(X_test)}")
print(f"Accuracy:  {accuracy_score(y_test, pred):.3f}")
print(f"Precision: {precision_score(y_test, pred, zero_division=0):.3f}")
print(f"Recall:    {recall_score(y_test, pred, zero_division=0):.3f}")

# Save the fitted model and its feature schema.
import joblib

joblib.dump(
    {"model": model, "features": FEATURES},
    MODEL_DIR / "synthetic_logistic_model.joblib"
)

print("Saved: model/synthetic_logistic_model.joblib")
print("WARNING: Metrics do not measure real-world scam-detection performance.")
