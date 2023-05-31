#!usr/bin/env python3

import subprocess
import time
import os
from pathlib import Path

BLOCK_DEVICES = [Path("/dev/sda1"),
		 Path("/dev/sdb1"),
		 Path("/dev/sdc1"),
		 Path("/dev/sdd1"),
		 Path("/dev/sde1") ]
MOUNT_POINT = Path("/media/usb")
detect_flag = 0


def detect_pendrive():
	#check for mount point
	if(MOUNT_POINT.is_dir()):
		pass
	else:
		os.mkdir('/media/usb')
	#check if the pendrive is plugged in
	for  BLOCK_DEVICE in BLOCK_DEVICES:
		if(BLOCK_DEVICE.exists()):
			DEVICE = BLOCK_DEVICE
	#to mount and print the status
	if(DEVICE.exists() and not MOUNT_POINT.is_mount()):
		MOUNT_COMMAND = ["sudo","mount",DEVICE,MOUNT_POINT]
		subprocess.check_call(MOUNT_COMMAND)
		detect_flag = 1 
		print("Detected")
	elif (DEVICE.exists() and MOUNT_POINT.is_mount()):
		print("Detected")
		detect_flag = 1
	else:
		print("Not detected")

#copying the contents of pendrive
########################################################################
folder_path = '/media/usb'
des_path = '/home/sanjana/Braillie_Project/input_files'

def copy_files(source_path, destination_path):
        #command to copy files
        COPY_COMMAND = ['cp',source_path,destination_path]
        #execute the command
        try:
           subprocess.check_call(COPY_COMMAND)
        except subprocess.CalledProcessError as e:
                print("Error:",e)


def check_folder():
        if(os.path.exists('/home/sanjana/Braillie_Project/input_files')):
                pass
        else:
                os.mkdir('/home/sanjana/Braillie_Project/input_files')
                print('Folder created')

#command to find the files with .txt extension
FILES_COMMAND_PDF=['find',folder_path,'-type','f','-name','*.pdf']
FILES_COMMAND_TXT= ['find',folder_path,'-type','f','-name','*.txt']

def copy():
	#list to store the files found
	output_pdf = subprocess.run(FILES_COMMAND_PDF, capture_output = True , text = True)
	output_txt = subprocess.run(FILES_COMMAND_TXT,capture_output = True , text = True)
 	#storing the file paths in a Variable
	file_paths_pdf = output_pdf.stdout.splitlines()
	file_paths_txt = output_txt.stdout.splitlines()
	file_paths = file_paths_pdf + file_paths_txt
	
	if(len(file_paths)==0):
		print("No pdf or text files found")
	else:
		#print the file paths
		for path in file_paths:
			file = path.split('/')     #converting string into a list to pr$
			print("Press 1 to copy the folder")
			print(file[3:])
			var = input()
			if(var == '1'):
				check_folder()
				copy_files(path,des_path)
			else:
				print("No file to copy")
########################################################################

#unmount the pendrive
def unmount():
	print("Press 1 to remove the pendrive or press any key not to proceed")
	var = input()
	UNMOUNT_COMMAND = ["sudo","umount",MOUNT_POINT]
	if(var == '1'):
		subprocess.check_call(UNMOUNT_COMMAND)


## main function
def main_detect():
	detect_pendrive()
	copy()
	unmount()


main_detect()
