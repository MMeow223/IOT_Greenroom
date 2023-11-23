#include <dht11.h>

#define DHT11PIN 4

dht11 DHT11;

// States
const int AUTO = 0;
const int LEFT = 0;
const int MANUAL = 1;
const int RIGHT = 1;

// sensors pins
const int PIN_PHOTORESISTOR = A0;
const int PIN_SOIL_MOISTURE = A2;
const int PIN_WATER_LEVEL = 2;

// actuators pins
const int PIN_FAN = 9;
const int PIN_LED_ONE = 6;
const int PIN_LED_TWO = 7;
const int PIN_LED_THREE = 8;
const int PIN_NUTRIENT_PUMP_SPEED = 10;
const int PIN_WATER_PUMP_SPEED = 11;
const int PIN_NUTRIENT_PUMP_DIRECTION = 12;
const int PIN_WATER_PUMP_DIRECTION = 13;

// THRESHOLDS
const int BRIGHTNESS_LEVEL_ONE = 350;
const int BRIGHTNESS_LEVEL_TWO = 200;
const int BRITGHTNESS_LEVEL_THREE = 100;
const int TEMP_THRES = 30;
const int SOIL_MOISTURE_THRES = 500;

// Nutrient pump variables
bool nutrientPumpOn = false;
long int nutrientPumpStartTime = millis();
long int nutrientPumpScheduledTime = millis();
int nutrientPumpDuration = 1000;
int nutrientPumpCounter = 0;

int MODE_LED_ONE = AUTO;
int MODE_LED_TWO_THREE = AUTO;
int MODE_FAN = AUTO;
int MODE_WATER_PUMP = AUTO;
int MODE_NUTRIENT_PUMP = AUTO;

int soil_moisture_value = 0; // 0-1023
int water_level_value = 0;   // 0 or 1
int light_value = 0;         // 0-1023
int temperature_value = 0;   // 0-1023

void setup()
{
  // set baud rate
  Serial.begin(9600);

  // set pin mode
  pinMode(PIN_PHOTORESISTOR, INPUT);
  pinMode(PIN_LED_ONE, OUTPUT);
  pinMode(PIN_LED_THREE, OUTPUT);
  pinMode(PIN_LED_TWO, OUTPUT);
  pinMode(PIN_FAN, OUTPUT);
  pinMode(PIN_SOIL_MOISTURE, INPUT);
  pinMode(PIN_WATER_PUMP_SPEED, OUTPUT);
  pinMode(PIN_WATER_PUMP_DIRECTION, OUTPUT);
  pinMode(PIN_WATER_LEVEL, INPUT_PULLUP);
  pinMode(PIN_NUTRIENT_PUMP_SPEED, OUTPUT);
  pinMode(PIN_NUTRIENT_PUMP_DIRECTION, OUTPUT);

  // turn off all
  digitalWrite(PIN_LED_ONE, LOW);
  digitalWrite(PIN_LED_TWO, LOW);
  digitalWrite(PIN_LED_THREE, LOW);
}

void loop()
{

  ReadSensors();

  HandleSerialInput();

  ActuatorControl();

  delay(500);
}

// Read all the sensors
void ReadSensors()
{
  DHT11.read(DHT11PIN);
  light_value = analogRead(PIN_PHOTORESISTOR);
  temperature_value = DHT11.temperature;
  soil_moisture_value = analogRead(PIN_SOIL_MOISTURE);
  water_level_value = digitalRead(PIN_WATER_LEVEL);
}

// Handle serial input
void HandleSerialInput()
{
  if (Serial.available())
  {
    int command = Serial.parseInt();

    switch (command)
    {
    case 100: // set all actuators to auto mode
      MODE_LED_ONE = AUTO;
      MODE_LED_TWO_THREE = AUTO;
      MODE_FAN = AUTO;
      MODE_WATER_PUMP = AUTO;
      break;
    case 1: // set LED1 to manual mode and turn it off
      MODE_LED_ONE = MANUAL;
      digitalWrite(PIN_LED_ONE, LOW);
      digitalWrite(PIN_LED_TWO, HIGH);
      digitalWrite(PIN_LED_THREE, HIGH);
      break;
    case 10: // set LED1 to manual mode and turn it on
      MODE_LED_ONE = MANUAL;
      digitalWrite(PIN_LED_ONE, HIGH);
      break;
    case 2: // set LED2 and LED3 to manual mode and turn them off
      MODE_LED_TWO_THREE = MANUAL;
      digitalWrite(PIN_LED_ONE, HIGH);
      digitalWrite(PIN_LED_TWO, LOW);
      digitalWrite(PIN_LED_THREE, LOW);
      break;
    case 20: // set LED2 and LED3 to manual mode and turn them on
      MODE_LED_TWO_THREE = MANUAL;
      digitalWrite(PIN_LED_TWO, HIGH);
      digitalWrite(PIN_LED_THREE, HIGH);
      break;
    case 3: // set LED1, LED2 and LED3 to manual mode and turn them off
      MODE_LED_ONE = MANUAL;
      MODE_LED_TWO_THREE = MANUAL;
      digitalWrite(PIN_LED_ONE, LOW);
      digitalWrite(PIN_LED_TWO, LOW);
      digitalWrite(PIN_LED_THREE, LOW);
      break;
    case 30: // set LED1, LED2 and LED3 to manual mode and turn them on
      MODE_LED_ONE = MANUAL;
      MODE_LED_TWO_THREE = MANUAL;
      digitalWrite(PIN_LED_ONE, HIGH);
      digitalWrite(PIN_LED_TWO, HIGH);
      digitalWrite(PIN_LED_THREE, HIGH);
      break;
    case 4: // set fan to manual mode and turn it off
      MODE_FAN = MANUAL;
      digitalWrite(PIN_FAN, LOW);
      break;
    case 40: // set fan to manual mode and turn it on
      MODE_FAN = MANUAL;
      digitalWrite(PIN_FAN, HIGH);
      break;
    case 5: // set water pump to manual mode and turn it off
      MODE_WATER_PUMP = MANUAL;
      digitalWrite(PIN_WATER_PUMP_SPEED, LOW);
      break;
    case 50: // set water pump to manual mode and turn it on
      MODE_WATER_PUMP = MANUAL;
      digitalWrite(PIN_WATER_PUMP_SPEED, HIGH);
      break;
    case 6: // set nutrient pump configuration for later process
      nutrientPumpScheduledTime = millis();
      nutrientPumpCounter = 3;
      break;
    case 60: // reset nutrient pump configuration
      nutrientPumpCounter = 0;
      stopNutrientPump();
      break;
    case 999: // print all the sensor values
      Serial.print("sensor!light:");
      Serial.println(light_value);

      Serial.print("sensor!temp:");
      Serial.println((float)temperature_value, 2);

      Serial.print("sensor!soil:");
      Serial.println(soil_moisture_value);

      Serial.print("sensor!water:");
      Serial.println(water_level_value);
    default:
      break;
    }
  }
}

