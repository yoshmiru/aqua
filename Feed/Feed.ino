/* Sweep
 by BARRAGAN <http://barraganstudio.com>
 This example code is in the public domain.

 modified 8 Nov 2013
 by Scott Fitzgerald
 http://www.arduino.cc/en/Tutorial/Sweep
*/

#include <Servo.h>

Servo myservo;
const int tempInPin = A0;
const int ecOutPin = A1;
const int ecInPin = A2;
const int phOutPin = A3;
const int phInPin = A4;
int sensorValue = 0;

void setup() {
  myservo.attach(8);  // attaches the servo on pin 9 to the servo object
  Serial.begin(9600);
  while (!Serial);
}

void loop() {
  if (Serial.available() > 0) {
    int inByte = Serial.read();
    switch (inByte) {
      case 'S':
        myservo.write(Serial.parseInt());
        break;
      case 'T': {
          // 割り込み禁止
          noInterrupts();
          delay(2);
          sensorValue = analogRead(tempInPin);
          float vo = sensorValue * (5.0 / 1023.0);
          Serial.println(sensorValue); 
          Serial.println(vo); 
          delay(2);
          // 割り込み許可
          interrupts();
        }
        break;
      case 'E':
        // 割り込み禁止
        noInterrupts();
        Serial.println(discharge(200, ecOutPin, ecInPin));
        Serial.println(readEc(100, ecOutPin, ecInPin));
        for (int i=0; i<10; i+=1) {
          int term = pow(2, i);
          float v1 = discharge(200, ecOutPin, ecInPin);
          float v2 = readEc(term, ecOutPin, ecInPin);
          Serial.print(term);
          Serial.print(": ");
          Serial.print(v2);
          Serial.print(" - ");
          Serial.print(v1);
          Serial.print(" = ");
          Serial.print(v2 - v1);
          Serial.print("\n");
//          Serial.println(v2 - v1);
        }
        // 割り込み許可
        interrupts();
        break;
      case 'P':
        // 割り込み禁止
        noInterrupts();
        Serial.println(discharge(30000, phOutPin, phInPin));
        Serial.println(readEc(100, phOutPin, phInPin));
        for (int i=0; i<10; i+=1) {
          int term = pow(2, i);
          float v1 = discharge(30000, phOutPin, phInPin);
          float v2 = readEc(pow(10, i), phOutPin, phInPin);
          Serial.print(term);
          Serial.print(": ");
          Serial.print(v2);
          Serial.print(" - ");
          Serial.print(v1);
          Serial.print(" = ");
          Serial.print(v2 - v1);
          Serial.print("\n");
//          Serial.println(v2 + "-" + v1 + "=" + (v2 - v1));
        }
        // 割り込み許可
        interrupts();
        break;
    }
  }
}

float discharge(int term, int outPin, int inPin) {
  pinMode(outPin, OUTPUT);
  // 放電
  digitalWrite(outPin, LOW);
  delay(term);
//  while ((int) aRead(inPin) > 0) {
//    delay(10);
//  }
  delay(2);
  float v = aRead(inPin);
  delay(2);
  return v;
}

float readEc(int term, int outPin, int inPin) {
  // 充電
  digitalWrite(outPin, HIGH);
  delayMicroseconds(term);
  // 計測
  pinMode(outPin, INPUT);
  delay(2);
  float v = aRead(inPin);
  delay(2);
  // 返す
  return v;
}

float toVoltage(int raw) {
    return raw  * (5.0 / 1023.0);
}

float aRead(int pin) {
    return toVoltage(analogRead(pin));
}

