from PyPDF2 import PdfReader

import os



def read_pdf(file_path):

    try:

    	if os.path.getsize(file_path) == 0:

    		raise ValueError("File is empty")

    	with open(file_path, 'rb') as file:

            pdf = PdfReader(file)

            print(f"The PDF has {pdf.getNumPages()} pages.")

    

            

    except FileNotFoundError:

        print("Error: File not found.")

        

    except ValueError as e:

    	print(str(e))

    	

    except EOFError:

        print("Error: Unexpected end of file.")



# Example usage

read_pdf("test.txt")

