import subprocess
import pyttsx3


engine = pyttsx3.init('espeak', True)
#engine = pyttsx3.init(driverName='flite')

command = f'sudo bluetoothctl connect CB:09:40:38:C1:A4'
subprocess.run(command, shell=True)

voice_id = 'english'
engine.setProperty('voice', voice_id)

engine.setProperty('rate', 170)
engine.setProperty('volume', 0.5)
engine.say('Woah, I can speak')
engine.runAndWait()
