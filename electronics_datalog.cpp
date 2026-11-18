#include <DHT.h>

// Define pins for voltage sensing
const int voltagePins[5] = {A0, A1, A2, A3, A4}; // Analog pins A0 to A4

// Define pin for DHT22 sensor
#define DHTPIN 2 // Digital pin 2
#define DHTTYPE DHT22 // DHT 22 (AM2302)

// Initialize DHT sensor
DHT dht(DHTPIN, DHTTYPE);

// Define pin for current sensing
const int currentPin = A6; // Analog pin A6

// Define pin for on/off control
const int controlPin = 7; // Digital pin 7

// Variables to store sensor readings
float voltages[5];
float temperature;
float humidity;
float current;

void setup() {
  // Initialize serial communication at 9600 baud rate
  Serial.begin(9600);

  // Set the control pin as output
  pinMode(controlPin, OUTPUT);
  digitalWrite(controlPin, LOW); // Ensure the control pin is off initially

  // Initialize DHT sensor
  dht.begin();

  // Optionally, print initial message
  Serial.println("System Initialized");
}

void loop() {
  // Read voltages from the 5 analog pins
  for (int i = 0; i < 5; i++) {
    voltages[i] = analogRead(voltagePins[i]) * (5.0 / 1023.0); // Convert to voltage
  }

  // Read temperature and humidity from DHT22 sensor
  temperature = dht.readTemperature();
  humidity = dht.readHumidity();

  // Read current from the analog pin and convert to a meaningful value
  int currentRaw = analogRead(currentPin);
  current = currentRaw * (5.0 / 1023.0); // Example conversion

  // Send the readings through serial communication
  Serial.print("{Voltages: [");
  for (int i = 0; i < 5; i++) {
    Serial.print(voltages[i]);
    Serial.print(", ");
  }
  Serial.print("]")
  Serial.print(" , Temperature: ");
  Serial.print(temperature);
  Serial.print(", Current: ");
  Serial.print(current);
  Serial.println("}\n");

  // Check for serial input and control the output pin
  if (Serial.available() > 0) {
    String command = Serial.readStringUntil('\n');
    command.trim(); // Remove any trailing newline characters

    if (command == "on") {
      digitalWrite(controlPin, HIGH);
      Serial.println("Device ON");
    } else if (command == "off") {
      digitalWrite(controlPin, LOW);
      Serial.println("Device OFF");
    }
  }

  // Delay to avoid flooding the serial monitor
  delay(1000);
}

