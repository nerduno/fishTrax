/*
Implements the following communication protocol...
1. Python, program should be started first.  When Android is start it sends cmdHandshake and then waits for cmdHandshake.
When it receives the response, it blinks the LEDs twice and turns all the pins OFF.
2. Then it waits for commands of the form: #,...,#M.  The first # is the command type, and the remainder are arguments:

COMMANDS:
SET,Pin#,Value,(Arg,Arg): a digital output pin
  If Value is HIGH or LOW, then there are no arguments.
  If Value is PULSE, then the arguments are Pulse Spacing (ms) and Pulse Duration (ms).
AGET,Analog_In_Pin#: return the value of the specified analog in.
*/
  
//Serial Cmd Byte Values
const int cBaud = 9600;

const int cmd_type_SET = 0;
const int cmd_type_AGET = 1;
const int cmd_set_LOW = 0;
const int cmd_set_HIGH = 1;
const int cmd_set_PULSE = 2;

const char cmd_END = 'M';
const char cmd_FAIL = 'N';
const char cmd_HANDSHAKE = 'Z';

//For ardunino uno
//const int numPins = 14;
//For arduino mega
const int numPins = 54;
//const boolean bValidPin[numPins] = {0,0,1,1,1,1,1,1,1,1,1,1,1,1};
//const boolean bValidPin[numPins] = {0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1};
const int communicationPin = 13;
const int cmd_maxFields = 10;

//State
boolean bHandshake = true;

//Current Command Information:
//Command are of the form #,#,..#K with a maximum of five numbers
int fieldIndex = 0;            // the current field being received
int values[cmd_maxFields];     // the fields received so far.

//Pulsing State (option to handle pulsing on the arduino for timing accuracy??)
boolean bValidPin[numPins];
boolean bPulsing[numPins];
unsigned long lastPulse[numPins];
boolean bPulseHigh[numPins];
int pulseDuration[numPins];
int pulseSpacing[numPins];

void setup()  { 
  randomSeed(analogRead(0));
  
  //init valid pins
  bValidPin[0] = 0;
  bValidPin[1] = 0;
  for(int nPin=2; nPin<numPins; nPin++) {
    bValidPin[nPin] = 1;
  }  
  
  //init pin outputs and states
  for(int nPin=0; nPin<numPins; nPin++) {
    if(bValidPin[nPin]) {
      pinMode( nPin, OUTPUT );
      digitalWrite( nPin, LOW );
      bPulsing[nPin] = false;
      lastPulse[nPin] = 0;
      bPulseHigh[nPin] = false;
      pulseSpacing[nPin] = 1000;
      pulseDuration[nPin] = 50;
    }
  }
  
  pinMode( communicationPin, OUTPUT );
  digitalWrite( communicationPin, LOW );
  Serial.begin(9600);
} 

void loop()  { 
  if(bHandshake) {
    // Check for input, if available update the current field information...
    if(Serial.available() > 0)
    {
      char ch = Serial.read();
      if(ch >= '0' && ch <= '9') // is this an ascii digit between 0 and 9?
      {
        // yes, accumulate the value
        values[fieldIndex] = (values[fieldIndex] * 10) + (ch - '0'); 
      }
      else if (ch == ',')  // comma is our separator, so move on to the next field
      {
        if(fieldIndex < cmd_maxFields-1)
          fieldIndex++;   // increment field index
      }
      else if (ch == cmd_END) // if the command is over execute it...
      {
        executeCmd(values, fieldIndex);
        //clear the values for the next command.
        for(int i=0; i <= fieldIndex; i++)
        {
          values[i] = 0; // set the values to zero, ready for the next message
        }
        fieldIndex = 0;  // ready to start over
      }   
    }
    
    handlePulsing();
    
  } 
  /*
  else 
  {
    bHandshake = attemptHandshake();
  }
  */
}

void executeCmd(int* cmdValues, int numValues) {
  boolean bSuccess = true;
  
  //for (int i = 0; i<=numValues; i++) {
  //  Serial.println(values[i]);
  //} 
  int val;
  if (numValues>=0) {
    if ( cmdValues[0] == cmd_type_SET ) {
      if (numValues>=2 && cmdValues[1]>=0 && cmdValues[1]<numPins && bValidPin[cmdValues[1]]) {
        int pin = cmdValues[1];
        if (cmdValues[2] == cmd_set_LOW ) {
          digitalWrite(pin, LOW);
          bPulsing[pin] = false;
        } else if (cmdValues[2] == cmd_set_HIGH ) {        
          digitalWrite(pin, HIGH);
          bPulsing[pin] = false;
          if (numValues>=3) {
            delay(10);
            val = analogRead(cmdValues[3]);
            Serial.println(val);
          }
        } else if (cmdValues[2] == cmd_set_PULSE ) {
          bPulsing[pin] = true;
          if (numValues>=3) {
            pulseSpacing[pin] = cmdValues[3];
          }
          if (numValues>=4) {
            pulseDuration[pin] = cmdValues[4];
          }
          lastPulse[pin] = millis();
          digitalWrite(pin, HIGH);
          bPulseHigh[pin] = true;
          if (numValues>=5) {
              delay(10);
              val = analogRead(cmdValues[5]);
              Serial.println(val);
          }
        }
      } else {
        //Set commands require both a valid pin number and a value
        bSuccess = false;
      }    
    } else if (cmdValues[0] == cmd_type_AGET) {
      if (numValues>=1 && cmdValues[1]>=0 && cmdValues[1]<=5) {
        val =  analogRead(cmdValues[1]);
        Serial.println(val);
      } else {
        bSuccess = false;
      }
    } else {
      bSuccess = false;
    }
  }
  
  if(bSuccess) {
    Serial.write(cmd_END);
  } else {
    Serial.write(cmd_FAIL);
  }
  
}

void handlePulsing() {
  for (int pin = 0; pin < numPins; pin++) {
    if (bPulsing[pin]) {
      if(bPulseHigh[pin] && millis() - lastPulse[pin] > pulseDuration[pin])
      {
        digitalWrite(pin, LOW);
        bPulseHigh[pin] = false;
      }
      if(millis() - lastPulse[pin] > pulseSpacing[pin])
      {
        digitalWrite(pin, HIGH); 
        lastPulse[pin] = millis();
        bPulseHigh[pin] = true;
      }
    }
  }  
}




