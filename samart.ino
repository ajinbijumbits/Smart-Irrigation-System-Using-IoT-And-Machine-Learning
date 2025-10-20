#define BLYNK_TEMPLATE_ID "TMPL3-xejFyOH"
#define BLYNK_TEMPLATE_NAME "Smart Irrigation"
#define BLYNK_AUTH_TOKEN "bnkJCgF0Jdjhcx_AQQRh6xcS-8JmesAG"

#include <WiFi.h>
#include <WiFiClient.h>
#include <BlynkSimpleEsp32.h>
#include "DHT.h"

// --- Pin Configuration ---
#define SOIL_PIN 34
#define DHTPIN 4
#define DHTTYPE DHT11
#define RELAY_PIN 13

// --- WiFi Credentials ---
char ssid[] = "ajin";
char pass[] = "kuttapan";

// --- Sensor Objects ---
DHT dht(DHTPIN, DHTTYPE);
BlynkTimer timer;

// --- Send Data Function ---
void sendSensorData() {
  int soilValue = analogRead(SOIL_PIN);
  int soilPercent = map(soilValue, 0, 4095, 100, 0);

  float h = dht.readHumidity();
  float t = dht.readTemperature();

  // --- Check Sensor Validity ---
  if (isnan(h) || isnan(t)) {
    Serial.println("❌ DHT11 Error — Skipping this cycle");
    return;
  }

  // --- Display in Serial Monitor ---
  Serial.print("🌱 Soil: ");
  Serial.print(soilPercent);
  Serial.print("% | 🌡 Temp: ");
  Serial.print(t);
  Serial.print("°C | 💧 Humidity: ");
  Serial.print(h);
  Serial.println("%");

  // --- Send to Blynk ---
  Blynk.virtualWrite(V0, soilPercent);
  Blynk.virtualWrite(V1, t);
  Blynk.virtualWrite(V2, h);

  // --- Pump Control (Fixed Logic + Delay Protection) ---
  static unsigned long lastPumpToggle = 0;
  const unsigned long debounceDelay = 5000;  // avoid relay flickering

  if (millis() - lastPumpToggle > debounceDelay) {
    if (soilPercent < 40) {
      digitalWrite(RELAY_PIN, HIGH);  // ON (if relay active HIGH)
      Blynk.virtualWrite(V3, 1);
      Serial.println("🚰 Pump: ON");
    } else {
      digitalWrite(RELAY_PIN, LOW);   // OFF
      Blynk.virtualWrite(V3, 0);
      Serial.println("🚰 Pump: OFF");
    }
    lastPumpToggle = millis();
  }
}

// --- Manual Pump Control from Blynk ---
BLYNK_WRITE(V3) {
  int pumpControl = param.asInt();
  if (pumpControl == 1) {
    digitalWrite(RELAY_PIN, HIGH);
    Serial.println("🚰 Pump manually turned ON via Blynk");
  } else {
    digitalWrite(RELAY_PIN, LOW);
    Serial.println("🚰 Pump manually turned OFF via Blynk");
  }
}

// --- Setup ---
void setup() {
  Serial.begin(9600);

  pinMode(RELAY_PIN, OUTPUT);
  digitalWrite(RELAY_PIN, LOW);  // OFF initially

  dht.begin();

  Serial.println("🌿 Connecting to WiFi...");
  Blynk.begin(BLYNK_AUTH_TOKEN, ssid, pass);

  timer.setInterval(3000L, sendSensorData);  // every 3 seconds
}

// --- Loop ---
void loop() {
  Blynk.run();
  timer.run();
}
