from bluepy import btle
import struct
import time
import BB8_driver
import sys
bb8 = BB8_driver.Sphero()

print("Connecting")
bb8.connect()
print("Connected")


bb8.start()
time.sleep(2)
bb8.set_rgb_led(255,0,0,0,False)
time.sleep(1)
bb8.set_rgb_led(0,255,0,0,False)
time.sleep(1)
bb8.set_rgb_led(0,0,255,0,False)
time.sleep(1)
bb8.roll(100, 0, 1, False)
time.sleep(3)
bb8.roll(100, 90, 1, False)
time.sleep(3)
bb8.roll(100, 180, 1, False)
time.sleep(3)
bb8.roll(100, 270, 1, False)
time.sleep(3)
bb8.join()
bb8.disconnect()
sys.exit(1)

