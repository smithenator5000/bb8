import interface
import time
import sys
import matplotlib.pyplot as pyplot
import numpy

def pingHandler(responseStr):
	print("Stable.")

def execHandler(responseStr):
	print(responseStr)
	
print("Connecting")
bb8 = interface.Device("EA:FE:40:7E:CA:0C", 0.1)
print("Starting")
bb8.begin()
print("Pinging")
bb8.ping(True, handler = pingHandler)
print("Sleeping for 5 s")
time.sleep(5)
print("Executing")
bb8.execute_ob(True, 1, 0, handler = execHandler)
time.sleep(10)
print("Ending")
bb8.end()
bb8.disconnect()

