#include <Arduino.h>
#include <Servo.h>  

Servo servo;
int numPixels = 16;
const int buttonPin = 2;
int buttonState = 0;
int openstate = 0; //0 means closed, 1 means open
void setup() {

  Serial.begin(115200);
  Serial.print("connecting servo");
  servo.attach(0);
  Serial.print("connecting pin");
  pinMode(buttonPin, INPUT);
  //on -> servo.write(180);
  //off ->servo.write(0);
  delay(500);
 
}
void loop(){
  //https://www.arduino.cc/en/Tutorial/BuiltInExamples/Button
  // read the state of the pushbutton value:
  buttonState = digitalRead(buttonPin);
  Serial.print(buttonState);

  // check if the pushbutton is pressed. If it is, the buttonState is HIGH:
  if (buttonState == LOW) {
    if(openstate == 0){
      Serial.print("turning on");
      openstate = 1;
      servo.write(180);  
      delay(400);  
    }else{
      Serial.print("turning off");
      openstate = 0;
      servo.write(135);  
      delay(400);  
    }
  }
    
  delay(200);
}
