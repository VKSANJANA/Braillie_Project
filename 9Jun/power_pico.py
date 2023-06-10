from machine import Pin, freq, ADC
from time import time
import _thread

freq(133000000)

led = Pin(25, Pin.OUT)
led.on()

battery = ADC(28)

power = Pin(21, Pin.IN, Pin.PULL_UP)
pi_zero = Pin(20, Pin.OUT)
fet = Pin(22, Pin.OUT)

fet.on()
pi_zero.on()

status = 0

def delay(period):
    start_time = time()
    while time() - start_time < period:
        pass
    

def power_control():
    global status
    if power.value():
        delay(0.05)
        if not power.value():
            return
        if status:
            fet.on()
            pi_zero.on()
            status = 0
            print(str(power.value()) + ' ' + str(pi_zero.value()))
    else:
        if not status:
            delay(0.05)
            if power.value():
                return
            pi_zero.off()
            print(str(power.value()) + ' ' + str(pi_zero.value()))
            delay(90)
            fet.off()
            status = 1
            print("done")
            delay(5)

def core_two():
    while True:
        power_control()

def read_adc():
    while True:
        print(battery.read_u16())
        delay(1)

try:
    _thread.start_new_thread(core_two, ())
    read_adc()
except KeyboardInterrupt:
    _thread.exit()