String incomingbyte;
void setup() {
  Serial.begin(9600);
  pinMode(LED_BUILTIN,OUTPUT);
  }
void loop(){

  if(Serial.available()){
    
    incomingbyte = Serial.readStringUntil('\n');
    if(incomingbyte == "on"){

      digitalWrite(LED_BUILTIN,HIGH);
      Serial.write("Led on");
      }
       if(incomingbyte == "off"){

      digitalWrite(LED_BUILTIN,LOW);
      Serial.write("Led off");
      }
    
    }

  
  }
