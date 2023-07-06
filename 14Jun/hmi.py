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
	trigger = 'n'
	long_press = True

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
				
	def long_press(self, pin):
		self.stat = read_input()
		if not stat[self.ok] or not stat[self.back]:
			time_start = time.time()
			while time.time() - time_start < 5:
				pass
			if not read_input()[self.ok]:
				self.trigger = 'r'
			elif not read_input()[self.back]:
				self.trigger = 'a'
			else:
				self.long_press = False
'''
hmi = HMI()
GPIO.add_event_detect(13, GPIO.FALLING, callback=hmi.isr_hmi, bouncetime=2)

try:
	while True:
		pass
except KeyboardInterrupt:
	GPIO.cleanup()
'''
'''
hmi = HMI()
GPIO.add_event_detect(13, GPIO.FALLING, callback=hmi.isr_hmi, bouncetime=2)

ok = True 
back = True
try:
	print('press okay to continue and back to exit')
	while ok and back:
		if not hmi.long_press:
			ok = hmi.stat[hmi.ok]
			back = hmi.stat[hmi.back]
			hmi.long_press = True
		else:
			if hmi.trigger == 'r':
				pass # read time
				hmi.trigger = 'n'
			elif hmi.trigger == 'a':
				pass # read adc
				hmi.trigger = 'n'
			else:
				pass
'''
