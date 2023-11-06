#include <dht11.h>

#define DHT11PIN 4

dht11 DHT11;

// Auto light system pin
const int photoresistor = A0;
const int LED1 = 9;
const int LED2 = 10;
const int LED3 = 11;

const int Level1 = 350; 
const int Level2 = 200; 
const int Level3 = 100; 

// Auto temperature system pin
const int FAN = 3;
const int TEMPthreshold = 30;

// Auto watering system pin
int soil;
int water;
const int soilMoisture = 5;
const int waterPump = 6;
const int waterLevel = 7;
const int nutrientPump = 8;

// States
const int AUTO = 0;
const int MANUAL = 1;

int LED1_mode = AUTO;
int LED2_LED3_mode = AUTO;
int FAN_mode = AUTO;
int waterPump_mode = AUTO;
int nutrientPump_mode = AUTO;

void setup() {
  Serial.begin(9600);

  pinMode(photoresistor, INPUT);
  pinMode(LED1, OUTPUT);
  pinMode(LED2, OUTPUT);
  pinMode(LED3, OUTPUT);

  pinMode(FAN, OUTPUT);

  pinMode(soilMoisture, INPUT);
  pinMode(waterPump, OUTPUT);
  pinMode(waterLevel, INPUT);
  pinMode(nutrientPump, OUTPUT); 

  // Ensure LEDs are initially turned off
  digitalWrite(LED1, LOW);
  digitalWrite(LED2, LOW);
  digitalWrite(LED3, LOW);
}

void loop() {
  if (Serial.available()) {
    int command = Serial.parseInt();

    switch (command) {
      case 100:
        LED1_mode = AUTO;
        LED2_LED3_mode = AUTO;
        FAN_mode = AUTO;
        waterPump_mode = AUTO;
        nutrientPump_mode = AUTO;
        break;
      case 1:
        LED1_mode = MANUAL;
        digitalWrite(LED1, LOW);
        break;
      case 10:
        LED1_mode = MANUAL;
        digitalWrite(LED1, HIGH);
        break;
      case 2:
        LED2_LED3_mode = MANUAL;
        digitalWrite(LED2, LOW);
        digitalWrite(LED3, LOW);
        break;
      case 20:
        LED2_LED3_mode = MANUAL;
        digitalWrite(LED2, HIGH);
        digitalWrite(LED3, HIGH);
        break;
      case 3:
        LED1_mode = MANUAL;
        LED2_LED3_mode = MANUAL;
        digitalWrite(LED1, LOW);
        digitalWrite(LED2, LOW);
        digitalWrite(LED3, LOW);
        break;
      case 30:
        LED1_mode = MANUAL;
        LED2_LED3_mode = MANUAL;
        digitalWrite(LED1, HIGH);
        digitalWrite(LED2, HIGH);
        digitalWrite(LED3, HIGH);
        break;
      case 4:
        FAN_mode = MANUAL;
        digitalWrite(FAN, LOW);
        break;
      case 40:
        FAN_mode = MANUAL;
        digitalWrite(FAN, HIGH);
        break;
      case 5:
        waterPump_mode = MANUAL;
        digitalWrite(waterPump, LOW);
        break;
      case 50:
        waterPump_mode = MANUAL;
        digitalWrite(waterPump, HIGH);
        break;
      case 6:
        nutrientPump_mode = MANUAL;
        digitalWrite(nutrientPump, LOW);
        break;
      case 60:
        nutrientPump_mode = MANUAL;
        digitalWrite(nutrientPump, HIGH);
        break;
      default:
        break;
    }
  }

  // Light Control Logic
  int lightValue = analogRead(photoresistor);
  Serial.print("Light Value: ");
  Serial.println(lightValue);

  // LED1 control
  if (LED1_mode == AUTO) {
    if (lightValue > Level2 && lightValue < Level1) {
      digitalWrite(LED1, LOW);
    } else if (lightValue < Level2 && lightValue > Level3)
      digitalWrite(LED1, HIGH);    
    else if (lightValue < Level3) {
      digitalWrite(LED1, LOW);
    } else {
      digitalWrite(LED1, HIGH);
    }
  }

  // LED2 and LED3 control
  if (LED2_LED3_mode == AUTO) {
    if (lightValue < Level1 && lightValue > Level2) {
      digitalWrite(LED2, HIGH);
      digitalWrite(LED3, HIGH);
    } else if (lightValue < Level2) {
      digitalWrite(LED2, LOW);
      digitalWrite(LED3, LOW);
    } else {
      digitalWrite(LED2, HIGH);
      digitalWrite(LED3, HIGH);
    }
  }

  // Fan
  if (FAN_mode == AUTO) {
    int chk = DHT11.read(DHT11PIN);
    Serial.print("Temperature  (C): ");
    Serial.println((float)DHT11.temperature, 2);
    if(DHT11.temperature > TEMPthreshold) {
      digitalWrite(FAN, HIGH); 
    } else {
      digitalWrite(FAN, LOW);  
    }
  }

  // waterPump
  if (waterPump_mode == AUTO) {
    soil = digitalRead(soilMoisture);
    Serial.print("Soil: ");
    Serial.println(soil);
    if (soil == HIGH) {
      digitalWrite(waterPump, LOW);
    } else {
      digitalWrite(waterPump, HIGH);
    }
  }
  
  //nutrientPump
    if (nutrientPump_mode == AUTO) {
    water = digitalRead(waterLevel);
    Serial.print("Water Level: ");
    Serial.println(water);
    if (water == HIGH) {
      digitalWrite(nutrientPump, LOW);
    } else {
      digitalWrite(nutrientPump, HIGH);
    }
  }

  delay(500);
}
