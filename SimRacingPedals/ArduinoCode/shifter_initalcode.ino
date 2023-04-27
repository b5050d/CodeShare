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
  Serial.println(val1);
  if (val1>800){
    digitalWrite(LED_PIN1,HIGH);
  }
  else{
    digitalWrite(LED_PIN1,LOW);
  }
  int val2 = analogRead(HALL_PIN2);
  Serial.println(val2);
  if (val2>795){
    digitalWrite(LED_PIN2,HIGH);
  }
  else{
    digitalWrite(LED_PIN2,LOW);
  }  
  int val3 = analogRead(HALL_PIN3);
  Serial.println(val3);
  if (val3>800){
    digitalWrite(LED_PIN3,HIGH);
  }
  else{
    digitalWrite(LED_PIN3,LOW);
  }

  delay(100);
  // Serial.println("HI");
}