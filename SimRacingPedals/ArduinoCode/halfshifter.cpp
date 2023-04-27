#define LED_PIN1 4
#define HALL_PIN1 A0
#define LED_PIN2 2
#define HALL_PIN2 A1
#define LED_PIN3 7
#define HALL_PIN3 A2

void setup() {
  // put your setup code here, to run once:
  pinMode(LED_PIN1, OUTPUT);
  pinMode(HALL_PIN1, INPUT);
  pinMode(LED_PIN2, OUTPUT);
  pinMode(HALL_PIN2, INPUT);
  pinMode(LED_PIN3, OUTPUT);
  pinMode(HALL_PIN3, INPUT);
  Serial.begin(9600);
}

void loop() {
  // put your main code here, to run repeatedly:
  int val1 = analogRead(HALL_PIN1);
  int val2 = analogRead(HALL_PIN2);
  int val3 = analogRead(HALL_PIN3);
  Serial.println(val1);
  Serial.println(val2);
  Serial.println(val3);
  if ((val1 > 600 || val2 > 600) || val3 > 600){
    if (val1>val2 && val1>val3){
      digitalWrite(LED_PIN1,HIGH);
    }
    else{
      digitalWrite(LED_PIN1,LOW);
    }
    if (val2>val1 && val2>val3){
      digitalWrite(LED_PIN2,HIGH);
    }
    else{
      digitalWrite(LED_PIN2,LOW);
    }  
    if (val3>val1 && val3>val2){
      digitalWrite(LED_PIN3,HIGH);
    }
    else{
      digitalWrite(LED_PIN3,LOW);
    }
  }
  else{
    digitalWrite(LED_PIN1,LOW);
    digitalWrite(LED_PIN2,LOW);
    digitalWrite(LED_PIN3,LOW);
  }
  delay(100);
  // Serial.println("HI");
}