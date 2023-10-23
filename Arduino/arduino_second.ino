int motorAPower = 10;
int motorADirection = 12;
int nutrientLevelSensor = 7;

bool nutrientPumpOn = false;
long int nutrientPumpStartTime = millis();
long int nutrientPumpScheduledTime = millis();
int nutrientPumpCounter = 0;

void setup() {
  Serial.begin(9600);
  pinMode(motorAPower, OUTPUT);
  pinMode(motorADirection, OUTPUT);
  pinMode(nutrientLevelSensor, INPUT);
}

void loop() {
  int waterLevel = digitalRead(7);
    
  if (Serial.available()) {
    int command = Serial.parseInt();
      switch (command) {
        case 6:
          if(waterLevel == HIGH){
            nutrientPumpScheduledTime = millis();
            nutrientPumpCounter = 3;
          }
          break;
        case 60:
          nutrientPumpCounter = 0;
          stopNutrientPump();
          break;
        case 999:
          Serial.print("level:");
          Serial.println(waterLevel);
      }
  }
  
  if(nutrientPumpCounter > 0 && millis() >= nutrientPumpScheduledTime){
    startNutrientPump();
  }
  if(nutrientPumpOn){
    long int currentTime = millis();
    if(currentTime - nutrientPumpStartTime >= 1000){
      stopNutrientPump();
    }
  }
  
}

void startNutrientPump(){
  int pumpPower = 150;
  nutrientPumpOn = true;
  nutrientPumpStartTime = millis();
  nutrientPumpScheduledTime = millis() + 120000;
  nutrientPumpCounter -= 1;

  digitalWrite(motorADirection, LOW);
  analogWrite(motorAPower, pumpPower);
}

void stopNutrientPump(){
  nutrientPumpOn = false;
  analogWrite(motorAPower, 0);
}
