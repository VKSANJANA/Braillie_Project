import subprocess
import pyttsx3


class audio():
	def __init__(self):
		self.engine = pyttsx3.init('espeak', True)
		#self.engine = pyttsx3.init(driverName='flite')

		self.command = f'sudo bluetoothctl connect CB:09:40:38:C1:A4'
		subprocess.run(self.command, shell=True)

		self.voice_id = 'english-us'
		self.engine.setProperty('voice', self.voice_id)
		self.engine.setProperty('rate', 170)
		self.engine.setProperty('volume', 0.3)


	def say(self, text):
		self.engine.say(text)
		self.engine.runAndWait()
