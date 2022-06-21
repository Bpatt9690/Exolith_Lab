#include <AccelStepper.h>
​
​
//Defining pins
​
  // Motor 1
  int Stepper1Pulse = 5;  // Pulse or step pin
  int Stepper1Direction = 6;  // Direction pin
​
  // Motor 2
  int Stepper2Pulse = 28; // Pulse or step pin
  int Stepper2Direction = 29; // Direction pin
​
  // Motor 3
  int Stepper3Pulse = 36;  // Pulse or step pin
  int Stepper3Direction = 37;  // Direction pin
​
  // Motor 4
  int Stepper4Pulse = 34;  // Pulse or step pin
  int Stepper4Direction = 35;  // Direction pin
​
​
//defining variables
​
  // Motor 1
  int Motor1speed = 0;
  int Motor1position = 0;
​
  // Motor 2
  int Motor2speed = 0;
  int Motor2position = 0;
​
  // Motor 3
  int Motor3speed = 0;
  int Motor3position = 0;
​
  // Motor 4
  int Motor4speed = 0;
  int Motor4position = 0;
​
  // Global
  int speedmin = 0; //pulses per second
  int speedmax = 4000;  //pulses per second
  int positionmax = 200;
​
//Defining AccelStepper Motors
​
  // Motor 1
  AccelStepper step1(1, Stepper1Pulse, Stepper1Direction);
​
  // Motor 2
  AccelStepper step2(1, Stepper2Pulse, Stepper2Direction);
​
  // Motor 3
  AccelStepper step3(1, Stepper3Pulse, Stepper3Direction);
​
  // Motor 4
  AccelStepper step4(1, Stepper4Pulse, Stepper4Direction);
​
​
void setup() {               
 
​
//Stepper Initial Conditions
​
  // Motor 1
  step1.setMaxSpeed (speedmax);  
  step1.setSpeed(0);
  step1.setAcceleration(1000);
  pinMode(Stepper1Pulse, OUTPUT);
  pinMode(Stepper1Direction, OUTPUT);
  digitalWrite(Stepper1Pulse, LOW);
  digitalWrite(Stepper1Direction, LOW);
​
  // Motor 2
  step2.setMaxSpeed (speedmax);  
  step2.setSpeed(0);
  step2.setAcceleration(1000);
  pinMode(Stepper2Pulse, OUTPUT);
  pinMode(Stepper2Direction, OUTPUT);
  digitalWrite(Stepper2Pulse, LOW);
  digitalWrite(Stepper2Direction, LOW);
​
  // Motor 3
  step3.setMaxSpeed (speedmax);  
  step3.setSpeed(0);
  step3.setAcceleration(1000);
  pinMode(Stepper3Pulse, OUTPUT);
  pinMode(Stepper3Direction, OUTPUT);
  digitalWrite(Stepper3Pulse, LOW);
  digitalWrite(Stepper3Direction, LOW);
​
  // Motor 4
  step4.setMaxSpeed (speedmax);  
  step4.setSpeed(0);
  step4.setAcceleration(1000);
  pinMode(Stepper4Pulse, OUTPUT);
  pinMode(Stepper4Direction, OUTPUT);
  digitalWrite(Stepper4Pulse, LOW);
  digitalWrite(Stepper4Direction, LOW);
​
}
​
void loop() {
​
//Stepper Run Conditions
  
  // Motor 1
  step1.setSpeed(250);
  step1.runSpeed();
  //step1.moveTo(200);
  //step1.run();
​
  // Motor 2
  step2.setSpeed(250);
  step2.runSpeed();
  //step2.moveTo(200);
  //step2.run();

  // Motor 3
  step3.setSpeed(250);
  step3.runSpeed();
  //step3.moveTo(200);
  //step3.run();

  // Motor 4
  step4.setSpeed(250);
  step4.runSpeed();
  //step4.moveTo(200);
  //step4.run();

}