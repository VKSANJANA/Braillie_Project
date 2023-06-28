################################## Pi Zero W ########################################
import blu_os as blu
import RPi.GPIO as GPIO
import serial

GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP)

a = blu.audio()
ser = serial.Serial('/dev/serial0', 9600, timeout=1)  # Use the appropriate serial port and baudrate

def isr(channel):
    data = ser.read()  # Read a single byte from the serial port
    word = ''
    y = data.decode()
    while not y == '\0':
        word += y
        data = ser.read()
        y = data.decode()
    print(word)
    a.say('battery is on ' + word + '%')


GPIO.add_event_detect(18, GPIO.FALLING, callback=isr, bouncetime=50)

try:
        while True:
                pass
except KeyboardInterrupt:
        GPIO.cleanup()

#########################################################################################
################################## Pi Pico W ########################################
from machine import Pin, UART
import time

sig = Pin(2, Pin.OUT)
uart = UART(0, baudrate=9600, tx=Pin(0), rx=Pin(1))

sig.off()

while True:
    word = input()
    sig.on()
    time.sleep(0.5)
    sig.off()
    time.sleep(0.5)
    uart.write(word + '\0')  # Send data over UART
