#import the necessary modules required


def work(key_pressed):
	if(left)	
		braille_only()
	if(right)
		audio_only
	if(up)
		braille_audio()

repeat_flag = True

#welcome message
#audio msg
a.say("Welcome to tactilo Have a nice experience")

while(repeat_flag == True)
	a.say("Choose left key to proceed with internal storage and right key to proceed with external storage")

	#key_pressed = left or right

	if(left)
		a.say("Do you want to braille reader or audio reader or both?")
        	#left : braille right : audio up : both
		work(key_pressed)

	if(right)
		detect_drive()
		a.say("Do you want to braille reader or audio reader or both?")
        	#left : braille right : audio up : both
		work(key_pressed)
		a.say("Press okay if you wish to proceed or press back to stop")
		if(key_pressed == okay)	
			repeat_flag = True
		else:
			repeat_flag = False
