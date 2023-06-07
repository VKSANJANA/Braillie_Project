import RPi.GPIO as GPIO
import time
import subprocess

GPIO.setmode(GPIO.BCM)

GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP)

command = f'sudo shutdown'

def isr_pow(pin):
	print("shutdown")
	subprocess.run(command, shell=True)

GPIO.add_event_detect(18, GPIO.FALLING, callback=isr_pow, bouncetime=3000)

try:
	while True:
		pass
except KeyboardInterrupt:
	GPIO.cleanup()
