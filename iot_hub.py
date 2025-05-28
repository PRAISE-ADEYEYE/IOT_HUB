import streamlit as st
import numpy as np
import pandas as pd
from PIL import Image, ImageDraw, ImageFont
import plotly.graph_objects as go
import random
import time

# Page setup
st.set_page_config(page_title="SmartSecure IoT Hub", layout="wide")
st.markdown(
    """
    <style>
        .big-title {
            font-size: 40px !important;
            color: #2c3e50;
            font-weight: bold;
        }
        .sub-section {
            font-size: 18px;
            color: #34495e;
        }
        .highlight {
            background-color: #f39c12;
            padding: 4px;
            border-radius: 5px;
            color: white;
        }
        .card {
            padding: 1rem;
            border-radius: 15px;
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
            background: #ffffff;
            margin-bottom: 1rem;
        }
    </style>
    """,
    unsafe_allow_html=True
)


# --- Functions ---
def overview_page():
    st.markdown(
        "<h1 style='font-size: 48px; color: #0c2461; font-weight: bold;'>🏠 SmartSecure IoT Hub</h1>",
        unsafe_allow_html=True
    )

    typing_area = st.empty()  # Reserve a space for typing effect

    intro_text = (
        "Welcome to SmartSecure — your all-in-one simulated IoT + AI security dashboard.\n\n"
        "Imagine a world where your environment is being monitored in real-time:\n"
        "- 🔥 Fire? Detected.\n"
        "- 💨 Gas leak? Alerted.\n"
        "- 👀 Intruder? Identified.\n\n"
        "SmartSecure provides that virtual simulation, giving you a complete tech demonstration "
        "without the need for physical sensors or cameras.\n\n"
        "Ready to dive in? Here’s what this powerful platform offers:"
    )

    def typewriter_effect(text, delay=0.02):
        output = ""
        for char in text:
            output += char
            typing_area.markdown(
                f"<div style='font-size: 20px; color: #2d3436; font-family: monospace; white-space: pre-wrap;'>{output}</div>",
                unsafe_allow_html=True
            )
            time.sleep(delay)

    typewriter_effect(intro_text)
    time.sleep(0.8)

    st.markdown("---")
    st.markdown(
        """
        <div style='font-size: 22px; color: #1e3799; font-weight: bold;'>✨ Features</div>
        <ul style='font-size: 18px; color: #2d3436;'>
            <li>📊 Live sensor dashboards (simulated)</li>
            <li>🧠 AI detection system demo</li>
            <li>🖼 CAD visualizations (static render)</li>
            <li>⚡ Smart alerting feedback</li>
        </ul>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div style='font-size: 22px; color: #1e3799; font-weight: bold;'>🧰 Technology Stack</div>
        <ul style='font-size: 18px; color: #2d3436;'>
            <li><b>Streamlit</b> - Interactive web interface</li>
            <li><b>NumPy + Pandas</b> - Simulated real-time sensor data</li>
            <li><b>Plotly</b> - Dynamic gauges and charts</li>
            <li><b>Pillow</b> - AI image processing demonstration</li>
        </ul>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div style='font-size: 22px; color: #1e3799; font-weight: bold;'>🧑‍💻 Created By</div>
        <p style='font-size: 18px; color: #2d3436;'>
            <b>Praise Adeyeye</b> — Lead Developer & Vision Architect<br>
            <b>Farouk Umoru</b> — Hardware Design & CAD Simulation
        </p>
        """,
        unsafe_allow_html=True,
    )

    st.success("🚀 Let’s explore the system using the sidebar menu ➡️")


def generate_sensor_data():
    return {
        "Temperature (°C)": round(random.uniform(20, 75), 2),
        "Humidity (%)": round(random.uniform(30, 90), 2),
        "Gas Level (ppm)": round(random.uniform(100, 900), 2),
        "Vibration (m/s²)": round(random.uniform(0, 5), 2),
        "Smoke Level (%)": round(random.uniform(0, 100), 2)
    }


def display_gauges(data):
    fig = go.Figure()
    for key, value in data.items():
        fig.add_trace(go.Indicator(
            mode="gauge+number",
            value=value,
            title={'text': key},
            gauge={'axis': {'range': [0, 100]}}
        ))
    fig.update_layout(grid={'rows': 2, 'columns': 3}, height=500)
    st.plotly_chart(fig, use_container_width=True)


def sensor_dashboard():
    st.markdown('<div class="big-title">📡 IoT Sensor Dashboard</div>', unsafe_allow_html=True)
    data = generate_sensor_data()
    df = pd.DataFrame([data])
    st.dataframe(df.style.highlight_max(axis=1), use_container_width=True)
    display_gauges(data)

    alerts = []
    if data["Temperature (°C)"] > 50:
        alerts.append("🔥 High Temperature")
    if data["Gas Level (ppm)"] > 600:
        alerts.append("🧪 Gas Leak Detected")
    if data["Smoke Level (%)"] > 60:
        alerts.append("🚨 Smoke Alert")
    if data["Vibration (m/s²)"] > 3:
        alerts.append("⚠️ Vibration Alert")

    if alerts:
        st.error(" | ".join(alerts))
    else:
        st.success("✅ All systems are stable.")


def draw_fake_ai_detection():
    img = Image.new("RGB", (640, 360), "white")
    draw = ImageDraw.Draw(img)
    draw.rectangle([50, 70, 250, 270], outline="red", width=3)
    draw.text((60, 60), "Intruder", fill="red")

    return img


def ai_security_vision():
    st.markdown('<div class="big-title">🎯 AI Security Vision (Simulated)</div>', unsafe_allow_html=True)
    st.write("This section simulates AI vision detection for security using static images.")
    if st.button("Run Simulated AI Detection"):
        st.image(draw_fake_ai_detection(), caption="Detection Result", use_column_width=True)
        st.success("✅ Mock AI Detection Complete")


def cad_visuals():
    st.markdown('<div class="big-title">🎨 CAD Visualization</div>', unsafe_allow_html=True)
    st.write("Simulated design of a Smart IoT Monitoring Device.")
    st.code("""
    +--------------------------------+
    |                                |
    |    SMARTSECURE DEVICE BODY     |
    |   [Sensors + Camera + WiFi]    |
    |                                |
    +--------------------------------+
    """, language='text')
    st.markdown("> **Note:** This is a simulated CAD representation. Real CAD renders can be embedded when available.")


# --- Main App Navigation ---
def main():
    st.sidebar.title("🔍 SmartSecure Navigation")
    section = st.sidebar.radio("Go to section:",
                               ["🏠 Overview", "📡 Sensor Dashboard", "🎯 AI Security Vision", "🎨 CAD Visuals"])

    if section == "🏠 Overview":
        overview_page()
    elif section == "📡 Sensor Dashboard":
        sensor_dashboard()
    elif section == "🎯 AI Security Vision":
        ai_security_vision()
    elif section == "🎨 CAD Visuals":
        cad_visuals()


if __name__ == "__main__":
    main()