// Control all the actuators
void ActuatorControl()
{
  AutoLedControl();
  AutoFanControl();
  AutoWaterPumpControl();
  NutrientPumpLoop();
}

// Control all the LEDs
void AutoLedControl()
{
  AutoLedOneControl();
  AutoLedTwoThreeControl();
}

// Control LED1
void AutoLedOneControl()
{

  // PIN_LED_ONE control
  if (MODE_LED_ONE == AUTO)
  {
    if (light_value > BRIGHTNESS_LEVEL_TWO && light_value < BRIGHTNESS_LEVEL_ONE)
    {
      Serial.println("act!light:1");
      digitalWrite(PIN_LED_ONE, LOW);
    }
    else if (light_value < BRIGHTNESS_LEVEL_TWO && light_value > BRITGHTNESS_LEVEL_THREE)
      digitalWrite(PIN_LED_ONE, HIGH);
    else if (light_value < BRITGHTNESS_LEVEL_THREE)
    {
      Serial.println("act!light:3");
      digitalWrite(PIN_LED_ONE, LOW);
    }
    else
    {
      Serial.println("act!light:0");
      digitalWrite(PIN_LED_ONE, HIGH);
    }
  }
}

// Control LED2 and LED3
void AutoLedTwoThreeControl()
{

  if (MODE_LED_TWO_THREE == MANUAL)
  {
    return;
  }

  if (light_value < BRIGHTNESS_LEVEL_ONE && light_value > BRIGHTNESS_LEVEL_TWO)
  {
    digitalWrite(PIN_LED_TWO, HIGH);
    digitalWrite(PIN_LED_TWO, HIGH);
  }
  else if (light_value < BRIGHTNESS_LEVEL_TWO)
  {
    Serial.println("act!light:2");
    digitalWrite(PIN_LED_TWO, LOW);
    digitalWrite(PIN_LED_THREE, LOW);
  }
  else
  {
    Serial.println("act!light:0");
    digitalWrite(PIN_LED_TWO, HIGH);
    digitalWrite(PIN_LED_THREE, HIGH);
  }
}

// Control the fan
void AutoFanControl()
{
  if (MODE_FAN == MANUAL)
  {
    return;
  }

  if (temperature_value > TEMP_THRES)
  {
    Serial.println("act!temp:1");
    digitalWrite(PIN_FAN, HIGH);
  }
  else
  {
    Serial.println("act!temp:0");
    digitalWrite(PIN_FAN, LOW);
  }
}

// Control the water pump
void AutoWaterPumpControl()
{

  if (MODE_WATER_PUMP == MANUAL)
  {
    return;
  }

  if (soil_moisture_value <= SOIL_MOISTURE_THRES)
  {
    Serial.println("act!soil:0");
    analogWrite(PIN_WATER_PUMP_SPEED, 0);
  }
  else
  {
    Serial.println("act!soil:1");
    digitalWrite(PIN_WATER_PUMP_DIRECTION, LEFT);
    analogWrite(PIN_WATER_PUMP_SPEED, 150);
  }
}

void PumpWater()
{
  if (soil_moisture_value <= SOIL_MOISTURE_THRES && water_level_value == 1)
  {
    digitalWrite(PIN_WATER_PUMP_DIRECTION, LEFT);
    analogWrite(PIN_WATER_PUMP_SPEED, 150);
  }
  else
  {
    analogWrite(PIN_WATER_PUMP_SPEED, 0);
  }
}

void NutrientPumpLoop()
{

  if (water_level_value == 1)
  {
    if (nutrientPumpCounter > 0 && millis() >= nutrientPumpScheduledTime)
    {
      startNutrientPump();
    }

    if (nutrientPumpOn)
    {
      long int currentTime = millis();
      if (currentTime - nutrientPumpStartTime >= nutrientPumpDuration)
      {
        stopNutrientPump();
      }
    }
  }
  else
  {
    stopNutrientPump();
    nutrientPumpCounter = 0;
  }
}

void startNutrientPump()
{
  nutrientPumpOn = true;
  nutrientPumpStartTime = millis();
  nutrientPumpScheduledTime = millis() + 10000;
  nutrientPumpCounter -= 1;

  digitalWrite(PIN_NUTRIENT_PUMP_DIRECTION, LEFT);
  analogWrite(PIN_NUTRIENT_PUMP_SPEED, 150);
}

void stopNutrientPump()
{
  nutrientPumpOn = false;
  analogWrite(PIN_NUTRIENT_PUMP_SPEED, 0);
}
