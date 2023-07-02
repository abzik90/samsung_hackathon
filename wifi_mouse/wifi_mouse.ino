#include <Wire.h>
#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>
#include "MPU6050.h"

MPU6050 mpu;
// Replace with your network credentials
const char* ssid = "AAstana2.4";
const char* password = "Astana382@";
WiFiClient client;


// Replace with your server URL
const char* serverUrl = "http://192.168.1.14:5000";

const int buttonPin = D6;  // D6 (GPIO12) for button input
bool buttonPressed = false;
int16_t ax, ay, az;
int16_t gx, gy, gz;

void setup() {
  Serial.begin(115200);
  mpu.initialize();
  pinMode(buttonPin, INPUT_PULLUP);  // Set button pin as input with internal pull-up resistor

  Wire.begin(2, 14);  // Initialize I2C communication


  // Connect to Wi-Fi
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to WiFi...");
  }

  Serial.println("Connected to WiFi");
}

void loop() {
  // Read accelerometer values
  mpu.getMotion6(&ax, &ay, &az, &gx, &gy, &gz);
  String action = "";
  if (digitalRead(buttonPin) == LOW && !buttonPressed) {
    buttonPressed = true;
    Serial.println("Button pressed");
    action = "&action=click";
  }
  else if (digitalRead(buttonPin) == HIGH) {
    buttonPressed = false;
  }

  String url = String(serverUrl) + "?accelX=" + String(ax) + "&accelY=" + String(ay) + action;
  Serial.print("Sending request to: ");
  Serial.println(url);

  HTTPClient http;
  http.begin(client, url);

  int httpResponseCode = http.GET();
  if (httpResponseCode > 0) {
    Serial.print("HTTP Response code: ");
    Serial.println(httpResponseCode);
  } else {
    Serial.println("Error on HTTP request");
  }

  http.end();
}
