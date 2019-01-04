import interface
import sys

def pingHandler(responseStr):
	print("Brilliant!")
bb8 = interface.Device("EA:FE:40:7E:CA:0C")
bb8.ping(True, handler = pingHandler)
bb8.disconnect()
sys.exit(0)
