import os

import math

import subprocess



# Provide the folder path

folder_path = '/home/sanjana/Documents/Braille_Project/input_files'

des_path = '/home/sanjana/Documents/Braille_Project/des_Folder'



def get_file_size(folder_path):

    total_size = 0



    # Walk through all the directories and files in the given folder

    for dirpath, dirnames, filenames in os.walk(folder_path):

        for filename in filenames:

            file_path = os.path.join(dirpath, filename)

            if os.path.isfile(file_path):

                total_size += os.path.getsize(file_path)



    return total_size



# Call the function to get the total size of files in the folder

#total_file_size = get_file_size(folder_path)



#Convert the size to a more readable format

def convert_size(size_bytes):

    if size_bytes == 0:

        return "0B"

    size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")

    i = int(math.floor(math.log(size_bytes, 1024)))

    p = math.pow(1024, i)

    s = round(size_bytes / p, 2)

    return f"{s} {size_name[i]}"
  
  
  # Display the total file size

#print(f"Total file size: {convert_size(total_file_size)}")



def check_folder():

        if(os.path.exists('/home/sanjana/Documents/Braille_Project/des_Folder')):

                pass

        else:

                os.mkdir('/home/sanjana/Documents/Braille_Project/des_Folder')

                print('Folder created')







def copy_files(source_path, destination_path):

        #command to copy files

        COPY_COMMAND = ['cp',source_path,destination_path]

        #execute the command

        try:

        	subprocess.check_call(COPY_COMMAND)

        except subprocess.CalledProcessError as e:

        	print("Error:",e)
          check_folder()



file_paths = os.listdir(folder_path)



if(len(file_paths)==0):

        print("No pdf or text files found")

else:

        #print the file paths

        for path in file_paths:

                #file = path.split('/')     #converting string into a list to pr$

                print("Press 1 to copy the folder")

                print(path)

                var = input()

                if(var == '1'):

           		check_folder()

           		src_path = os.path.join(folder_path,path)

           		file_size = get_file_size(des_path) + get_file_size(src_path)

           		if file_size < 1000000 :

                      		copy_files(src_path,des_path)

                      		print("File copied /n")

           		else:

           			print("Exceeded the limit.Cannot print the file/n")

  

        	

                else:

                        print("No file to copy")


 
