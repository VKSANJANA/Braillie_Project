from machine import Pin, freq, ADC, UART
from time import time
import _thread

freq(133000000)

led = Pin(25, Pin.OUT)
led.on()

battery = ADC(28)
uart = UART(0, baudrate=9600, tx=Pin(0), rx=Pin(1))

power = Pin(21, Pin.IN, Pin.PULL_UP)
pi_zero = Pin(20, Pin.OUT)
fet = Pin(22, Pin.OUT)
sig = Pin(2, Pin.OUT)

fet.on()
pi_zero.on()
sig.off()

status = 0
flag_adc = 0
milestone = [50, 25, 15, 5]

def delay(period):
    start_time = time()
    while time() - start_time < period:
        pass
    

def shut_down():
    global status
    print("shutdown")
    pi_zero.off()   
    delay(90)
    fet.off()
    status = 1
    delay(5)
    
def power_control():
    global status
    global flag_adc
    if flag_adc:
        return
    if power.value():
        delay(0.05)
        if status:
            if not power.value():
                return
            fet.on()
            pi_zero.on()
            status = 0
            print('core2 ' + str(power.value()) + ' ' + str(pi_zero.value()))
    else:
        if not status:
            delay(0.05)
            if power.value():
                return
            print('core2 ')        
            shut_down()
            print('core2 ' + str(power.value()) + ' ' + str(pi_zero.value()))

def core_two():
    while True:
        power_control()

def signal(word):
    sig.on()
    delay(0.5)
    sig.off()
    uart.write(word)
    delay(0.1)

'''
def read_adc():
    global flag_adc
    sig.off()
    while True:
        level = battery.read_u16()
        level_analog = level*3.3/65535
        print(str(level) + ' ' + str(level_analog))
        if level_analog == 50:              # at 50 %
            signal('50\0')
        elif level_analog == 25:
            signal('25\0')
        elif level_analog == 15:
            signal('15\0')
        elif level_analog < 2.7 and not status:
            signal('5\0')
            delay(5)
            flag_adc = 1
            shut_down()
        else:
            flag_adc = 0
        delay(5)
'''

def read_adc():
    global flag_adc
    global milestone
    level = milestone
    while True:
        level = battery.read_u16()
        level_analog = level*3.3/65535
        print(str(level) + ' ' + str(level_analog))
        if not len(level):
            level = milestone
            flag_adc = 1
            shut_down()
        if level_analog <= level[0]:
            signal((str(level[0])+'\0'))
            level.pop(0)
        if flag_adc and level_analog > 10: # above 10 percent
            flag_adc = 0


try:
    _thread.start_new_thread(core_two, ())
    read_adc()
except KeyboardInterrupt:
    _thread.exit()
    pass
