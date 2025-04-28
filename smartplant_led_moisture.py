import time
import board
import busio
import neopixel
import paho.mqtt.publish as publish
from adafruit_seesaw.seesaw import Seesaw

# Setup soil sensor
i2c_bus = busio.I2C(board.SCL, board.SDA)
ss = Seesaw(i2c_bus, addr=0x36)

# Setup NeoPixel
NUM_PIXELS = 8
PIXEL_PIN = board.D18
pixels = neopixel.NeoPixel(PIXEL_PIN, NUM_PIXELS, brightness=0.4, auto_write=False)

# MQTT Broker config
MQTT_BROKER = "test.mosquitto.org"
MQTT_TOPIC = "smartplant/data"

# Color functions
def set_color(color):
    pixels.fill(color)
    pixels.show()

def wheel(pos):
    if pos < 85:
        return (255 - pos * 3, pos * 3, 0)
    elif pos < 170:
        pos -= 85
        return (0, 255 - pos * 3, pos * 3)
    else:
        pos -= 170
        return (pos * 3, 0, 255 - pos * 3)

def rainbow_cycle(wait):
    for j in range(255):
        for i in range(NUM_PIXELS):
            rc_index = (i * 256 // NUM_PIXELS) + j
            pixels[i] = wheel(rc_index & 255)
        pixels.show()
        time.sleep(wait)

# Main loop
while True:
    try:
        touch = ss.moisture_read()
        temp_c = ss.get_temp()
        
        # Calibrate temperature (original temp_f - 12.7)
        temp_f = (temp_c * 9 / 5) + 32 - 12.7
        
        # Convert raw moisture to percentage (0–100%)
        moisture_pct = max(0, min(100, int((touch - 200) / (1000 - 200) * 100)))

        # Output to terminal
        print("Temp (F):", round(temp_f, 2), "Moisture (%):", moisture_pct)

        # Publish over MQTT
        message = f"Temp: {round(temp_f, 2)} | Moisture: {moisture_pct} | led:{'on' if temp_f > 90 or moisture_pct > 80 else 'ok'}"
        publish.single(MQTT_TOPIC, message, hostname=MQTT_BROKER)

        # LED logic
        if temp_f > 90 or moisture_pct > 80:
            set_color((255, 0, 0))  # Red = warning
        else:
            rainbow_cycle(0.01)     # Rainbow = healthy

        time.sleep(1)

    except Exception as e:
        print("Error:", e)
        set_color((0, 0, 255))  # Blue = error
        time.sleep(2)
