// Auto watering system pin
int water;
const int soilMoisture = 6;
const int motorInput1 = 11;
const int motorInput2 = 13;

// Auto light system pin
const int photoresistor = A0;
const int LED1 = 3;
const int LED2 = 9;
const int LED3 = 10;
const int LM35 = A1;

// Auto temperature system pin
const int FAN = 5;
const int TEMPthreshold = 100;

// States
const int AUTO = 0;
const int MANUAL = 1;

int LED1_mode = AUTO;
int LED2_LED3_mode = AUTO;
int FAN_mode = AUTO;
int PUMP_mode = AUTO;

void setup() {
  Serial.begin(9600);
  
  // Configure pins as inputs or outputs
  pinMode(soilMoisture, INPUT);
  pinMode(motorInput1, OUTPUT);
  pinMode(motorInput2, OUTPUT);

  pinMode(photoresistor, INPUT);
  pinMode(LED1, OUTPUT);
  pinMode(LED2, OUTPUT);
  pinMode(LED3, OUTPUT);

  pinMode(LM35, INPUT);
  pinMode(FAN, OUTPUT);

  // Ensure LEDs are initially turned off
  digitalWrite(LED1, LOW);
  digitalWrite(LED2, LOW);
  digitalWrite(LED3, LOW);
}

void loop() {
  // Check for Serial Input
  if (Serial.available()) {
    int command = Serial.parseInt();

    switch (command) {
      case 100:
        LED1_mode = AUTO;
        LED2_LED3_mode = AUTO;
        FAN_mode = AUTO;
        PUMP_mode = AUTO;
        break;
      case 1:
        LED1_mode = MANUAL;
        digitalWrite(LED1, HIGH);
        break;
      case 10:
        LED1_mode = MANUAL;
        digitalWrite(LED1, LOW);
        break;
      case 2:
        LED2_LED3_mode = MANUAL;
        digitalWrite(LED2, HIGH);
        digitalWrite(LED3, HIGH);
        break;
      case 20:
        LED2_LED3_mode = MANUAL;
        digitalWrite(LED2, LOW);
        digitalWrite(LED3, LOW);
        break;
      case 3:
        LED1_mode = MANUAL;
        LED2_LED3_mode = MANUAL;
        digitalWrite(LED1, HIGH);
        digitalWrite(LED2, HIGH);
        digitalWrite(LED3, HIGH);
        break;
      case 30:
        LED1_mode = MANUAL;
        LED2_LED3_mode = MANUAL;
        digitalWrite(LED1, LOW);
        digitalWrite(LED2, LOW);
        digitalWrite(LED3, LOW);
        break;
      case 4:
        FAN_mode = MANUAL;
        digitalWrite(FAN, HIGH);
        break;
      case 40:
        FAN_mode = MANUAL;
        digitalWrite(FAN, LOW);
        break;
      case 5:
        PUMP_mode = MANUAL;
        digitalWrite(motorInput1, HIGH);
        digitalWrite(motorInput2, LOW);
        break;
      case 50:
        PUMP_mode = MANUAL;
        digitalWrite(motorInput1, LOW);
        digitalWrite(motorInput2, LOW);
        break;
      default:
        break;
    }
  }

  // If in AUTO mode, handle the logic for LED1, LED2/LED3, Fan, Pump

  // LED1
  if (LED1_mode == AUTO) {
    int lightValue = analogRead(photoresistor);
    Serial.print("Light Value: ");
    Serial.println(lightValue);
    if (lightValue < 150) {
      digitalWrite(LED1, LOW);
    } else if (lightValue < 200) {
      digitalWrite(LED1, HIGH);
    }
  }

  // LED2 and LED3
  if (LED2_LED3_mode == AUTO) {
    int lightValue = analogRead(photoresistor);
    if (lightValue < 150) {
      digitalWrite(LED2, LOW);
      digitalWrite(LED3, LOW);
    } else if (lightValue < 500) {
      digitalWrite(LED2, HIGH);
      digitalWrite(LED3, HIGH);
    } else {
      digitalWrite(LED2, HIGH);
      digitalWrite(LED3, HIGH);
    }
  }

  // Fan
  if (FAN_mode == AUTO) {
    int tempValue = analogRead(LM35);
    Serial.print("Temperature: ");
    Serial.println(tempValue);
    if (tempValue > TEMPthreshold) {
      digitalWrite(FAN, HIGH);
    } else {
      digitalWrite(FAN, LOW);
    }
  }


  // Pump
  if (PUMP_mode == AUTO) {
    water = digitalRead(soilMoisture);
    Serial.print("Water: ");
    Serial.println(water);
    if (water == HIGH) {
      digitalWrite(motorInput1, HIGH);
      digitalWrite(motorInput2, LOW);
    } else {
      digitalWrite(motorInput1, LOW);
      digitalWrite(motorInput2, LOW);
    }
  }

  delay(500);
}
