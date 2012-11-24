import unittest
import pca9685pw
import smbus

address = 0b1000011 #address pins [1][A5][A4][A3][A2][A1][A0]
frequency = 600 #hertz 64 recomended for Servos

class TestPCM(unittest.TestCase):

    def test_smbus(self):
        pwm = pca9685pw.Pca9685pw()
        self.assertIsInstance(pwm, pca9685pw.Pca9685pw)
        self.assertTrue(pwm.defaultBus == 0)
        self.assertIsInstance(pwm.bus, smbus.SMBus)

    def test_address(self):
        pwm = pca9685pw.Pca9685pw()
        pwm.defaultAddress = address
        self.assertTrue(pwm.defaultAddress == address)

    def test_reset(self):
        pwm = pca9685pw.Pca9685pw()
        pwm.defaultAddress = address
        pwm.reset()

    def test_setFrequency(self):
        pwm = pca9685pw.Pca9685pw()
        pwm.defaultAddress = address
        pwm.setFrequency(frequency)

    def test_setTimes(self):
        pwm = pca9685pw.Pca9685pw()
        pwm.defaultAddress = address
        pwm.setFrequency(frequency)
        pwm.reset()
        pwm.setTimes(0,000,4030)
        pwm.setTimes(1,4000,4030)
        pwm.setTimes(2,000,4030)

    def test_getTimes(self):
        pwm = pca9685pw.Pca9685pw()
        pwm.defaultAddress = address
        pwm.getTimes(0)
        pwm.getTimes(1)
        pwm.getTimes(2)

    def test_setPercent(self):
        pwm = pca9685pw.Pca9685pw()
        pwm.defaultAddress = address
        pwm.setFrequency(frequency)
        pwm.reset()
        pwm.setPercent(0,99)
        pwm.setPercent(1,99)
        pwm.setPercent(2,99)

    def test_setColourRed(self):
        pwm = pca9685pw.Pca9685pw()
        pwm.defaultAddress = address
        pwm.setFrequency(frequency)
        pwm.reset()
        pwm.setColour(0,255,0,0)
        
    def test_setColourGreen(self):
        pwm = pca9685pw.Pca9685pw()
        pwm.defaultAddress = address
        pwm.setFrequency(frequency)
        pwm.reset()
        pwm.setColour(0,0,255,0)
        
    def test_setColourBlue(self):
        pwm = pca9685pw.Pca9685pw()
        pwm.defaultAddress = address
        pwm.setFrequency(frequency)
        pwm.reset()
        pwm.setColour(0,0,0,255)

    def test_setColourPurple(self):
        pwm = pca9685pw.Pca9685pw()
        pwm.defaultAddress = address
        pwm.setFrequency(frequency)
        pwm.reset()
        pwm.setColour(0,217,27,224)

    def test_setColourYellow(self):
        pwm = pca9685pw.Pca9685pw()
        pwm.defaultAddress = address
        pwm.setFrequency(frequency)
        pwm.reset()
        pwm.setColour(0,232,225,19)

    def test_setColourCyan(self):
        pwm = pca9685pw.Pca9685pw()
        pwm.defaultAddress = address
        pwm.setFrequency(frequency)
        pwm.reset()
        pwm.setColour(0,19,232,221)

if __name__ == '__main__':
    unittest.main()
