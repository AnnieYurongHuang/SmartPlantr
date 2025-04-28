# 🌱 SmartPlantr Project

Welcome to SmartPlantr — a smart, connected planter that monitors soil moisture and temperature in real-time, provides visual alerts, and gives AI-powered care suggestions.

---

## 📂 Project Structure

- `smartplant_led_moisture.py` → Runs on Raspberry Pi. Reads sensor data, controls NeoPixel LEDs, and publishes data to MQTT.
- `smartplant_dashboard.py` → Streamlit dashboard to visualize plant data and generate AI-driven plant messages.
- `sub.py` → A simple MQTT subscriber for debugging or extra testing.
- `all_requirements.txt` → Lists all required Python packages.
- `goals.txt` → Project goals and vision.
- `.env` → Stores your secret Gemini API key.
- `README.md` → (this file!)

---

## 🛠 Materials Needed

- Raspberry Pi (any modern model)
- Adafruit STEMMA Soil Sensor (capacitive moisture + temperature sensor)
- NeoPixel 1x8 RGB LED Strip (WS2812)
- Jumper wires, breadboard, optional enclosure
- Internet connection for MQTT communication
- Optional: USB power bank for portable setup

---

## 🔌 Hardware Setup

1. **Connect the Soil Sensor** to the Raspberry Pi via I2C (SCL and SDA pins).
2. **Connect the NeoPixel LED Strip** to GPIO18 (pin 12) + 5V + GND.
3. **Double check** all wiring for correct voltage and data lines.

---

## ⚙️ Software Setup

### 1. Create a Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate   # Windows
```

### 2. Install Required Packages
```bash
pip install -r all_requirements.txt
```

### 3. Set Up `.env` File
Create a `.env` file in the project folder with:

```
GEMINI_API_KEY=your_google_gemini_api_key_here
```

---

## 🚀 Running the Project

### Step 1: Start the Sensor Publisher
On the Raspberry Pi, run:

```bash
python smartplant_led_moisture.py
```
- This script reads sensor data.
- It publishes temperature and moisture to MQTT broker `test.mosquitto.org` on topic `smartplant/data`.
- It also controls the LED strip color based on plant health.

### Step 2: Launch the Streamlit Dashboard
On your computer (or Pi if powerful enough), run:

```bash
streamlit run smartplant_dashboard.py
```
- This dashboard listens to MQTT for plant data.
- It shows live charts and generates plant "messages" using Gemini AI.

### Step 3 (Optional): Run Basic MQTT Subscriber
If you want to debug MQTT separately, you can also run:

```bash
python sub.py
```

---

## 🧠 How It Works

- `smartplant_led_moisture.py` sends live plant data (temp + moisture) via MQTT.
- `smartplant_dashboard.py` listens, plots live charts, and generates playful AI plant updates.
- Sensors are protected inside a waterproof shell, and NeoPixel LEDs give quick visual feedback.

---

## 💡 Future Enhancements

- Google Assistant or Alexa integration
- Smarter watering predictions
- Multiple plants support

---

## 🎨 Visual Cues (LED)
- 🌈 **Rainbow Animation** = Plant is healthy
- 🔴 **Red Light** = Temperature too hot or moisture too high
- 🔵 **Blue Light** = Error detected (sensor or MQTT issue)

---

Enjoy building SmartPlantr! 🌿✨
