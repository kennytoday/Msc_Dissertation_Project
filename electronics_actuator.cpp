#include <DHT.h>
#include <DHT_U.h>
#include <SD.h>

// Define analog pin connections
const int cell1Pin = A0;
const int cell2Pin = A1;
const int cell3Pin = A2;
const int cell4Pin = A3;
const int cell5Pin = A4;
const int currentPin = A5;

// SD card setup
const int chipSelect = 10;

// DHT22 setup
#define DHTPIN 2      // Pin which is connected to the DHT sensor
#define DHTTYPE DHT22   // DHT 22 (AM2302)
DHT dht(DHTPIN, DHTTYPE);

void setup() {
  Serial.begin(9600);
  while (!Serial); // Wait for serial to be connected
  Serial.println(F("Battery Management System Data Logger"));

  // Initialize the SD card
  if (!SD.begin(chipSelect)) {
    Serial.println("Initialization of SD card failed!");
    while (1);
  }
  Serial.println("SD card is ready to use.");

  // Create or open the file on SD card
  File dataFile = SD.open("battery_log.csv", FILE_WRITE);
  if (dataFile) {
    dataFile.println("Temperature (C), Voltage1 (V), Voltage2 (V), Voltage3 (V), Voltage4 (V), Voltage5 (V), Current (A)");
    dataFile.close();
  } else {
    Serial.println("Error opening battery_log.csv");
    while (1);
  }

  // Initialize DHT22 sensor
  dht.begin();
}

void loop() {
  // Read temperature from DHT22 sensor
  float temperature = dht.readTemperature();
  
  // Read voltage levels
  float voltage1 = analogRead(cell1Pin) * (5.0 / 1023.0);
  float voltage2 = analogRead(cell2Pin) * (5.0 / 1023.0);
  float voltage3 = analogRead(cell3Pin) * (5.0 / 1023.0);
  float voltage4 = analogRead(cell4Pin) * (5.0 / 1023.0);
  float voltage5 = analogRead(cell5Pin) * (5.0 / 1023.0);
  
  // Read current level
  float current = analogRead(currentPin) * (5.0 / 1023.0);
  
  // Open the file again to log data
  File dataFile = SD.open("battery_log.csv", FILE_WRITE);
  if (dataFile) {
    dataFile.print(temperature);
    dataFile.print(", ");
    dataFile.print(voltage1);
    dataFile.print(", ");
    dataFile.print(voltage2);
    dataFile.print(", ");
    dataFile.print(voltage3);
    dataFile.print(", ");
    dataFile.print(voltage4);
    dataFile.print(", ");
    dataFile.print(voltage5);
    dataFile.print(", ");
    dataFile.println(current);
    dataFile.close();
  } else {
    Serial.println("Error opening battery_log.csv");
  }
  
  // Delay before the next reading
  delay(1000);
}
