#!usr/bin/env python3

import subprocess
import time
from pathlib import Path
import pyttsx3
import keyboard
import louis

#engine = pyttsx3.init() #object creation

def braille_reader():
	tableList = ["unicode.dis","braille-patterns.cti","en-ueb-g1.ctb"]
	line =  ["abcd"]
	for i in line:
		translation = louis.translateString(tableList,i)
		print(i + "=" + translation + "\n")
	
def detect_drive():
        BLOCK_DEVICE = Path("/dev/sda1")
        MOUNT_POINT = Path("/mnt/usb1")
        MOUNT_COMMAND = ["sudo", "mount", BLOCK_DEVICE, MOUNT_POINT]

        if(BLOCK_DEVICE.exists() and not MOUNT_POINT.is_mount()):
                subprocess.check_call(MOUNT_COMMAND)
                print("Detected")
                return 1
        elif (BLOCK_DEVICE.exists() and MOUNT_POINT.is_mount()):
                print("Detected")
                return 1
        else:
                print("Not detected")
                return 1


while(detect_drive()):
	#engine.say("Pendrive detected")
	#engine.runAndWait()	
	#time.sleep(1)
	#engine.say("Choose 1 for Braille reading or Choose 2 for Audio reading or Choose 3 for both")
	print("Choose 1 for braille reading or choose 2 for audio reading or choose 3 for both")
	var = input()
	time.sleep(2)
	if(var == '1'):
		#engine.say("Braille reader")
		print("Braille reading")
		braille_reader()
		break
	elif(var == '2'):
		#engine.say("Audio reader")
		print("Audio reading")
		break
	elif(var == '3'):
		print("Both")
		break
		#engine.say("Both")	
	else:
		print("Wrong key")
		break
		#engine.say("Wrong key")
	
	
