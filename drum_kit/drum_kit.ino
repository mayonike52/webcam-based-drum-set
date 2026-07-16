#include <Servo.h>

Servo drum1;
Servo drum2;
Servo drum3;

void setup() {
  Serial.begin(9600);
  drum1.attach(3);  // servo 1 on pin 3
  drum2.attach(5);  // servo 2 on pin 5
  drum3.attach(6);  // servo 3 on pin 6

  // set all servos to starting position
  drum1.write(0);
  drum2.write(0);
  drum3.write(0);
}

void strike(Servo s) {
  s.write(150);   // strike down
  delay(174);     // wait
  s.write(0);    // spring back up
}

void loop() {
  if (Serial.available() > 0) {
    char input = Serial.read();

    if (input == '1') strike(drum1);
    else if (input == '2') strike(drum2);
    else if (input == '3') strike(drum3);
  }
}