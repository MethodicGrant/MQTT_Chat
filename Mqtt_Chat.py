import paho.mqtt.client as mqtt
import threading
import time
import ssl
from datetime import datetime

# === SETTINGS ===
BROKER = "YOUR_CLUSTER_ID.s2.eu.hivemq.cloud" # <-- replace with your HiveMQ Cloud hostname
PORT = 8883
USERNAME = "your_hivemq_username"
PASSWORD = "your_hivemq_password"

MY_NAME = "PI_ID" # Change PI_ID to the username of your PI
PEER_NAME = "PI_ID" # Change PI_ID to the username of your PI

MY_TOPIC = f"{MY_NAME}/messages"
PEER_TOPIC = f"{PEER_NAME}/messages"
CLIENT_ID = f"{MY_NAME}_chat" # keep fixed for persistent session

SHOW_UTC = False # set True if you prefer UTC timestamps

# === TIME HELPERS ===
def now_str():
    t = datetime.utcnow() if SHOW_UTC else datetime.now()
    return t.strftime("%Y-%m-%d %H:%M:%S")

# === CALLBACKS ===
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print(f"✅ Connected securely to HiveMQ Cloud as {CLIENT_ID}")
        client.subscribe(MY_TOPIC, qos=1)
        print(f"📡 Listening on topic: {MY_TOPIC}")
    else:
        print(f"❌ Connection failed with code {rc}")

def on_message(client, userdata, msg):
    text = msg.payload.decode()
    timestamp = now_str()
    print(f"\n[{timestamp}] 💬 {text}")
    print("You: ", end="", flush=True)

def on_disconnect(client, userdata, rc):
    print("⚠️ Disconnected. Attempting reconnect...")
    while True:
        try:
            time.sleep(3)
            client.reconnect()
            break
        except:
            pass

# === CLIENT SETUP ===
client = mqtt.Client(client_id=CLIENT_ID, clean_session=False)
client.username_pw_set(USERNAME, PASSWORD)
client.tls_set(cert_reqs=ssl.CERT_REQUIRED, tls_version=ssl.PROTOCOL_TLS)

client.on_connect = on_connect
client.on_message = on_message
client.on_disconnect = on_disconnect

client.connect(BROKER, PORT, keepalive=60)
threading.Thread(target=client.loop_forever, daemon=True).start()

print(f"\n💬 Chat ready! Messages to {PEER_NAME} appear below.")
print("Type and press Enter to send. Ctrl+C to exit.\n")

try:
    while True:
        msg = input("You: ")
        if msg.strip():
            full_msg = f"{MY_NAME} [{now_str()}]: {msg}"
            result = client.publish(PEER_TOPIC, full_msg, qos=1, retain=False)
            if result.rc == 0:
                print(f"📨 Sent to {PEER_NAME}.")
            else:
                print("❌ Send failed.")
except KeyboardInterrupt:
    print("\n👋 Chat ended.")
finally:
    client.disconnect()
