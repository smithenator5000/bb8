import bluepy.btle as bt
import time
import struct
import sys
import threading

#------------------------------------------------------
class Delegate(bt.DefaultDelegate):
	def __init__(self):
		bt.DefaultDelegate.__init__(self)
		
	def handleNotification(self, cHandle, data):
		print("Received: {} from {}".format(data.encode("hex"), cHandle))
#------------------------------------------------------
		
dgt = Delegate()

#------------------------------------------------------
S = bt.Scanner()

print("Scanning")

devices = S.scan()

for i in range(len(devices)):
	print("{} {}: {}".format(i, devices[i].getValueText(9), devices[i].addr))

i = input("Which one? ")

#---------------------------------------------------------

print("Connecting")
bb8per = bt.Peripheral(devices[i].addr, addrType = bt.ADDR_TYPE_RANDOM)
bb8per.setDelegate(dgt)

antidos = bb8per.getCharacteristics(uuid = "22bb746f2bbd75542d6f726568705327")[0]
wakecpu = bb8per.getCharacteristics(uuid = "22bb746f2bbf75542d6f726568705327")[0]
txpower = bb8per.getCharacteristics(uuid = "22bb746f2bb275542d6f726568705327")[0]

bb8 = bb8per.getCharacteristics(uuid = "22bb746f2ba175542d6f726568705327")[0]

antidos.write("011i3", withResponse = True)
txpower.write("\x0007", withResponse = True)
wakecpu.write("\x01", withResponse = True)

print("Pinging")

output = [255, 255, 0, 1, 3, 1, 250]
msg = "".join(struct.pack("B", c) for c in output)

print(msg.encode("hex"))

bb8.write(msg, withResponse = True)

bb8per.waitForNotifications(10.0)

output =  [0x02, 0x30, 0x02, 0x05, 0xc8, 0x00, 0x00, 0x01]
chk = ~ sum(output) % 256
output = [0xff, 0xff] + output + [chk]

msg2 = "".join(struct.pack("B", c) for c in output)
print(msg2.encode("hex"))

bb8.write(msg2, withResponse = True)

bb8per.waitForNotifications(10.0)

time.sleep(1000)

bb8per.disconnect()

def end():

	sys.exit(0)
