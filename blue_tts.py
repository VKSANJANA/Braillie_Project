import pyttsx3
import bluetooth
import os
import socket

target_name = "BT-163"
target_address = None

nearby_devices = bluetooth.discover_devices()

for bdaddr in nearby_devices:
    print(bdaddr)
    if target_name == bluetooth.lookup_name( bdaddr ):
        target_address = bdaddr
        break

if target_address is not None:
    print ("found target bluetooth device with address ", target_address)
else:
    print ("could not find target bluetooth device nearby")

# pairs device if not paired
#os.system(f"bluetoothctl -- pair {target_address}")

service_matches = bluetooth.find_service(address=target_address)
s = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)

'''
# lists available ports for the device
if len(service_matches) > 0:
    for service in service_matches:
        if service["protocol"] == "RFCOMM":
            print(service["port"])
            #s.connect((target_address, int(service["port"])))
'''

s.connect((target_address, 2))

# delay to allow socket to establish connection
for i in range(500000000):
    pass

#####################################################################

engine = pyttsx3.init('espeak', True)

engine.say('I been running through the jungle; I been running with the wolves to get to you')
engine.runAndWait()

s.close()
