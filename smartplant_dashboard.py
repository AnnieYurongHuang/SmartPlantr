import streamlit as st
import paho.mqtt.client as mqtt
import plotly.graph_objs as go
from collections import deque
import os
from dotenv import load_dotenv
import google.generativeai as genai
import time
import threading
from queue import Queue

# Load Gemini API key
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)

# Streamlit UI config
st.set_page_config(page_title="SmartPlantr Dashboard", layout="wide")
st.title("🌿 How is my plant doing")

# Tabs
tab1, tab2 = st.tabs(["📈 Plant Conditions", "🌡️ Temperature & Moisture Trends"])

# Data buffers
MAX_LEN = 50
temps = deque(maxlen=MAX_LEN)
moistures = deque(maxlen=MAX_LEN)
labels = deque(maxlen=MAX_LEN)

# Streamlit placeholders
status_box = tab1.empty()
ai_box = tab1.empty()
temp_chart = tab2.empty()
moist_chart = tab2.empty()

# MQTT config
MQTT_BROKER = "test.mosquitto.org"
MQTT_TOPIC = "smartplant/data"

# Thread-safe queue for MQTT messages
message_queue = Queue()

# Handle incoming messages
def on_message(client, userdata, msg):
    try:
        payload = msg.payload.decode()
        message_queue.put(payload)  # Add the message to the queue
    except Exception as e:
        message_queue.put(f"Error: {e}")

# MQTT client setup
client = mqtt.Client()
client.on_message = on_message
client.connect(MQTT_BROKER, 1883, 60)
client.subscribe(MQTT_TOPIC)

# Start MQTT loop in a separate thread
mqtt_thread = threading.Thread(target=client.loop_forever)
mqtt_thread.daemon = True
mqtt_thread.start()

last_time_upadte =  time.time() - 60

# Streamlit app loop
while True:
    if not message_queue.empty():
        payload = message_queue.get()
        try:
            # Process the payload
            parts = payload.replace(" ", "").split("|")
            temp = float(parts[0].split(":")[1])
            moist = int(parts[1].split(":")[1])

            # Store data
            temps.append(temp)
            moistures.append(moist)
            labels.append(len(labels))

            # Display status
            status_box.markdown(f"**🌡️ Temp:** {temp}°F  **💧 Moisture:** {moist}  ")

            # Plant personality via Gemini
            if time.time() - last_time_upadte > 60:
                prompt = f"""
                You are a dramatic, emotional houseplant. Based on these vitals:
                - Temperature: {temp}°F
                - Moisture: {moist}
                Give your human a short, like two sentence max message. Be expressive, funny, and real, end it with the action that the user should take. 
                """
                model = genai.GenerativeModel("gemini-2.0-flash")
                response = model.generate_content(prompt)
                ai_box.markdown(f"🧠 **SmartPlantr says:** {response.text}")
                last_time_upadte = time.time()

            # Update charts
            with temp_chart:
                st.plotly_chart(go.Figure(go.Scatter(
                    x=list(labels), y=list(temps), mode='lines+markers', name="Temp (F)")),
                    use_container_width=True)

            with moist_chart:
                st.plotly_chart(go.Figure(go.Scatter(
                    x=list(labels), y=list(moistures), mode='lines+markers', name="Moisture")),
                    use_container_width=True)

        except Exception as e:
            ai_box.error(f"⚠️ Error: {e}")

    time.sleep(0.1)  # Prevent high CPU usage