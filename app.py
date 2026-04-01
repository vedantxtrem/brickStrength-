import streamlit as st
import pandas as pd
import joblib

# ------------------ CONFIG ------------------
st.set_page_config(
    page_title="Brick Strength Predictor",
    page_icon="🧱",
    layout="centered"
)

# ------------------ LOAD MODEL ------------------
model = joblib.load("./model/brick_strength_model.pkl")

# ------------------ CUSTOM CSS ------------------
st.markdown("""
<style>
    .main {
        background-color: #f5f7fa;
    }
    .stButton>button {
        width: 100%;
        height: 50px;
        font-size: 18px;
        border-radius: 10px;
        background-color: #4CAF50;
        color: white;
    }
    .stButton>button:hover {
        background-color: #45a049;
    }
    .result-box {
        padding: 20px;
        border-radius: 10px;
        background-color: #ffffff;
        text-align: center;
        box-shadow: 0px 0px 10px rgba(0,0,0,0.1);
        color: #808080;
    }
</style>
""", unsafe_allow_html=True)

# ------------------ TITLE ------------------
st.title("🧱 Brick Strength Prediction System")
st.markdown("### 📊 AI-Based Smart Construction Tool")

# ------------------ FIXED SOIL ------------------
soil = 60
st.info(f"🟤 Soil Content is fixed at **{soil}%**")

st.markdown("---")

# ------------------ INPUT SECTION ------------------
st.markdown("### 🧪 Enter Material Composition (%)")

col1, col2 = st.columns(2)

with col1:
    fly_ash = st.text_input("Fly Ash (%)", "10")
    coal_ash = st.text_input("Coal Ash (%)", "10")

with col2:
    cow_dunk_ash = st.text_input("Cow Dunk Ash (%)", "10")
    water_absorption = st.text_input("Water Absorption (%)", "5")

# ------------------ VALIDATION ------------------
try:
    fly_ash = float(fly_ash)
    coal_ash = float(coal_ash)
    cow_dunk_ash = float(cow_dunk_ash)
    water_absorption = float(water_absorption)
except:
    st.error("⚠️ Please enter valid numeric values")
    st.stop()

# Negative check
if any(v < 0 for v in [fly_ash, coal_ash, cow_dunk_ash, water_absorption]):
    st.error("⚠️ Values cannot be negative")
    st.stop()

st.markdown("---")

# ------------------ MIX CALCULATION ------------------
total_mix = soil + fly_ash + coal_ash + cow_dunk_ash
remaining = 100 - total_mix

col1, col2 = st.columns(2)

with col1:
    st.metric("🔢 Total Mix (%)", f"{total_mix:.2f}%")

with col2:
    st.metric("📉 Remaining (%)", f"{remaining:.2f}%")

# Validation
if total_mix > 100:
    st.error("⚠️ Total mix should not exceed 100%")

st.markdown("---")

# ------------------ PREDICTION ------------------
if st.button("🔍 Predict Strength"):

    if total_mix > 100:
        st.stop()

    # ✅ FIX: Use DataFrame (no sklearn warning)
    input_data = pd.DataFrame([{
        'Soil': soil,
        'Fly Ash': fly_ash,
        'Coal Ash': coal_ash,
        'Cow Dunk Ash': cow_dunk_ash,
        'Water Absorption (%)': water_absorption
    }])

    prediction = model.predict(input_data)

    st.markdown("## 📊 Prediction Result")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown(f"""
        <div class="result-box">
            <h3>3-Day Strength</h3>
            <h2>{prediction[0][0]:.2f} MPa</h2>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="result-box">
            <h3>7-Day Strength</h3>
            <h2>{prediction[0][1]:.2f} MPa</h2>
        </div>
        """, unsafe_allow_html=True)

st.markdown("---")

# ------------------ FOOTER ------------------
st.caption("🚀 Developed using Machine Learning (Random Forest) & Streamlit")