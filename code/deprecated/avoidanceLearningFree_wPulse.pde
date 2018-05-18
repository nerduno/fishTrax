//Implements the following communication protocol...
//1. Python, program should be started first.  When Android is start it sends cmdHandshake and then waits for cmdHandshake. When it receives the response, it blinks the LEDs twice and turns all the pins OFF.
//2. Then it waits for commands of the form cmd,...,cmd,endcmd. It executes the cmds and returns an endcmd.

//Serial Cmd Byte Values
const int cBaud = 9600;
const char cmd_LED_1_ON = 'A'; 
const char cmd_LED_1_OFF = 'B';
const char cmd_LED_2_ON = 'C';
const char cmd_LED_2_OFF = 'D';
const char cmd_SHOCK_OFF = 'E';
const char cmd_SHOCK_SIDE1 = 'F'; 
const char cmd_SHOCK_SIDE2 = 'G';
const char cmd_PULSESHOCK_SIDE1 = 'H'; 
const char cmd_PULSESHOCK_SIDE2 = 'I';
const char cmd_END = 'M';
const char cmd_FAIL = 'N';
const char cmd_HANDSHAKE = 'Z';

//Pins
const int ledSide1Pin = 13; // this pin powers side1 LED 
const int ledSide2Pin = 12; // this pin powers side2 LED
const int shockOffPin = 10; //see next line
const int shockOnPin = 11; //these two pins control a latching relay turning shock on and off
const int shockSide1Pin = 8; //see next line
const int shockSide2Pin = 9; //these two pins control a latching relay that determines which side is shocked

//State
boolean bHandshake = false;

//Pulsing State (we handle pulsing on the arduino for timing accuracy)
boolean bPulseSide1 = false;
boolean bPulseSide2 = false;
int pulseDuration = 50; //ms
int pulseSpacing = 1000;  //ms start to start
unsigned long lastPulse = 0; //time of last pulse
boolean bPulseHigh = false;

void setup()  { 
  randomSeed(analogRead(0));
  pinMode( ledSide1Pin, OUTPUT);
  pinMode( ledSide2Pin, OUTPUT);
  pinMode( shockOnPin, OUTPUT);
  pinMode( shockOffPin, OUTPUT);
  pinMode( shockSide1Pin, OUTPUT);
  pinMode( shockSide2Pin, OUTPUT); 
  
  digitalWrite( ledSide1Pin, LOW);
  digitalWrite( ledSide2Pin, LOW);
  digitalWrite( shockOnPin, LOW);
  digitalWrite( shockOffPin, LOW);
  digitalWrite( shockSide1Pin, LOW);
  digitalWrite( shockSide2Pin, LOW); 
  
  Serial.begin(9600);
} 

void loop()  { 
  if(bHandshake) {
    // Check for input
    if(Serial.available() > 0)
    {
      //When input in received, keep reading and executing commands until and end command is received.
      int currCmd = -1;
      boolean bSuccess = true;
      while(currCmd != cmd_END) {
        if(Serial.available() > 0) {
          currCmd = Serial.read();
          bSuccess = bSuccess && executeCmd(currCmd);
        }
      }
      
      //When end command is received, respond with command outcome.
      if(bSuccess) {
        Serial.write(cmd_END);
      } else {
        Serial.write(cmd_FAIL);
      }
    }
    
    if (bPulseSide1 || bPulseSide2)
    { 
      handlePulsing();
    }
    
  } else {
    bHandshake = attemptHandshake();
  }
}

boolean attemptHandshake() {
  //Send out a handshake attempt.
  Serial.print(cmd_HANDSHAKE);
  digitalWrite( ledSide1Pin, HIGH);
  delay(100);
  digitalWrite( ledSide1Pin, LOW);
  
  //Check for response
  if(Serial.available() > 0){
    char response = Serial.read();
    if(response == cmd_HANDSHAKE){
      //Successful response, acknowledget and return.
      for(int i = 0; i< 10; i++){
        digitalWrite( ledSide1Pin, HIGH);
        delay(100);
        digitalWrite( ledSide1Pin, LOW);
        delay(100);
      }
      return true;
    } 
  } else {
    delay(1000);
  } 
  return false;
}

boolean executeCmd(int cmd){
  if(cmd == cmd_END) {
    return true;
  } else if(cmd == cmd_LED_1_ON) {
    digitalWrite(ledSide1Pin, HIGH);
  } else if(cmd == cmd_LED_1_OFF) {
    digitalWrite(ledSide1Pin, LOW);
  } else if(cmd == cmd_LED_2_ON) {
    digitalWrite(ledSide2Pin, HIGH);
  } else if(cmd == cmd_LED_2_OFF) {
    digitalWrite(ledSide2Pin, LOW);
  } else if(cmd == cmd_SHOCK_OFF) {
    digitalWrite(shockOffPin, HIGH);
    digitalWrite(shockOnPin, LOW);
    bPulseSide1 = false;
    bPulseSide2 = false;    
  } else if(cmd == cmd_SHOCK_SIDE1) {
    digitalWrite(shockSide1Pin, HIGH);
    digitalWrite(shockSide2Pin, LOW);
    digitalWrite(shockOffPin, LOW);
    digitalWrite(shockOnPin, HIGH);  
    bPulseSide1 = false;
    bPulseSide2 = false;     
  } else if(cmd == cmd_SHOCK_SIDE2) {
    digitalWrite(shockSide1Pin, LOW);
    digitalWrite(shockSide2Pin, HIGH);
    digitalWrite(shockOffPin, LOW);
    digitalWrite(shockOnPin, HIGH);
    bPulseSide1 = false;
    bPulseSide2 = false;  
  } else if(cmd == cmd_PULSESHOCK_SIDE1) {
    bPulseSide1 = true;
    bPulseSide2 = false;     
    digitalWrite(shockSide1Pin, HIGH);
    digitalWrite(shockSide2Pin, LOW);
    digitalWrite(shockOffPin, LOW);
    digitalWrite(shockOnPin, HIGH); 
    lastPulse = millis();
    bPulseHigh = true;
  } else if(cmd == cmd_PULSESHOCK_SIDE2) {
    bPulseSide1 = false;
    bPulseSide2 = true; 
    digitalWrite(shockSide1Pin, LOW);
    digitalWrite(shockSide2Pin, HIGH);
    digitalWrite(shockOffPin, LOW);
    digitalWrite(shockOnPin, HIGH);
    lastPulse = millis();
    bPulseHigh = true;
  } else {
    return false;
  }
  return true;
}

void handlePulsing() {
  if(bPulseHigh && millis() - lastPulse > pulseDuration)
  {
    digitalWrite(shockOffPin, HIGH);
    digitalWrite(shockOnPin, LOW);
    bPulseHigh = false;
  }
  if(millis() - lastPulse > pulseSpacing)
  {
    digitalWrite(shockOffPin, LOW);
    digitalWrite(shockOnPin, HIGH); 
    lastPulse = millis();
    bPulseHigh = true;
  }  
}

