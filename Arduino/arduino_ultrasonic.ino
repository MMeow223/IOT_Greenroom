//Includes the Arduino Stepper Library
#include <Stepper.h>

// --- General setup ---

const int motorPins[] = {2, 3, 4, 5}; // in order: IN1-IN2-IN3-IN4

const int US_echoPins[] = {6, 7, 8};
// const int US_trigPin[] = {9, 10, 11};
const int US_trigPin[] = {9};

int sensorPosition = 0; // Assuming that sensor mount is at botton position at start. [mm]
const int maxHeight = 150; // max height sensor mount can move up. [mm]

const int DistToWall = 22; // The distance to the lid/wall of the enclosure. [mm]
const int DistToWallMarg = 3; // Margin of the reading of the distance to the lid/wall. [mm]

int plantHeight;
bool Measure = false;

// --- Motor setup ---
// Defines the number of steps per rotation
const int stepsPerRevolution = 2038; //from datasheet
const int pulleyDiameter = 24; //[mm]
const int distance = 5; //[mm]

// Creates an instance of stepper class
// Pins entered in sequence IN1-IN3-IN2-IN4 for proper step sequence
Stepper myStepper = Stepper(stepsPerRevolution, motorPins[0], motorPins[2], motorPins[1], motorPins[3]);

void motorCycle(int dist, int speed) {
  const int steps = -stepsPerRevolution/(pulleyDiameter * 3.1415) * dist; // Calculates the amount of steps

  myStepper.setSpeed(speed);
	myStepper.step(steps);
}

// --- Ultra sonic sensor setup ---
int USdistance[] = {0, 0, 0};

void US_scanCycle() {
  float d;

  for(int i = 0; i <= 2; i++) {
    int duration[] = {10000, 10000, 10000};
    for(int j = 0; j <= 4; j++) { // To get accurate reading. Sometimes the duration is not accurate (to long)
      digitalWrite(US_trigPin[0], LOW);
      delayMicroseconds(2);
      digitalWrite(US_trigPin[0], HIGH);
      delayMicroseconds(10);
      digitalWrite(US_trigPin[0], LOW);

      d = pulseIn(US_echoPins[i], HIGH); // Calculates the duration for the signal to "bounce"

      duration[i] = (d < duration[i] ? d : duration[i]); // Takes the shortest duration (sometimes it is way to long)

      delay(100);
    }

    USdistance[i] = (duration[i]*.0343)/2; // calculated distance to object [mm]
  }
  /*
  Serial.print("Distances1:");
  Serial.println(USdistance[0]);
  Serial.print("Distances2:");
  Serial.println(USdistance[1]);
  Serial.print("Distances3:");
  Serial.println(USdistance[2]);
  */
}

int checkHeight(int wallDist, int wallMargin, int us[3]) {
  int wd = wallDist - wallMargin; // Distance to wall with margin

  int hCheck[] = {false, false, false}; 

  // Checks each sensor to see if the array to see if it's anything closer than the wall.
  for(int i = 0; i <= 2; i++) {
    if(us[i] <= wd) {
      hCheck[i] = true;
    } 
  }

  // If any sensor senses before wall it returns "true"
  if(!(hCheck[0] || hCheck[1] || hCheck[2])){
    return false;
  } else {
    return true;
  }
}


void setup() {
  Serial.begin(9600);
  pinMode(US_trigPin[0], OUTPUT);
  //pinMode(US_trigPin[1], OUTPUT);
  //pinMode(US_trigPin[2], OUTPUT);
  pinMode(US_echoPins[0], INPUT);
  pinMode(US_echoPins[1], INPUT);
  pinMode(US_echoPins[2], INPUT);
}

void loop() {
  if (Serial.available()) {
    int command = Serial.parseInt();
      switch (command) {
        case 101:
          Measure = true;
          break;
      }
  }

  if(Measure) {
    if(sensorPosition <= maxHeight) {
      US_scanCycle();

      /*
      Serial.print("Distance: ");
      Serial.println(USdistance[1]);
      Serial.print("Height:");
      Serial.println(sensorPosition);
      Serial.println(checkHeight(DistToWall, DistToWallMarg, USdistance));
      */

      if(checkHeight(DistToWall, DistToWallMarg, USdistance)) {
        plantHeight = sensorPosition;
      }
      motorCycle(distance, 5);
      sensorPosition += distance;
    } else {

      Serial.print("Plant Height: ");
      Serial.println(plantHeight);

      motorCycle(-(sensorPosition), 10);
      sensorPosition = 0;
      plantHeight = 0;
      Measure = false;
    }
  }
}
