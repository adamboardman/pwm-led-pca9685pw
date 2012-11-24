import smbus
import time
import random

class Pca9685pw:

    def __init__(self):
        self.defaultBus = 0
        self.bus = smbus.SMBus(self.defaultBus)
        self.defaultAddress = 0b1000000

        self.pca9685Mode1 = 0x0
        self.pca9685Mode2 = 0x1
        self.pca9685PreScale = 0xfe
        self.pca9685OutDrv = 0x2
        self.pca9685OutDrvOpenDrain = 0
        self.pca9685OutDrvTotemPole = 1

        self.ledBlockSize = 4

        self.led0OnL = 6
        self.led0OnH = 7
        self.led0OffL = 8
        self.led0OffH = 9

        self.ledFull = 0x10 # bit4 used to set full On/Off

        self.ledMaxOn = 4096-1 #0 based counter

    def reset(self):
	self.bus.write_byte_data(self.defaultAddress,self.pca9685Mode1, 0)

    def prescaleFromFrequency(self,freq):
	return int(round((25000000.0/(4096*freq))-1))

    def readByteData(self,register):
        return self.bus.read_byte_data(self.defaultAddress,register)

    def writeByteData(self,register,value):
        self.bus.write_byte_data(self.defaultAddress,register,value)
	
    def setFrequency(self,freq):
        prescalevalue = self.prescaleFromFrequency(freq)
	oldmode = self.readByteData(self.pca9685Mode1)
	newmode = oldmode&0x7f|0x10
	self.writeByteData(self.pca9685Mode1,newmode)
	self.writeByteData(self.pca9685PreScale,prescalevalue)
	self.writeByteData(self.pca9685Mode1,oldmode)
	time.sleep(0.005) #5 miliseconds
	self.writeByteData(self.pca9685Mode1,(oldmode | 0x80)) #set restart bit (causes remembering where was when off)

    def setTimes(self,ledNum,onTime,offTime):
        print ledNum,onTime,offTime
	ledOnL = self.led0OnL + self.ledBlockSize * ledNum
	ledOnH = self.led0OnH + self.ledBlockSize * ledNum
	ledOffL = self.led0OffL + self.ledBlockSize * ledNum
	ledOffH = self.led0OffH + self.ledBlockSize * ledNum
	onTimeL = onTime & 0xff
	onTimeH = onTime >> 8
	offTimeL = offTime & 0xff
	offTimeH = offTime >> 8
	#print ledOnL,ledOnH,ledOffL,ledOffH
	print onTimeL,onTimeH,offTimeL,offTimeH
	self.writeByteData(ledOnL,onTimeL)
	self.writeByteData(ledOnH,onTimeH)
	self.writeByteData(ledOffL,offTimeL)
	self.writeByteData(ledOffH,offTimeH)

    def getTimes(self,ledNum):
	ledOnL = self.led0OnL + self.ledBlockSize * ledNum
	ledOnH = self.led0OnH + self.ledBlockSize * ledNum
	ledOffL = self.led0OffL + self.ledBlockSize * ledNum
	ledOffH = self.led0OffH + self.ledBlockSize * ledNum
	onTimeL = self.readByteData(ledOnL)
	onTimeH = self.readByteData(ledOnH)
	offTimeL = self.readByteData(ledOffL)
	offTimeH = self.readByteData(ledOffH)
	#print ledOnL,ledOnH,ledOffL,ledOffH
	#print onTimeL,onTimeH,offTimeL,offTimeH
	print bin(onTimeL),bin(onTimeH),bin(offTimeL),bin(offTimeH)
	
    def setFullOn(self,ledNum):
        print 'On',ledNum
	ledOnL = self.led0OnL + self.ledBlockSize * ledNum
	ledOnH = self.led0OnH + self.ledBlockSize * ledNum
	ledOffL = self.led0OffL + self.ledBlockSize * ledNum
	ledOffH = self.led0OffH + self.ledBlockSize * ledNum
	self.writeByteData(ledOnL,0)
	self.writeByteData(ledOnH,self.ledFull)
	self.writeByteData(ledOffL,0)
	self.writeByteData(ledOffH,0)

    def setFullOff(self,ledNum):
        print 'Off',ledNum
        ledOnL = self.led0OnL + self.ledBlockSize * ledNum
	ledOnH = self.led0OnH + self.ledBlockSize * ledNum
	ledOffL = self.led0OffL + self.ledBlockSize * ledNum
	ledOffH = self.led0OffH + self.ledBlockSize * ledNum
	self.writeByteData(ledOnL,0)
	self.writeByteData(ledOnH,0)
	self.writeByteData(ledOffL,0)
	self.writeByteData(ledOffH,self.ledFull)
	
    def setPercent(self,ledNum,percentOn):
        print 'Percent',ledNum,percentOn
	timeOn = int((percentOn/100.0)*self.ledMaxOn)
	if timeOn == 0:
            return self.setFullOff(ledNum)
        if timeOn == self.ledMaxOn:
            return self.setFullOn(ledNum)
	maxLeadIn = self.ledMaxOn - timeOn
	start = random.randint(0,maxLeadIn)
	stop = start+timeOn
	self.setTimes(ledNum,start,stop)

    def setColour(self,ledNum,red,green,blue):
        print 'Colour: ',red,green,blue
        self.setPercent(ledNum,(red/255.0*100))
        self.setPercent(ledNum+1,(green/255.0*100))
        self.setPercent(ledNum+2,(blue/255.0*100))
