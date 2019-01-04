import BB8_driver
import cwiid

def main():
	print("Welcome to the Matthew Smith BB-8 Control Progtam. This program will serve to control a Sphero BLE BB-8 with the help of a Wii Remote (Wiimote). Thanks to GitHub user jchadwhite for their excellent Python-Sphero interface.")
	response = input(""Enter your BB-8 UUID? y/n: "
	if(response == "y"):
		addr = input("Enter the UUID of your BB-8: ")
		BB8_driver.setAddress(addr)
	bb8 = BB8_driver.Sphero()
	print("Connecting to BB-8")
	bb8.connect()
	
	rm = cwii.Wiimote()
	
if __name__ == "__main__":
	main()	
