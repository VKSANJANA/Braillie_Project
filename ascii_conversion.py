import os



output_folder_path = "/home/sanjana/Documents/Braille_Project/translation_dir"



import louis



'''tableList = ["unicode.dis","braille-patterns.cti","en-ueb-g1.ctb","en-ueb-math.ctb"]

for i in line:

	translation = louis.translateString(tableList,i)

	print(i + "=" + translation + "\n") '''

	

        

def convert_to_format(text):

    	for item in text:		

    		binstr = bin(int((ascii(item).replace("\\u28", "")).replace("'", ""),16))

    		reverse = binstr[-1:1:-1]

    		reverse_ = int((reverse + (8 - len(reverse))*"0"),2)

    		print("Reversed = " + bin(reverse_))

    	return reverse_

 







def translation(no_of_pages):

        for i in range(0,no_of_pages):

                f_name = f"Page_{i}.BRL"

                path = os.path.join(output_folder_path,f_name)

                with open(path,'r') as file:

                        for line in file:

                                converted_line = convert_to_format(line)

                                print("Converted line = " + converted_line)

                                print("/n") 

                                

                                

no_of_pages = 1



translation(no_of_pages)



