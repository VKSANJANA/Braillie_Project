from machine import Pin
from time import sleep

power = Pin(21, Pin.IN)
pi_zero = Pin(20, Pin.OUT)
switch = Pin(22, Pin.OUT)

switch.on()
pi_zero.on()

status = 0

def power_control():
    global status
    if power.value():
        if status:
            switch.on()
            pi_zero.on()
            status = 0
    else:
        pi_zero.off()
        sleep(15)
        switch.off()
        status = 1

while True:
    power_control()
