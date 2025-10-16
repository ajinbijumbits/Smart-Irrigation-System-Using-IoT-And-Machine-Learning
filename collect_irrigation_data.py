import requests
import csv
import time
from datetime import datetime

# --- Your Blynk Auth Token ---
BLYNK_AUTH_TOKEN = "bnkJCgF0Jdjhcx_AQQRh6xcS-8JmesAG"

# --- Blynk Cloud Base URL ---
BASE_URL = f"https://blynk.cloud/external/api/get?token={BLYNK_AUTH_TOKEN}"

# --- Virtual Pins ---
SENSORS = {
    "soil_moisture": "V0",
    "temperature": "V1",
    "humidity": "V2",
    "pump_state": "V3"
}

# --- CSV File to Save Data ---
CSV_FILE = "irrigation_data.csv"

# --- Initialize CSV Header ---
def init_csv():
    try:
        with open(CSV_FILE, mode='x', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Timestamp", "Soil (%)", "Temperature (°C)", "Humidity (%)", "Pump State"])
        print(f"✅ CSV file '{CSV_FILE}' created.")
    except FileExistsError:
        print(f"ℹ️ CSV file '{CSV_FILE}' already exists. Appending data...")

# --- Fetch Sensor Data from Blynk ---
def get_sensor_data():
    try:
        soil = requests.get(f"{BASE_URL}&{SENSORS['soil_moisture']}").text
        temp = requests.get(f"{BASE_URL}&{SENSORS['temperature']}").text
        hum = requests.get(f"{BASE_URL}&{SENSORS['humidity']}").text
        pump = requests.get(f"{BASE_URL}&{SENSORS['pump_state']}").text
        return {
            "soil": float(soil),
            "temp": float(temp),
            "hum": float(hum),
            "pump": int(pump)
        }
    except Exception as e:
        print("❌ Error fetching data:", e)
        return None

# --- Append Data to CSV ---
def append_to_csv(data):
    with open(CSV_FILE, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            data["soil"],
            data["temp"],
            data["hum"],
            data["pump"]
        ])

# --- Main Loop ---
def main():
    init_csv()
    print("📡 Starting data collection from Blynk...") 
    while True:
        data = get_sensor_data()
        if data:
            print(f"🌱 Soil: {data['soil']}% | 🌡 Temp: {data['temp']}°C | 💧 Hum: {data['hum']}% | Pump: {data['pump']}")
            append_to_csv(data)
        time.sleep(3)  # collect every 10 seconds

if __name__ == "__main__":
    main()
