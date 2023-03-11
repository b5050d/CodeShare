//This is to try out three potentiometers and then fade an offboard led for each POT, and send Joystick to the PC

// POT1 is on pin A11, and LED1 is on D11
#define LED_PIN1 11
#define POT_PIN1 A11
#define LED_PIN2 6
#define POT_PIN2 A10
#define LED_PIN3 5
#define POT_PIN3 A9

#include <Joystick.h>

//Create Joystick object
Joystick_ Joystick(0x03,JOYSTICK_TYPE_JOYSTICK,0,0);

void setup() {
  pinMode(LED_PIN1, OUTPUT);
  pinMode(POT_PIN1, INPUT);
  pinMode(LED_PIN2, OUTPUT);
  pinMode(POT_PIN2, INPUT);
  pinMode(LED_PIN3, OUTPUT);
  pinMode(POT_PIN3, INPUT);
  //Initialize Joystick Library
  Joystick.begin(false);
  Joystick.setXAxisRange(0,255); // X-axis will be our clutch
  Joystick.setYAxisRange(0,255); // Y-axis will be our Brake
  Joystick.setZAxisRange(0,255); // Rudder-axis will be our Acc
}
void loop() {
  int cval2 = analogRead(POT_PIN3);
  // Serial.println(cval2);
  int cmax = 417;
  int cmin = 5;
  int cval3 = abs(cval2-cmax);
  double cval4 = (double(cval3)/(cmax-cmin));
  int cval5 = int(cval4*255);
  if (cval5>255) {
    cval5=255;
  }
  Serial.println(cval5);
  Joystick.setXAxis(cval5);
  analogWrite(LED_PIN1,cval5);

  int bval2 = analogRead(POT_PIN2);
  // Serial.println(bval2);
  int bmax = 440;
  int bmin = 79;
  int bval3 = abs(bval2-bmax);
  double bval4 = (double(bval3)/(bmax-bmin));
  int bval5 = int(bval4*255);
  if (bval5>255) {
    bval5=255;
  }
  Serial.println(bval5);
  Joystick.setYAxis(bval5);
  analogWrite(LED_PIN2,bval5);

  int aval2 = analogRead(POT_PIN1);
  // Serial.println(aval2);
  int amax = 465;
  int amin = 79;
  int aval3 = abs(aval2-amax);
  double aval4 = (double(aval3)/(amax-amin));
  int aval5 = int(aval4*255);
   if (aval5>255) {
    aval5=255;
  }
  Serial.println(aval5);
  Joystick.setZAxis(aval5);
  analogWrite(LED_PIN3,aval5);

  Joystick.sendState();
  delay(10);
}