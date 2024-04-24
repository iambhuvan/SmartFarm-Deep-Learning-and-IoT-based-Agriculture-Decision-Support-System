#include <WiFi.h>
#include <AsyncTCP.h>
#include <ESPAsyncWebSrv.h>
#include <DHT.h>
#include <Wire.h>
#include <LiquidCrystal_I2C.h>
#include <ArduinoJson.h>

AsyncWebServer server(80);

#define DHTPIN 12      // DHT sensor pin
#define DHTTYPE DHT11  // DHT sensor type

#define SOIL_PIN 34  // Soil moisture sensor pin


LiquidCrystal_I2C lcd(0x27, 16, 2);

const char* ssid = "project";
const char* password = "1234567890";


const char* PARAM_MESSAGE = "message";.0

void notFound(AsyncWebServerRequest* request) {
  request->send(404, "text/plain", "Not found");
}
int t, h, s;

int c = 0;

const unsigned long eventInterval = 2000;
unsigned long previousTime = 0;
DHT dht(DHTPIN, DHTTYPE);

DynamicJsonDocument doc(200);


void setup() {
  Serial.begin(9600);
  pinMode(14, OUTPUT);
  digitalWrite(14, HIGH);
  dht.begin();
  lcd.init();
  lcd.backlight();

  lcd.clear();
  lcd.setCursor(0, 0);
  // lcd.print("Connecting...l
  lcd.print("Printing");

  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);
    while (WiFi.status() != WL_CONNECTED) {
        delay(500);
        Serial.print(".");
    }

  lcd.clear();

  lcd.setCursor(0, 0);
  lcd.print(WiFi.localIP());

  server.on("/", HTTP_GET, [](AsyncWebServerRequest* request) {
    String jsonString;
    serializeJson(doc, jsonString);
    request->send(200, "text/plain", jsonString);
  });

  server.onNotFound(notFound);

  server.begin();
}
void loop() {
  t = dht.readTemperature();
  h = dht.readHumidity();
  s = 4096-analogRead(34);
  s = map(s,0,4096,0,100);
  doc["T"] = t;
  doc["H"] = h;
  doc["S"] = s;
  unsigned long currentTime = millis();
  if (currentTime - previousTime >= eventInterval) {
    lcd.setCursor(0, 1);
    if (c == 3) c = 0;
    if (c == 0) lcd.print("Temp : " + String(t) + " C              ");
    if (c == 1) lcd.print("Humi : " + String(h) + " %              ");
    if (c == 2) lcd.print("Soil : " + String(s) + " %              ");
    c = c + 1;
    previousTime = currentTime;
  }
}