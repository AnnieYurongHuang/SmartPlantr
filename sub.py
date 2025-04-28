import paho.mqtt.client as mqtt

# MQTT config
MQTT_BROKER = "test.mosquitto.org"
MQTT_TOPIC = "smartplant/data"

# Callback on message received
def on_message(client, userdata, msg):
    print(f"[SmartPlant] {msg.payload.decode()}")

# Setup client
client = mqtt.Client()
client.on_message = on_message

client.connect(MQTT_BROKER, 1883, 60)
client.subscribe(MQTT_TOPIC)

print("Listening for SmartPlantr updates...\n")
client.loop_forever()
