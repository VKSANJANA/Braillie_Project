import RPi.GPIO as GPIO
from pcf8574 import PCF8574
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(13, GPIO.IN, pull_up_down=GPIO.PUD_UP)

class HMI():

	left = 4
	right = 5
	up = 2
	down = 3
	ok = 6
	back = 7

	def __init__(self):
		pcf_address = 0x20
		self.pcf = PCF8574(1, pcf_address)
		self.key_pressed = 0

	def read_input(self):
	        key_status = []
	        global last_state, last_change_time
	        current_state = self.pcf.port
	        last_change_time = time.time()
	        while (time.time() - last_change_time) < 0.02:
	                pass
	        last_state = self.pcf.port
	        for i in range(8):
	                if(last_state[i]==current_state[i]):
	                        key_status.append(current_state[i])
	                else:
	                        print("Not happening")
	        return key_status

	def isr_hmi(self, pin):
	        key_status = self.read_input()
	        for i in range(6):
	                if not key_status[i+2]:
	                        print("Button "+str(i)+" pressed")
        	                self.key_pressed = key_status[+2]

'''
hmi = HMI()
GPIO.add_event_detect(13, GPIO.FALLING, callback=hmi.isr_hmi, bouncetime=2)

try:
	while True:
		pass
except KeyboardInterrupt:
	GPIO.cleanup()
'''
