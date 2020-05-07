import RPi.GPIO as GPIO
GPIO.setwarnings(False)
import time
from collections import deque

class Encoder(object):
    
    def __init__(self, intPin, aPin, bPin, backward=False, dtHistMaxLen=10, halfRes=True, detectionDirection='rising'):
        # a  b  i  a  b  i
        # 12 16 7 11 13 15
        if halfRes:
            intPin = aPin
        self.intPin = intPin
        self.wavePins = aPin, bPin
        self.prev = (0, 0)
        self.prevTime = time.time()
        self.dtHist = deque()
        self.dtHistMaxLen = dtHistMaxLen
        self.dt = 1
        self.pos = 0
        for pin in intPin, aPin, bPin:
            GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        
        if backward:
            self.reverser = -1
        else:        
            self.reverser = 1
            
        direction = {
            'rising': GPIO.RISING,
            'falling': GPIO.FALLING,
            'both': GPIO.BOTH
            }[detectionDirection.lower()]
                
        GPIO.add_event_detect(intPin, direction, callback=self.interruptCallback)
        
    def __del__(self):
        try:
            GPIO.remove_event_detect(self.intPin)
        except:
            pass
        
    @property
    def dt(self):
        return self._dt
    
    @dt.setter
    def dt(self, dtVal):
        self._dt = dtVal
        self.dtHist.append(dtVal)
        if len(self.dtHist) > self.dtHistMaxLen:
            self.dtHist.popleft()
            
    def smoothedDt(self):
        return sum(self.dtHist) / len(self.dtHist)
            
    def interruptCallback(self, data):
        aNow, bNow = GPIO.input(self.wavePins[0]), GPIO.input(self.wavePins[1])
        if aNow == bNow:
            direc = self.reverser
        else:
            direc = -self.reverser
        self.pos += direc