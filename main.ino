#include <WiFi.h>
#include <ThingSpeak.h>
#include <Wire.h>
#include <LiquidCrystal_I2C.h>

// ====== ThingSpeak Settings ======
const char* apiKey = "OUZFLO152RA77S8J";
int channelId=3081768;

WiFiClient client;

const char* ssid = "Mad";
const char* password = "123madhu";


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
  ThingSpeak.begin(client);

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

    ThingSpeak.setField(1,String(count));
    int httpCode=ThingSpeak.writeFields(channelId,apiKey);

    if (httpCode > 0) {
      Serial.println("Sent to ThingSpeak: " + String(count));
    } else {
      Serial.println("Data not Uploaded due to weak Internet");
    }
  }
}
