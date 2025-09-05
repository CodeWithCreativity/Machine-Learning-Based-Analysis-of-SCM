import streamlit as st
import pandas as pd
import joblib

st.set_page_config(page_title="SCM Strength Estimator", layout="centered")
st.title("SCM-Based NFC Strength Estimator")

with st.expander("📘 Note", expanded=True):
    st.markdown("""
    **Recommended SCM quantity limits based on research findings:**
    
    1. Fly ash – up to **10 kg/m³**  
    2. Metakaolin – up to **60 kg/m³**  
    3. Silica fume – up to **40 kg/m³**  
    4. Rice husk ash – up to **40 kg/m³**  
    
    ⚠️ Exceeding these limits may negatively impact compressive strength.
    """)

cement_content = st.number_input("Enter Cement content (in kg/m³):", min_value=300.0, value=410.0, step=10.0)

scm_selected = st.selectbox(
    "Select kind of SCM:",
    ["Fly ash", "Metakaolin", "Silica Fume", "Rice Husk Ash"]
)

scm_limits = {
    "Fly ash": 10.0,
    "Metakaolin": 60.0,
    "Silica Fume": 40.0,
    "Rice Husk Ash": 40.0
}

scm_value = st.number_input(
    "Select quantity of SCM (in kg/m³):",
    min_value=0.0,
    value=10.0,
    step=1.0
)

curing_age = st.number_input("Specify curing age (in days):", min_value=1, value=7, step=1)

@st.cache_resource
def load_model():
    return joblib.load("final_model.pkl") 

model = load_model()

input_features = {
    "Cement": cement_content,
    "Fly ash": scm_value if scm_selected == "Fly ash" else 0.0,
    "Metakaolin": scm_value if scm_selected == "Metakaolin" else 0.0,
    "Silica Fume": scm_value if scm_selected == "Silica Fume" else 0.0,
    "Rice Husk Ash": scm_value if scm_selected == "Rice Husk Ash" else 0.0,
    "Curing age": curing_age
}

if st.button("Predict Strength"):
    pred = model.predict(pd.DataFrame([input_features]))[0]
    st.success(f"✅ Predicted Compressive Strength: {pred:.2f} MPa")

    if scm_value > scm_limits[scm_selected]:
        st.error(f"⚠️ Warning: {scm_selected} exceeds recommended limit ({scm_limits[scm_selected]} kg/m³).")
