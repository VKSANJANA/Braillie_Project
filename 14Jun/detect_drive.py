#!usr/bin/env python3

import blu_os as blu
import subprocess
import time
import os
from pathlib import Path
from hmi import HMI

hmi = HMI()

a = blu.audio()
a.say("Please insert the pendrive")

BLOCK_DEVICES = [Path("/dev/sda1"),
		 Path("/dev/sdb1"),
		 Path("/dev/sdc1"),
		 Path("/dev/sdd1"),
		 Path("/dev/sde1") ]
MOUNT_POINT = Path("/media/usb")
detect_flag = 0


def detect_pendrive() -> bool:
	#check for mount point
	if(MOUNT_POINT.is_dir()):
		pass
	else:
		os.mkdir('/media/usb')
	DEVICE = None
	#check if the pendrive is plugged in
	for  BLOCK_DEVICE in BLOCK_DEVICES:
		if(BLOCK_DEVICE.exists()):
			DEVICE = BLOCK_DEVICE
		else:
			 continue
	#to mount and print the status
	if DEVICE == None:
		a.say("Pendrive not detected. Press cancel to continue")
		a.say("Or insert pendrive and press OK")
		ok = True
		cancel = True
		while ok and cancel:
			ok = hmi.read_input()[hmi.ok]
			cancel = hmi.read_input()[hmi.back]
		if not ok:
			return detect_pendrive()
		elif not cancel:
			return False
	if(DEVICE.exists() and not MOUNT_POINT.is_mount()):
		MOUNT_COMMAND = ["sudo","mount",DEVICE,MOUNT_POINT]
		subprocess.check_call(MOUNT_COMMAND)
		detect_flag = 1
		a.say("Detected pendrive") 
		print("Detected")
		return True
	elif (DEVICE.exists() and MOUNT_POINT.is_mount()):
		a.say("Detected pendrive")
		print("Detected")
		detect_flag = 1
		return True


#######################################################################
def get_file_size(folder_path):
	total_size = 0
	# Walk through all the directories and files in the given folder
	for dirpath, dirnames, filenames in os.walk(folder_path):
		for filename in filenames:
			file_path = os.path.join(dirpath, filename)
			if os.path.isfile(file_path):
				total_size += os.path.getsize(file_path)
	return total_size


def convert_size(size_bytes):
	if size_bytes == 0:
		return "0B"
	size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
	i = int(math.floor(math.log(size_bytes, 1024)))
	p = math.pow(1024, i)
	s = round(size_bytes / p, 2)
	return f"{s} {size_name[i]}"

#######################################################################

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
		a.say("No pdf or text files found")
		print("No pdf or text files found")
	else:
		#print the file paths
		a.say("Press OK to copy and cancel to skip copy the file:")
		for path in file_paths:
			file = path.split('/')     #converting string into a list to pr$
			name = file[3:]
			a.say(str(name))
			print("Press 1 to copy the file: " + str(name))
			yes = True
			while yes:
				yes = hmi.read_input()[hmi.ok]
				if not hmi.read_input()[hmi.back]:
					break
			if not yes:
				check_folder()
				file_size = get_file_size(des_path) + get_file_size(path)
				if file_size < 1000000:
					copy_files(path,des_path)
				else:
					print("exceeded limit")
					a.say("file exceeds storage limit")

########################################################################

#unmount the pendrive
def unmount():
	a.say("Press OK to remove pendrive and cancel to continue")
	print("Press OK to remove pendrive and cancel to continue")
	UNMOUNT_COMMAND = ["sudo","umount",MOUNT_POINT]

	yes =  True
	while yes:
		yes = hmi.read_input()[hmi.ok]
		if not hmi.read_input()[hmi.back]:
			return
	subprocess.check_call(UNMOUNT_COMMAND)
	a.say("Pendrive ejected succesfully")

## main function
def main_detect():
	if detect_pendrive():
		copy()
		unmount()


main_detect()
