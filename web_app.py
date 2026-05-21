import streamlit as st
import numpy as np
import joblib

# Load model
model = joblib.load("model.pkl")
scaler = joblib.load("scaler.pkl")

st.title("🏥 Breast Cancer AI Web App")

values = []

for i in range(5):
    values.append(
        st.number_input(f"Feature {i+1}")
    )

if st.button("Predict"):

    arr = np.zeros(30)

    arr[:5] = values

    arr = scaler.transform([arr])

    result = model.predict(arr)

    if result[0] == 0:
        st.error("❌ Cancer Detected")
    else:
        st.success("✅ No Cancer")