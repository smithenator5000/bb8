import cwiid
import time
import BB8_driver
import matplotlib.pyplot as pyplot
import numpy
import sys

modes = ["tank"]

print("Please connect the Wiimote now.")
wm = cwiid.Wiimote()
print("Wiimote successfully connected")

wm.rpt_mode = cwiid.RPT_BTN | cwiid.RPT_ACC

bb8 = BB8_driver.Sphero()
a = None
print("Connecting to BB-8")
try:
	bb8.connect()
except:
	print("Connection failed. Escaping script.")
	sys.exit(1)
bb8.ping(True)
print("Connection Successful")

bb8.start()

print("Hold Wiimote in horizontal equillibrium for calibration.")

time.sleep(3)
zero = 0.5*(wm.state["acc"][0] + wm.state["acc"][1])
g = wm.state["acc"][2] - zero

bb8.set_back_led(0, False)

print("Starting contol loop.")

time.sleep(5)

print("pinging")

bb8.ping(response = True)

going = True

bb8.set_stablization(1, False)
bb8.set_rotation_rate(250, False)

heading = 0
ph = 0
v = 0

mode = "tank"

responseStr = None
responseArr = None

def getResponse(data):
	responseStr = data
	responseArr = []
	for i in range(0, len(responseStr) - 2, 2):
		responseArr.append(data[i:(i+2)])
	print(responseArr)
	
def setMode(d):	
	k = index(mode)
	if(d == 1):
		k = (k + 1) % len(mode)
	else:
		k = k - 1
		if(k == -1): k = len(mode) - 1
	mode = modes[k]

while(going):
	acc = numpy.array(wm.state["acc"]) - zero
	button = wm.state["buttons"]
	aX = acc[0]
	aY = acc[1]
	aZ = acc[2]
	if(mode == "tank"):
		if(button == 512): heading = 0 #up
		elif(button == 1024): heading = 90 #right
		elif(button == 256): heading = 180 #down
		elif(button == 2048): heading = 270 #left
		elif(button == 1): v = 255 #2
		elif(button == 2): v = 0 #1
	
		elif(button == 128):
			print("Exiting script.")
			sys.exit(0)
		if(button in [1, 2, 512, 1024, 256, 2048]): #2 OR 1
			bb8.roll(100, ph, 0, False)
			time.sleep(0.5)
			bb8.roll(v, heading, 1, False) 
			ph = heading
	else: 
		print("Unknown mode")
		mode = mode[0]
		
	if(button == 4096): setMode(1)
	elif(button == 16): setMode(-1)
	time.sleep(0.05)

	
bb8.join()
bb8.disconnect()


