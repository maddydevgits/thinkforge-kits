#include <WiFi.h>
#include <HTTPClient.h>
#include <Wire.h>
#include <LiquidCrystal_I2C.h>

// ====== ThingSpeak Settings ======
String apiKey = "YOUR_THINGSPEAK_WRITE_API_KEY";
const char* ssid = "YOUR_WIFI_SSID";
const char* password = "YOUR_WIFI_PASSWORD";
const char* server = "http://api.thingspeak.com/update";

// ====== IR Sensors & LCD ======
#define IR1 32   // Inside sensor
#define IR2 33   // Outside sensor

LiquidCrystal_I2C lcd(0x27, 16, 2);

int count = 0;

void setup() {
  Serial.begin(115200);
  pinMode(IR1, INPUT_PULLUP);
  pinMode(IR2, INPUT_PULLUP);

  lcd.init();
  lcd.backlight();
  lcd.print("Connecting WiFi");

  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  
  lcd.clear();
  lcd.print("WiFi Connected");
  delay(1000);
  updateLCD();
}

void loop() {
  // If someone triggers IR2 first, then IR1 → Entry
  if (digitalRead(IR2) == LOW) {
    while (digitalRead(IR1) == HIGH); // wait for IR1
    count++;
    Serial.println("Entry detected");
    updateLCD();
    sendToThingSpeak();
    delay(1000); // debounce
  }

  // If someone triggers IR1 first, then IR2 → Exit
  if (digitalRead(IR1) == LOW) {
    while (digitalRead(IR2) == HIGH); // wait for IR2
    if (count > 0) count--;
    Serial.println("Exit detected");
    updateLCD();
    sendToThingSpeak();
    delay(1000); // debounce
  }
}

void updateLCD() {
  lcd.clear();
  lcd.setCursor(0,0);
  lcd.print("Canteen Count:");
  lcd.setCursor(0,1);
  lcd.print(count);
}

void sendToThingSpeak() {
  if (WiFi.status() == WL_CONNECTED) {
    HTTPClient http;
    String url = server;
    url += "?api_key=" + apiKey;
    url += "&field1=" + String(count);

    http.begin(url);
    int httpCode = http.GET();
    if (httpCode > 0) {
      Serial.println("Sent to ThingSpeak: " + String(count));
    }
    http.end();
  }
}
