# SmartSecure IoT Hub - Full Streamlit App
# Author: Praise Adeyeye (Covenant University)
# Description: AI-powered security system + real-time IoT sensor dashboard

# --- Libraries ---
import streamlit as st
import numpy as np
import pandas as pd
from PIL import Image, ImageDraw
import plotly.graph_objects as go
from streamlit_lottie import st_lottie
from ultralytics import YOLO
import json

# --- Page Setup ---
st.set_page_config(page_title="SmartSecure IoT Hub", layout="wide")


# --- Load Lottie Animation ---

def load_lottiefile(filepath: str):
    with open(filepath, "r") as f:
        return json.load(f)


# --- Simulate IoT Sensor Readings ---
def simulate_sensor_data():
    return {
        "Temperature (C)": np.random.uniform(20, 70),
        "Humidity (%)": np.random.uniform(30, 90),
        "Gas Level (ppm)": np.random.uniform(200, 900),
        "Vibration (m/s²)": np.random.uniform(0, 5),
        "Smoke Level": np.random.uniform(0, 100)
    }


# --- Generate Alert Messages Based on Readings ---
def create_alerts(data):
    alerts = []
    if data['Temperature (C)'] > 50:
        alerts.append("🔥 High Temperature Detected!")
    if data['Gas Level (ppm)'] > 600:
        alerts.append("🧪 Gas Leak Detected!")
    if data['Vibration (m/s²)'] > 3:
        alerts.append("⚠️ High Vibration - Structural Risk!")
    if data['Smoke Level'] > 50:
        alerts.append("🚨 Smoke Detected!")
    return alerts


# --- Draw Bounding Boxes for Object Detection ---
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


# --- Sensor Dashboard UI ---
def sensor_dashboard():
    st.subheader("🔧 IoT Sensor Monitoring Dashboard")
    col1, col2 = st.columns(2)

    with col1:
        st_lottie(load_lottiefile("media/lottie/sensors.json"), height=200)

    with col2:
        st.write("Real-time simulated IoT readings:")
        data = simulate_sensor_data()
        df = pd.DataFrame([data])
        st.dataframe(df.round(2), use_container_width=True)

    # Gauge-style charts for each sensor
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

    # Show alerts if thresholds exceeded
    alerts = create_alerts(data)
    if alerts:
        st.error("\n".join(alerts))
    else:
        st.success("✅ All systems operating within safe parameters.")


# --- AI Security Vision Module ---
def ai_vision_security(model):
    st.subheader("🧠 AI Security Camera System")
    st_lottie(load_lottiefile("media/lottie/security.json"), height=200)
    uploaded_file = st.file_uploader("Upload an image for AI scan", type=["jpg", "jpeg", "png"])

    if uploaded_file:
        st.image(uploaded_file, caption="Uploaded Image", use_column_width=True)
        if st.button("Run AI Detection"):
            with st.spinner("Processing with YOLOv8..."):
                result_image = draw_detection_boxes(uploaded_file, model)
                st.image(result_image, caption="Detection Result", use_column_width=True)
                st.success("✅ AI Detection Complete")


# --- CAD Simulation Preview ---
def cad_visualization():
    st.subheader("📐 CAD Model & Simulation")
    st.write("Preview of hardware device designed for deployment.")

    st.image("media/images/cad_render.png", caption="SmartSecure IoT Device", use_column_width=True)
    st.video("media/videos/cad_demo.mp4")


# --- About Project Section ---
def about_section():
    st.title("SmartSecure IoT Hub")
    st.markdown("""
    ### 🚀 Our Mission  
    Enhance campus security at Covenant University with real-time IoT & AI vision systems.

    ### 🔍 Features  
    - Real-time monitoring of environmental data (gas, smoke, temperature).
    - AI-powered object detection for security surveillance.
    - CAD-based hardware visualization for future deployment.

    ### 🧑‍💻 Team  
    - **Praise Adeyeye** – Lead Developer, AI Vision, Streamlit UI  
    - **Farouk Umoru** – CAD Design, Simulation, Device Architecture  
    """)


# --- Main Navigation ---
def main():
    st.sidebar.title("🔍 SmartSecure Navigation")
    selection = st.sidebar.radio("Choose Section:", [
        "🏠 About", "📡 Sensor Dashboard", "🎯 AI Security Vision", "🎨 CAD Visuals"
    ])

    model = YOLO("yolov8n.pt")  # Load pretrained AI model

    if selection == "🏠 About":
        about_section()
    elif selection == "📡 Sensor Dashboard":
        sensor_dashboard()
    elif selection == "🎯 AI Security Vision":
        ai_vision_security(model)
    elif selection == "🎨 CAD Visuals":
        cad_visualization()


# --- Run App ---
if __name__ == "__main__":
    main()
