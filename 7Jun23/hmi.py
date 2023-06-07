import RPi.GPIO as GPIO
from pcf8574 import PCF8574
import time

GPIO.setmode(GPIO.BCM)

GPIO.setup(13, GPIO.IN, pull_up_down=GPIO.PUD_UP)

#define the pcf8574 i2c address
pcf_address = 0x20

#initialize the pcf8574 object
pcf = PCF8574(1, pcf_address)

#debouncing variables
debounce_delay = 0.02
last_state = 0
last_change_time = time.time()

#read input from pcf8574 
def read_input():
	key_pressed = []
	global last_state, last_change_time
	current_state = pcf.port
	last_change_time = time.time()
	while (time.time() - last_change_time) < debounce_delay:
		pass
	last_state = pcf.port
	for i in range(8):
		if(last_state[i]==current_state[i]):
			key_pressed.append(current_state[i]) 
		else:
			print("Not happening")
	return key_pressed


def isr_hmi(pin):
	key_pressed = read_input()
	for i in range(6):
		if not key_pressed[i+2]:
			print("Button "+str(i+1)+" pressed")
			break

GPIO.add_event_detect(13, GPIO.FALLING, callback=isr_hmi)

try:
	while True:
		pass
except KeyboardInterrupt:
	GPIO.cleanup()
