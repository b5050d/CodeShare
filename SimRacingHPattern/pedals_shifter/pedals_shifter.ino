//This script is written to control the Pedals and the shifter, and to then send the input to the PC

// Define our Pedal Pins
#define POT_PIN1 A8
#define POT_PIN2 A6
#define POT_PIN3 A11

//Define out Gear Pins
#define GPIN_1 A0
#define GPIN_2 A1
#define GPIN_3 A2
#define GPIN_4 A3
#define GPIN_5 A4
#define GPIN_6 A5

//Define the Kill Switch and the Reverse Switch
#define KILL_SW 14
#define REV_SW 15

// Initialize PC input objects
#include <Joystick.h>
#include <Keyboard.h>

char state = '0';
char last = '0';

//Create Joystick object
Joystick_ Joystick(0x03,JOYSTICK_TYPE_JOYSTICK,0,0);

void setup() {
  pinMode(POT_PIN1, INPUT);
  pinMode(POT_PIN2, INPUT);
  pinMode(POT_PIN3, INPUT);

  pinMode(GPIN_1, INPUT);
  pinMode(GPIN_2, INPUT);
  pinMode(GPIN_3, INPUT);
  pinMode(GPIN_4, INPUT);
  pinMode(GPIN_5, INPUT);
  pinMode(GPIN_6, INPUT);

  pinMode(KILL_SW, INPUT);
  pinMode(REV_SW, INPUT);

  Keyboard.begin();
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
  else if (cval5<5){
    cval5=0;
  }
  // Serial.println(cval5);
  Joystick.setXAxis(cval5);

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
  else if (bval5<5){
    bval5=0;
  }
  // Serial.println(bval5);
  Joystick.setYAxis(bval5);

  int aval2 = analogRead(POT_PIN1);
  // Serial.println(aval2);
  int amax = 464;
  int amin = 66;
  int aval3 = abs(aval2-amax);
  double aval4 = (double(aval3)/(amax-amin));
  int aval5 = int(aval4*255);
   if (aval5>255) {
    aval5=255;
  }
  else if (aval5<4){
    aval5=0;
  }
  // Serial.println(aval5);
  Joystick.setZAxis(aval5);

  Joystick.sendState();

  int val1 = analogRead(GPIN_1);
  int val2 = analogRead(GPIN_2);
  int val3 = analogRead(GPIN_3);
  int val4 = analogRead(GPIN_4);
  int val5 = analogRead(GPIN_5);
  int val6 = analogRead(GPIN_6);

  int kill_val = digitalRead(KILL_SW);
  Serial.println(kill_val);
  int rev_val = digitalRead(REV_SW);
  Serial.println(rev_val);
  Serial.println(val1);
  // Serial.println(val2);
  // Serial.println(val3);
  // Serial.println(val4);
  // Serial.println(val5);
  // Serial.println(val6);
  if (kill_val>0){
    state = 'P';
    Serial.println("Kill Switch");
  }
  else if (rev_val>0){
    state='9';
    Serial.println("Reverse Gear");
  }
  else if (val1>775){
    state='1';
    Serial.println("First Gear");
  }
  else if (val2>775){
    state='2';
    Serial.println("Second Gear");
  }
  else if (val3>775){
    state='3';
    Serial.println("Third Gear");
  }
  else if (val4>775){
    state='4';
    Serial.println("Fourth Gear");
  }
  else if (val5>775){
    state='5';
    Serial.println("Fifth Gear");
  }
  else if (val6>775){
    state='6';
    Serial.println("Sixth Gear");
  }
  else {
    state ='0';
    Serial.println("Neutral Gear");
  }
  // Choose the correct actions
  if (state == last){
  }
  else if (state == 'P'){
    Keyboard.release(last);
  }
  else{
    Keyboard.release(last);
    Keyboard.press(state);
    last=state;
  }
  delay(10);
}