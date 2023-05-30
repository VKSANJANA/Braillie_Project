'''This code iterates over the files in the input_files folder which has the contents
copied from the pendrive and prompts the user to select a pdf file for translation and
 the file choosen will be transalted to BRL format'''

from PyPDF2 import PdfReader
import louis
import os
import RPi.GPIO as GPIO
import time


# Directory
directory = "translation_dir"

# Parent Directory path
parent_dir = "/home/sanjana/Braillie_Project/"

# Path
output_folder_path = os.path.join(parent_dir, directory)

#input folder path
input_folder_path =  '/home/sanjana/Braillie_Project/input_files'

#get a list of files
pdf_files = [file for file in os.listdir(input_folder_path)]

#tables to be used for translation
tableList = ["unicode.dis","braille-patterns.cti","en-ueb-g1.ctb","en-ueb-math.ctb"]

def create_directory():
        if os.path.isdir(output_folder_path):
                pass
        else:
                os.mkdir(output_folder_path)



#translate the file selected
def translation_to_brl():
        # Print each file name
       for file in pdf_files:
                print(file)
                #Audio output : Press <key> to translate the file
                f_var = input("Press 1 to translate the file ")
                if(f_var == '1'):
                        file_path = os.path.join(input_folder_path,file)

        # This below code opens a file and reads a file and converts the text into braillie and
        # writes it to a file that is stored in a translation_dir directory

        with open(file_path,"rb") as f:

                pdf = PdfReader(f)

                no_of_pages = len(pdf.pages)

                if no_of_pages > 0:

                        for page_id in range(no_of_pages):
                                page_obj = pdf.pages[page_id]

                                lines=page_obj.extract_text().splitlines()

                                #print("\n","THIS IS PAGE",page_id ,"\n")

                                #print(lines)

                                translated = open("translation_dir"+"/"+"Page_"+str(page_id)+".BRL",'w')

                                for line in lines:

                                        translated.write(louis.translateString(tableList,line)+ "\n")

                                translated.close()
        return no_of_pages

def convert_to_format(text):
        #binstr = bin(int((ascii(text).replace("\\u28","")).replace("'",""),16))
        temp = ((ascii(text).replace("'","")).replace("\\n","")).split("\\u28")
        temp = temp[1:]
        binstr = []
        for i in temp:
                binstr.append(int(i, 16))
        return binstr

########################################################################################################
GPIO.setmode(GPIO.BCM)

clk = 3
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

def cell_write(inp):
        for i in inp:
            in_r = int(i)
            in_l = int(i)
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
            time.sleep(2)
########################################################################################################

def translation(no_of_pages):
        for i in range(0,no_of_pages):
                f_name = f"Page_{i}.BRL"
                path = os.path.join(output_folder_path,f_name)
                with open(path,'r') as file:
                        for line in file:
                                converted_line = convert_to_format(line)
                                print(converted_line)
                                cell_write(converted_line)


#call functions
create_directory()
num_of_pages = translation_to_brl()
translation(num_of_pages)
GPIO.cleanup()
