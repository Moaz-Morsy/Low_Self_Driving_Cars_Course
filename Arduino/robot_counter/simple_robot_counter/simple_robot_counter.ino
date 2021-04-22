#define A 2
#define B 3
int counter = 0;
void isr(){
  if (digitalRead(B)==LOW){
    counter++;}
  else{
    counter--;}
  }
void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  pinMode(A,INPUT);
  pinMode(B,INPUT);
  attachInterrupt(digitalPinToInterrupt(A), isr, RISING);

}

void loop() {
  // put your main code here, to run repeatedly:
  Serial.println(counter);

}
