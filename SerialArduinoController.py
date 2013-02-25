# Serial Arduino Controller
"""
AA 2012.07.25
Summary:
Python interface to the arduino sketch named serialPinController.

Command are written as:
#,...,#M
type,arguments,...,cmd_END

SET:
	cmd_TYPE_SET, pin#, [low,high,pulse], (pulseSpacing-ms, pulseDuration-ms): sets a digital output
	where: pulseSpacing-ms, pulseDuration-ms are optional and only used if the value is pulse.
        return cmd_End

        cmd_type_AGET, pin#: reads an analog input...
"""

import serial
import time
import os
import sys
import traceback
import ipdb

#Serial Communication Constants (for Arduino)
cBaud = 9600;
validPins = range(2,54)
cmd_maxFields = 10

#Commands
cmd_type_SET = 0;
cmd_type_AGET = 1; #analog get
cmd_set_LOW = 0;
cmd_set_HIGH = 1;
cmd_set_PULSE = 2;
cmd_END = 'M';
cmd_FAIL = 'N';
cmd_HANDSHAKE = 'Z';

class SerialArduinoController:

    @staticmethod
    def static_getDefaultPortName():
        if os.name == 'posix':
            return '/dev/ttyACM0'
        elif os.name == 'mac':
            return '/dev//dev/tty.usbmodemfd121'

    def __init__(self, portName=None):
        self.ser = None
        if not portName:
            portName = SerialArduinoController.static_getDefaultPortName()
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
            #ipdb.set_trace()
       	    self.ser = serial.Serial(port=self.portName, baudrate=cBaud, bytesize=8, 
                                     parity='N', stopbits=1, timeout=1)
            print self.ser
            time.sleep(1)
            self.ser.flushInput()
            self.ser.flushOutput()
            bSuccess = True
            time.sleep(1)
            for pin in validPins:
                bSuccess = bSuccess and self.pinLow(pin)
                if not bSuccess:
                    #ipdb.set_trace()
                    print 'ERROR: SerialArduinoController failed to connect to the arduino. %d'%pin
                    self.disconnect()
                    return False
            print 'SerialArduinoController is connected to the arduino.'
            return True
        except:
            print 'EXCEPTION: SerialArduinoController failed to connect to arduino.'
            traceback.print_exc()
            self.disconnect()
            return False

    def disconnect(self):
        if self.isConnected():
            self.ser.close()
        self.ser = None

    def isConnected(self):
        return bool(self.ser) and self.ser.isOpen()

    def pinHigh(self,pinNumber): 
        if not self.isConnected(): return False
        if not pinNumber in validPins: print 'Invalid Pin'; return False
        self.ser.write('%d,%d,%d%s'%(cmd_type_SET,pinNumber,cmd_set_HIGH,cmd_END))
        return self.confirmMessageRecv()

    def pinLow(self,pinNumber):
        if not self.isConnected(): return False
        if not pinNumber in validPins: print 'Invalid Pin'; return False
        self.ser.write('%d,%d,%d%s'%(cmd_type_SET,pinNumber,cmd_set_LOW,cmd_END))
        return self.confirmMessageRecv()

    def pinPulse(self,pinNumber, pulsePeriod=1000, pulseDuration=50):
        if not self.isConnected(): return False
        if not pinNumber in validPins: print 'Invalid Pin'; return False
        self.ser.write('%d,%d,%d,%d,%d%s'%(cmd_type_SET,pinNumber,cmd_set_PULSE,pulsePeriod,
                                           pulseDuration,cmd_END))
        print '%d,%d,%d,%d,%d%s'%(cmd_type_SET,pinNumber,cmd_set_PULSE,pulsePeriod,
                                  pulseDuration,cmd_END)
        return self.confirmMessageRecv()	

    def analogRead(self, pinNumber, scale=(0,5)):
        if not self.isConnected(): return None
        if not pinNumber in range(6): print 'Invalid Pin'; return None
        self.ser.write('%d,%d%s'%(cmd_type_AGET,pinNumber,cmd_END))
        """val = self.readValueAndConfirm()
        if not val == None:
            return (val/1023.0)*(scale[1]-scale[0]) + scale[0]
        """
        val = self.ser.readline()
        print val
        bSuccess = self.confirmMessageRecv()
        if bSuccess:
            val = float(val)
            return (val/1023.0)*(scale[1]-scale[0]) + scale[0]
        else:
            return None

    def readValueAndConfirm(self):
        #import ipdb; ipdb.set_trace()
        startT = time.time()
        val = None
        bReachedDecimalPoint = False
        while time.time() - startT < 0.25:
            if(self.ser.inWaiting() > 0):
                r = self.ser.read()
                if r >= '0' and r <= '9' and not bReachedDecimalPoint:
                    if val == None:
                        val = 0
                    val = val*10 + int(r)
                    print r
                    print val
                elif r == '.':
                    bReachedDecimalPoint = True
                    print 'dec'
                elif r == cmd_END:
                    print 'returning', val
                    return val
                elif r == cmd_FAIL:
                    return None
        return None

    def confirmMessageRecv(self):
        startT = time.time();
        while time.time() - startT < .25:
            if(self.ser.inWaiting() > 0):
                r = self.ser.read()
                if(r == cmd_END):
                    return True
                elif(r == cmd_FAIL):
                    return False
        return False
