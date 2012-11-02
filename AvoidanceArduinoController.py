# Avoidance Arduino Controller
"""
AA 2012.07.25
Summary:
Python interface to AvoidanceLearningFree Arduino Sketch
"""

import serial
import time
import os
import sys

#Serial Communication Constants (for Arduino)
cBaud = 9600;
cmd_pin13 = 'A';
cmd_pin12 = 'B';
cmd_pin11 = 'C';
cmd_pulse = 'X';
cmd_high = 'Z';
cmd_low = 'Y';


cmd_LED_1_ON = 'F'; 
cmd_LED_1_OFF = 'B';
cmd_LED_2_ON = 'C';
cmd_LED_2_OFF = 'D';
cmd_SHOCK_OFF = 'E';
cmd_SHOCK_SIDE1 = 'J'; 
cmd_SHOCK_SIDE2 = 'G';
cmd_PULSESHOCK_SIDE1 = 'K'; 
cmd_PULSESHOCK_SIDE2 = 'I';

cmd_END = 'R';
cmd_FAIL = 'S';
cmd_HANDSHAKE = 'T';



class AvoidanceArduinoController:

    @staticmethod
    def static_getDefaultPortName():
        if os.name == 'posix':
            return '/dev/ttyACM1'
        elif os.name == 'mac':
            return '/dev//dev/tty.usbmodemfd121'

    def __init__(self, portName=None):
        print 'init'
        self.ser = None
        if not portName:
            portName = AvoidanceArduinoController.static_getDefaultPortName()
        self.portName = portName
        self.connect(portName)

    def __del__(self):
        self.disconnect()

    def connect(self, portName=None):
        """ connects to arduino and returns if connection successful """
        if self.isConnected():
            self.disconnect()
        if portName:
            self.portName = portName

        try:
            self.ser = serial.Serial(port=self.portName, baudrate=cBaud, bytesize=8, parity='N', stopbits=1, timeout=1)
            print self.ser            
			#ser.open()
            #self.ser.flushInput()
            #self.ser.flushOutput()
            for nAttempt in range(10):
                call = self.ser.read()
                if(call == cmd_HANDSHAKE):
                    self.ser.write(cmd_HANDSHAKE)
                    time.sleep(5)
                    self.ser.flushInput()
                    self.ser.flushOutput()
                    if self.sendMessage(cmd_LED_1_OFF):
                        return True
                    else:
                        self.ser.flushInput()
                        self.ser.flushOutput()
                time.sleep(1);
            self.ser = None
            return False
        except:
            print 'Failed to connect to arduino:', sys.exc_info()[0]
            return False

    def disconnect(self):
        if self.isConnected():
            self.ser.close()
        self.ser = None

    def isConnected(self):
        return bool(self.ser) and self.ser.isOpen()

    def sendMessage(self, message):
        if not self.isConnected(): return False
        self.ser.write(message+cmd_END)
        return self.confirmMessageRecv()

	def sendMessage2(self, pinVal, command):
		self.ser.write(pinVal+command+cmd_END)
		return self.confirmMessageRecv()

    def confirmMessageRecv(self):
        startT = time.time();
        while time.time() - startT < .25:
                if(self.ser.inWaiting() > 0):
                        if(self.ser.read() == cmd_END):
                                return True
        return False
