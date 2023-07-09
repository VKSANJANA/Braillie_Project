
'''This code iterates over the files in the input_files folder which has the contents
copied from the pendrive and prompts the user to select a pdf file for translation and
 the file choosen will be transalted to BRL format'''

from PyPDF2 import PdfReader
import louis
import os
import RPi.GPIO as GPIO
import time
import multiprocessing
import subprocess
import blu_os as blu
from hmi import HMI
import cell
import parse

a = blu.audio()

hmi = HMI()

'''
GPIO.setmode(GPIO.BCM)
s_dwn = 18
GPIO.setup(s_dwn, GPIO.IN, pull_up_down=GPIO.PUD_UP)
'''
#tables to be used for translation
tableList = ["unicode.dis","braille-patterns.cti","en-ueb-g1.ctb","en-ueb-math.ctb"]

#translate the file selected
def translation_to_brl(file_path):
	# Print each file name
	line_list = ""
	# This below code opens a file and reads a file and converts the text into braillie and
	# writes it to a file that is stored in a translation_dir directory
	with open(file_path,"rb") as f:
		pdf = PdfReader(f)
		no_of_pages = len(pdf.pages)
		if no_of_pages > 0:
			for page_id in range(no_of_pages):
				page_obj = pdf.pages[page_id]
				lines = page_obj.extract_text().splitlines()
				translated = open(parse.output_folder_path+"/"+"Page_"+str(page_id)+".BRL",'w')
				for line in lines:
					translated.write(louis.translateString(tableList,line)+ "\n")
					line_list += line
					line_list += "\n"
				translated.close()
	return no_of_pages, line_list


def convert_to_format(text):
	temp = ((ascii(text).replace("'","")).replace("\\n","")).split("\\u28")
	temp = temp[1:]
	binstr = []
	for i in temp:
		binstr.append(int(i, 16))
	return binstr


def move_to_line(file, line_number):
	file.seek(0)
	current_line = 1
	while current_line < line_number:
		file.readline()
		current_line += 1


def translation(no_of_pages,line_list, tm = False):
	for i in range(0,no_of_pages):
		f_name = f"Page_{i}.BRL"
		if tm:
			f_name = "Time.BRL"
		path = os.path.join(parse.output_folder_path,f_name)
		curr_pos = 1
		with open(path,'r') as file:
			line = file.readline()
			j = 0
			while True:
				flag_new_line = 1
				if not line:
					break
				converted_line = convert_to_format(line)
				flag = 0
				# loop variable
				i = 0
				word = ""
				while i>=0 and i<len(converted_line):
					if flag:
						flag = 0
						i = i+1
						continue
					if converted_line[i] == 32 or converted_line[i] == 60 or converted_line[i] == 16:
						flag = 1
						cell.cell_write(converted_line[i+1], converted_line[i])
						if(line_list[j].isupper()):
							a.say("Capital " + line_list[j])
						else:
							a.say(line_list[j])
						word += line_list[j]
					else:
						cell.cell_write(converted_line[i], 0)
						if converted_line[i]:
							a.say(line_list[j])
							word += line_list[j]
						else:
							a.say(word)
							word = ""
					up = True
					down = True
					back_l = True
					front_r = True
					while back_l and front_r and up and down:
						up = hmi.read_input()[hmi.up]
						down = hmi.read_input()[hmi.down]
						back_l = hmi.read_input()[hmi.left]
						front_r = hmi.read_input()[hmi.right]
					if not front_r:
						i = i+1
						j = j+1
					elif not back_l:
						i = i-1
						if not word == "":
							word = word.rstrip(word[-1])
						if converted_line[i-1] == 32 or converted_line[i] == 60 or converted_line[i] == 16:
							i = i-1
						j = j-1
						if i<0:
							i = 0
						if j<0:
							j = 0
					elif not up:
						curr_pos = curr_pos - 1
						move_to_line(file,curr_pos)
						line = file.readline()
						word = ""
						try:
							line_pos = line_list.rindex('\n', 0, j)
							j = line_list.rindex('\n', 0, (line_pos-1)) + 1
						except ValueError:
							j = 0
						flag_new_line = 0
						break
					elif not down:
						curr_pos = curr_pos +1
						move_to_line(file,curr_pos)
						line = file.readline()
						word = ""
						j = line_list.find('\n', j) + 1
						print(line_list[j])
						flag_new_line = 0
						break
				if flag_new_line:
					curr_pos = curr_pos + 1
					line = file.readline()
					j = j + 1
				if not word == "":
					a.say(word)

#shutdown = f'sudo shutdown'
'''
def initiate_shutdown(pin):
	print("shutdown")
	#subprocess.run(shutdown, shell=True)

GPIO.add_event_detect(18, GPIO.FALLING, callback=initiate_shutdown, bouncetime=60000)
'''

#call functions
def read(file_path):
	#parse.create_directory()
	#file_path = parse.get_file_address()
	num_of_pages,line_list = translation_to_brl(file_path)
	print(line_list)
	translation(num_of_pages,line_list)

'''
try:
	braille_reader()
finally:
	GPIO.cleanup()
'''
