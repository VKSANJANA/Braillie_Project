import subprocess
import pyttsx3
from time import time
import cell


class audio():
	def __init__(self):
		#self.engine = pyttsx3.init('espeak', True)
		self.engine = pyttsx3.init()
		#self.engine = pyttsx3.init(driverName='flite')

		self.command = f'sudo bluetoothctl connect CB:09:40:38:C1:A4'

		#subprocess.run(self.command, shell=True, capture_output=True)
		if subprocess.run(self.command, shell=True, capture_output=True).returncode:
			self.flag = 3
			self.device_not_found()

		#self.voice_id = 'english-us'
		#self.engine.setProperty('voice', self.voice_id)
		self.engine.setProperty('rate', 150)
		self.engine.setProperty('volume', 0.3)


	def say(self, text):
		self.engine.say(text)
		self.engine.runAndWait()

	def device_not_found(self):
		if self.flag:
			print("flag loop")
			start_time = time()
			while time()-start_time < 5:
				pass
			if subprocess.run(self.command, shell=True, capture_output=True).returncode:
				self.flag = self.flag - 1
				self.device_not_found()
		else:
			# er on braille cell
			cell.cell_write(23, 17)
			print("dev not found")
			self.flag = 5
			self.device_not_found()

	def __del__(self):
		cell.GPIO.cleanup()

'''
try:
	a = audio()
	#a.say("hello thanks for trying to tune my voice and make it soothing")
except:
	print("Aagthilla")

'''
a = audio()
#a.say('hello hello this is a long sentence')
