import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

clk = 19
data_l = 4
data_r = 17
oe_l = 27
oe_r = 22
strobe_l = 5
strobe_r = 6

GPIO.setup(clk, GPIO.OUT)
GPIO.setup(data_l, GPIO.OUT)
GPIO.setup(data_r, GPIO.OUT)
GPIO.setup(oe_l, GPIO.OUT)
GPIO.setup(oe_r, GPIO.OUT)
GPIO.setup(strobe_l, GPIO.OUT)
GPIO.setup(strobe_r, GPIO.OUT)

GPIO.output(data_l, GPIO.LOW)
GPIO.output(data_r, GPIO.LOW)
GPIO.output(strobe_l, GPIO.HIGH)
GPIO.output(strobe_r, GPIO.HIGH)
GPIO.output(oe_l, GPIO.HIGH)
GPIO.output(oe_r, GPIO.HIGH)
GPIO.output(clk, GPIO.LOW)


def shiftOut(data_pin, clock_pin, order, value):
    if order == 'MSBFIRST':
        bit_order = range(7, -1, -1)
    else:
        bit_order = range(8)
    for bit in bit_order:
        GPIO.output(data_pin, (value >> bit) & 1)
        GPIO.output(clock_pin, GPIO.HIGH)
        time.sleep(0.001)
        GPIO.output(clock_pin, GPIO.LOW)
        time.sleep(0.001)


def swap(pos_1, pos_2, data)->int:
    mask = ~((1<<pos_1) | (1<<pos_2))
    temp_1 = data & 1<<pos_1
    temp_2 = data & 1<<pos_2
    diff = pos_1 - pos_2
    data &= mask
    if(diff>0):
        data |= (temp_1>>diff) | (temp_2<<diff)
    else:
        diff = -diff
        data |= (temp_1<<diff) | (temp_2>>diff)
    return data

def correct_data(position, data)->int:
    correction = 0b00000000
    for i in range(3):
        correction |= (1<<position[i])
    return data ^ correction

def map(data)->int:
    map_array = [7, 5, 3, 6, 4, 2, 1, 0]
    data_mapped = 0
    for i in range(8):
      data_mapped |= ((data>>i)&1)<<map_array[i]
    return data_mapped


def cell_write(in_r, in_l):
	    in_r = map(in_r)
	    in_l = map(in_l)
	    in_l = swap(0, 1, in_l)
	    in_l = swap(2, 3, in_l)

	    GPIO.output(strobe_l, GPIO.LOW)
	    shiftOut(data_l, clk, 'LSBFIRST', in_r)
	    shiftOut(data_l, clk, 'LSBFIRST', in_l)
	    GPIO.output(strobe_l, GPIO.HIGH)

	    GPIO.output(strobe_r, GPIO.LOW)
	    shiftOut(data_r, clk, 'LSBFIRST', ~(in_r))
	    shiftOut(data_r, clk, 'LSBFIRST', ~(in_l))
	    GPIO.output(strobe_r, GPIO.HIGH)

	    for i in range(3):
	      time.sleep(0.005)
	      GPIO.output(oe_l, GPIO.LOW)
	      GPIO.output(oe_r, GPIO.LOW)
	      time.sleep(0.015)
	      GPIO.output(oe_l, GPIO.HIGH)
	      GPIO.output(oe_r, GPIO.HIGH)

'''
try:
	i = int(input("value "))
	while i:
	    cell_write(i, i)
	    i = int(input("value "))
finally:
	GPIO.cleanup()
'''
