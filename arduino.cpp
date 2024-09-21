int x;
int pin1=12;
int pin2=11;
int pin3=10;
void setup() {
 Serial.begin(9600);
 Serial.setTimeout(1);
 pinMode(pin1,OUTPUT);
 pinMode(pin2,OUTPUT);
 pinMode(pin3,OUTPUT);
 digitalWrite(pin1,HIGH);
 digitalWrite(pin2,HIGH);
 digitalWrite(pin3,HIGH);
 delay(1000);
 digitalWrite(pin1,LOW);
 digitalWrite(pin2,LOW);
 digitalWrite(pin3,LOW);
 }
void loop() {
 while (!Serial.available());
 x = Serial.readString().toInt();
 if(x==1){
  digitalWrite(pin1,HIGH);
 }
 else if(x==2){
  digitalWrite(pin1,LOW);
 }
 else if(x==3){
  digitalWrite(pin2,HIGH);
 }
 else if(x==4){
  digitalWrite(pin2,LOW);
 }
 else if(x==5){
  digitalWrite(pin3,HIGH);
 }
 else if(x==6){
  digitalWrite(pin3,LOW);
 }
}