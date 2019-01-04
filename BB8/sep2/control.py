import interface
import cwiid
import time
import sys

global working
global time
global acc

def pingHandler(responseStr):
	global working
	print("Connection stable.")
	working = True

def connectWiimote():
	try:
		rmt = cwiid.Wiimote()
		return rmt
	except:
		return None

def handleAcc(responseStr):
	global time
	global acc
	if(len(responseStr) < 24):
		return
	try:
		x = bin(int(responseStr[10:14], 16))[2:]
		if(len(x) < 16): x = "0" + x
		accxk = int(x[1:], 2)
		finx = int(x[0], 2)*32768
		accxk = accxk - finx
		y = bin(int(responseStr[14:18], 16))[2:]
		if(len(y) < 16): y = "0" + y
		accyk = int(y[1:], 2)
		finy = int(y[0], 2)*32768
		accyk = accyk - finy
		z = bin(int(responseStr[18:22], 16))[2:]
		if(len(z) < 16): z = "0" + z
		acczk = int(z[1:], 2)
		finz = int(z[0], 2)*32768
		acczk = acczk - finz
		acc.append([time, float(accxk), float(accyk), float(acczk)])
	except Exception as e:
		rfdf = 1 # dummy command
		
print("Connecting to BB-8.")
working = False
bb8 = interface.Device("EA:FE:40:7E:CA:0C", 0.1)

print("Starting communication thread.")
bb8.begin()

print("Pinging.")
bb8.ping(True, handler = pingHandler)
time.sleep(1)

if(not working):
	print("Stable connection failed.")
	bb8.end()
	bb8.disconnect()
	sys.exit(1)

for i in range(3):
	bb8.set_rgb_led(False, 0, 0, 255, 0)
	time.sleep(0.2)
	bb8.set_rgb_led(False, 0, 255, 0, 0)
	time.sleep(0.2)

bb8.set_rgb_led(False, 0, 0, 0, 0)

rmt = None

while(rmt is None):
	print("Please connect Wii Remote now.")
	rmt = connectWiimote()
	if(rmt is None):
		res = ""
		while(res not in ["y", "Y", "n", "N"]):
			res = str(raw_input("Connection failed. Try again? (y/n) "))
		if(res in ["n", "N"]): 
			bb8.end()
			bb8.disconnect()
			sys.exit(0)	

print("Connection successful.")

rmt.rpt_mode = cwiid.RPT_BTN | cwiid.RPT_ACC

print("Please place the Wiimote horizontally for calibration. Wait until further prompted")
time.sleep(5)
print("Calibrating")
acc0 = rmt.state["acc"]
eq = 0.5*(acc0[0] + acc0[1])
g = acc0[2] - eq
print("Finished calibration with EQ = {} and g = {}".format(eq, g))
print("Entering main control loop.")
going = True
v = 0
h = 0
dv = 5
dh = 40
w = 0
vr = 0
hr = 0
incv = 20
acc = []
time = 0
bb8.set_sensor_handler(handleAcc)
bb8.set_data_streaming(False, 40, 1, 0xE000, 0)
while(going):
	btnr = bin(rmt.state["buttons"])[2:]
	while(len(btnr) < 13): btnr = "0" + btnr
	btn = ""
	for i in range(len(btnr)): btn = btn + btnr[len(btnr)-1-i]
	if(btn[7] == '1'): # home button
		print("Exiting main control loop.")
		going = False
	if(btn[0] == '1'): # 2 button
		print("acc")
		v = v + dv
	if(btn[1] == '1'): # 1 button
		print("dec")
		v = v - dv
	if(btn[2] == '1'): # B button
		print("flip")
		h = (h + 180) % 360
		
	acc = rmt.state["acc"]
	ax = acc[0] - eq
	ay = acc[1] - eq
	az = acc[2] - eq
	if(w < 5): w = w + 1
	if(az < 0.1*g):
		if(ay > 0.3*g):
			if(w == 5):
				h = h - dh
				w = 0
		elif(ay < -0.3*g): 
			if(w == 5):
				h = h + dh
				w = 0
	v = v % 256
	h = h % 360
	if((int(vr/dv) != int(v/dv)) or (hr != h)): 
		if(v == 0):
			bb8.roll(False, int(v), int(h), 0)
		else:
			bb8.roll(False, int(v), int(h), 1)
		vr = v
		hr = h
	
	time.sleep(0.05)
	time = time + 0.05
		
print("Ending communication thread.")
	
bb8.end()

print("Disconnecting BB-8.")
bb8.disconnect()

acc = numpy.array(acc)

pyplot.plot(acc[0], acc[1]/4096.0, label = "X")
pyplot.plot(acc[0], acc[2]/4096.0, label = "Y")
pyplot.plot(acc[0], acc[3]/4096.0, label = "Z")
pyplot.legend()
pyplot.xlabel("Time / s")
pyplot.ylabel("Accelerimeter Readout / g")
pyplot.show()
print("Ending script.")
