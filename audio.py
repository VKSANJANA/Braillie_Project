# Import the python text to speech libarary and the PDF REader library

import pyttsx3 

from PyPDF2 import PdfReader

from blu_os import *

# Read the PDF file binary mode
#Pass file code to be added

with open(file_path,"rb") as f:

	pdf=PdfReader(f)

	num_of_pages=len(pdf.pages)  #find the number of pages

	for i in range(num_of_pages):

		page=pdf.pages[i]

		page_content=page.extract_text()

		a.say(page_content)

		

