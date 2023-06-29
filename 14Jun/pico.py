from machine import Pin, freq, ADC, UART
from time import time
import _thread

freq(133000000)

led = Pin(25, Pin.OUT)
led.on()

battery1 = ADC(26)
battery2 = ADC(27)
uart = UART(0, baudrate=9600, tx=Pin(0), rx=Pin(1))

power = Pin(21, Pin.IN, Pin.PULL_UP)
pi_zero = Pin(20, Pin.OUT)
fet = Pin(22, Pin.OUT)

fet.on()
pi_zero.on()

status = 0
flag_adc = 0
charge = [3, 2.8, 2.7, 2.6, 0]
milestone = [50, 25, 15, 5, 0]

def delay(period):
    start_time = time()
    while time() - start_time < period:
        pass
    

def shut_down():
    global status
    print("shutdown")
    signal('2\0')   
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
    pi_zero.on()
    delay(0.5)
    pi_zero.off()
    uart.write(word)
    delay(0.1)

def poll_battery():
    level = battery1.read_u16()
    level_analog1 = level*3.3/65535
    level = battery2.read_u16()
    level_analog2 = level*3.3/65535
    print("Level analog1 = ",level_analog1)
    print("Level analog2 = ",level_analog2)
    if level_analog1 < level_analog2:
        return level_analog1
    else:
        return level_analog2

def read_adc():
    global flag_adc
    global milestone
    global charge
    ch = charge
    level = milestone
    while True:
        level_analog = poll_battery()
        #print(level_analog)
        if len(ch) == 1:
            ch = charge
            level = milestone
            flag_adc = 1
            shut_down()
        if level_analog <= ch[0]:
            signal((str(level[0])+'\0'))
            level = level[1:]
            ch = ch[1:]
        if flag_adc and level_analog > 2.7: # above 10 percent
            flag_adc = 0


try:
    _thread.start_new_thread(core_two, ())
    read_adc()
except KeyboardInterrupt:
    _thread.exit()
    pass
