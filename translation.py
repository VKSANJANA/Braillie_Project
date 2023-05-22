'''This code iterates over the files in the input_files folder which has the contents
copied from the pendrive and prompts the user to select a pdf file for translation and the file choosen will be transalted to BRL format'''

from PyPDF2 import PdfReader

import louis

import os

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
                f_var = input("Press 1 to translate the file \n")
                if(f_var == 'y'):
                        file_path = os.path.join(input_folder_path,file)
        #This below code opens a file and reads a file and converts the text into braillie and writes it to a file that is stored in a translation_dir directory

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
        binstr = bin(int((ascii(text).replace("\\u28","")).replace("'",""),16))
        return binstr

def translation(no_of_pages):
        for i in range(0,no_of_pages):
                f_name = f"Page_{i}.BRL"
                path = os.path.join(output_folder_path,f_name)
                with open(path,'r') as file:
                        for line in file:
                                converted_line = convert_to_ascii(line)
                                print(converted_line)


#call functions
create_directory()
num_of_pages = translation_to_brl()
translation(num_of_pages)




