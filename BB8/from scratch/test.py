import interface
import time
import sys
import thread
import matplotlib.pyplot as pyplot
import cwiid

global stable

stable = False

def pingHandler(responseStr):
	global stable
	print("Stable connection acheived.")
	stable = True

def rollHandler(responseStr):
	print("On a roll")
	
print("Connecting.")	
bb8 = interface.Device("EA:FE:40:7E:CA:0C")

print("Pinging.")
bb8.ping(True, handler = pingHandler)
bb8.comm.per.waitForNotifications(10.0)

if(not stable): 
	print("Stable connection failed.")
	sys.exit(1)

print("Please connect the Wii Remote now.")
connected = False
while(not connected):
	try:
		rmt = cwiid.Wiimote()
		connected = True
	except: 
		print("Connection failed.")
		retry = ""
		while(retry not in ["y", "n", "Y", "N"]):
			retry = str(raw_input("Try connecting again? (y/n) "))
			if(retry in ["y", "Y"]): print("Try connecting again now.")
			elif(retry in ["n", "N"]):
				print("Exiting script.")
				sys.exit(1)
			else:
				print("Invalid response.")

rmt.rpt_mode = cwiid.RPT_BTN | cwiid.RPT_ACC

print("Hold the Wii Remote steady for a few seconds.")
time.sleep(5)
print("Calibrating")
eq_acc = rmt.state["acc"]
zero = 0.5*(eq_acc[0] + eq_acc[1])
G = eq_acc[2] - zero 
print("Entering main control loop.")

bb8.startListening()

going = True

v = 0
h = 0
dv = 5
dh = 5

while(going):
	btn = rmt.state["buttons"]
	acc = rmt.state["acc"]
	aX = acc[0] - zero
	aY = acc[1] - zero
	aZ = acc[2] - zero

	change = False
	
	#button controls
	if(btn == 128): going = False
	elif(btn == 1): v = (v + dv) % 256
	elif(btn == 2): v = (v - dv)
	if(btn in [1, 2]): change = True
	#acceleration controls
	if(abs(aZ) < 0.1*G):
		if(aY > 0.3*G): h = (h + dh) % 360
		elif(aY < 0.3*G): h = h - dh
		if(abs(aY) > 0.3*G): change = True
		
	#corrections
	if(v < 0): v = 0
	if(h < 0): h = 360 - abs(h)
	
	if(change): 
		print("v: {}; h: {}".format(v, h))
		bb8.roll(int(v), int(h), 1, False)
		
	time.sleep(0.05)

bb8.stopListening()

bb8.disconnect()

sys.exit(0)


