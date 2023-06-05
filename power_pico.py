from machine import Pin
from time import time


power = Pin(21, Pin.IN)
pi_zero = Pin(20, Pin.OUT)
fet = Pin(22, Pin.OUT)

fet.on()
pi_zero.on()

status = 0

def power_control():
    global status
    if power.value():
        if status:
            fet.on()
            pi_zero.on()
            status = 0
    else:
        if not status:
            pi_zero.off()
            time_then = time()
            while (time() - time_then) < 90:
                pass
            fet.off()
            status = 1

while True:
    power_control()
