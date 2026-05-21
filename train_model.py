import numpy as np
import joblib
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

# ================= LOAD DATA =================
data = load_breast_cancer()

# TAKE ONLY 8 FEATURES (IMPORTANT FIX)
X = data.data[:, :8]
y = data.target

# ================= SPLIT =================
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# ================= SCALING =================
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# ================= MODEL =================
model = LogisticRegression(max_iter=5000)
model.fit(X_train, y_train)

# ================= PREDICTION =================
y_pred = model.predict(X_test)

acc = accuracy_score(y_test, y_pred)
print("Accuracy:", acc)

# ================= SAVE MODEL =================
joblib.dump(model, "model.pkl")
joblib.dump(scaler, "scaler.pkl")

print("Model saved successfully!")