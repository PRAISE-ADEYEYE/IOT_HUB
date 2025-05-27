# SmartSecure IoT Hub - Full Streamlit App (No OpenCV)
# By Praise Adeyeye (Covenant University) - AI Security + IoT Infrastructure Monitor

# --- REQUIRED LIBRARIES (Install via pip) ---
# pip install streamlit numpy pandas pillow plotly torch torchvision streamlit-lottie ultralytics

import streamlit as st
import numpy as np
import pandas as pd
from PIL import Image, ImageDraw, ImageFont
import plotly.graph_objects as go
import time
import random
from streamlit_lottie import st_lottie
from ultralytics import YOLO
import json
import os

# --- GLOBAL VARIABLES ---
st.set_page_config(page_title="SmartSecure IoT Hub", layout="wide")


# --- HELPER FUNCTIONS ---
def load_lottiefile(filepath: str):
    with open(filepath, "r") as f:
        return json.load(f)


def simulate_sensor_data():
    return {
        "Temperature (C)": np.random.uniform(20, 70),
        "Humidity (%)": np.random.uniform(30, 90),
        "Gas Level (ppm)": np.random.uniform(200, 900),
        "Vibration (m/s^2)": np.random.uniform(0, 5),
        "Smoke Level": np.random.uniform(0, 100)
    }


def create_alerts(data):
    alerts = []
    if data['Temperature (C)'] > 50:
        alerts.append("🔥 High Temperature Detected!")
    if data['Gas Level (ppm)'] > 600:
        alerts.append("🧪 Gas Leak Detected!")
    if data['Vibration (m/s^2)'] > 3:
        alerts.append("⚠️ High Vibration - Structural Risk!")
    if data['Smoke Level'] > 50:
        alerts.append("🚨 Smoke Detected!")
    return alerts


def draw_detection_boxes(image_path, model):
    image = Image.open(image_path).convert("RGB")
    results = model(image_path)
    draw = ImageDraw.Draw(image)
    for r in results:
        for box in r.boxes:
            x1, y1, x2, y2 = box.xyxy[0].tolist()
            cls = int(box.cls[0].item())
            label = model.names[cls]
            draw.rectangle([x1, y1, x2, y2], outline="red", width=3)
            draw.text((x1, y1 - 10), label, fill="red")
    return image


def sensor_dashboard():
    st.subheader("🔧 IoT Sensor Monitoring Dashboard")
    col1, col2 = st.columns(2)
    with col1:
        st_lottie(load_lottiefile("media/lottie/sensors.json"), height=200)
    with col2:
        st.write("Real-time sensor values simulated below:")
        data = simulate_sensor_data()
        df = pd.DataFrame([data])
        st.dataframe(df.round(2))

    fig = go.Figure()
    for key, val in data.items():
        fig.add_trace(go.Indicator(
            mode="gauge+number",
            value=val,
            title={'text': key},
            gauge={'axis': {'range': [0, 100]}}
        ))
    fig.update_layout(height=400)
    st.plotly_chart(fig, use_container_width=True)

    alerts = create_alerts(data)
    if alerts:
        st.error("\n".join(alerts))
    else:
        st.success("✅ All systems operating within safe parameters.")


def ai_vision_security(model):
    st.subheader("🧠 AI Security Camera System")
    st_lottie(load_lottiefile("media/lottie/security.json"), height=200)
    uploaded_file = st.file_uploader("Upload Image for AI Vision Scan", type=["jpg", "jpeg", "png"])
    if uploaded_file:
        st.image(uploaded_file, caption="Uploaded Image", use_column_width=True)
        if st.button("Run AI Detection"):
            with st.spinner("Processing image with AI..."):
                result_image = draw_detection_boxes(uploaded_file, model)
                st.image(result_image, caption="Detection Result", use_column_width=True)
                st.success("✅ AI Detection Complete")


def cad_visualization():
    st.subheader("📐 CAD Model Preview & Simulation")
    st.write("This section contains visuals and animations from the CAD and simulation team.")

    st.image("media/images/cad_render.png", caption="SmartSecure IoT Device - Render", use_column_width=True)
    st.video("media/videos/cad_demo.mp4")


def about_section():
    st.title("SmartSecure IoT Hub")
    st.markdown("""
    ### 🚀 Mission
    To make Covenant University smarter and safer using real-time IoT monitoring and AI-powered vision security.

    ### 🧠 What It Does
    - Monitors temperature, gas, vibration, and smoke levels across hostels, lecture halls, and labs.
    - Uses AI to detect suspicious activity and send real-time alerts to school management.
    - Enhances campus safety, prevents disasters, and improves infrastructure reliability.

    ### 🧑‍💻 Team Roles
    - **Praise Adeyeye** – Python/Streamlit developer, AI security module, dashboard logic
    - **Farouk Umoru** – CAD design, rendering, simulation model visualization
    """)


# --- MAIN STREAMLIT APP ---
def main():
    st.sidebar.title("🔍 SmartSecure Navigation")
    selection = st.sidebar.radio("Go to:", [
        "🏠 About", "📡 Sensor Dashboard", "🎯 AI Security Vision", "🎨 CAD Visuals"])

    model = YOLO("yolov8n.pt")

    if selection == "🏠 About":
        about_section()
    elif selection == "📡 Sensor Dashboard":
        sensor_dashboard()
    elif selection == "🎯 AI Security Vision":
        ai_vision_security(model)
    elif selection == "🎨 CAD Visuals":
        cad_visualization()


if __name__ == '__main__':
    main()
