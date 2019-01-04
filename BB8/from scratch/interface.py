import bluepy.btle as bluetooth
import struct
import threading
import time
import multiprocessing
import sys

listening = False

COMMAND  = dict(
	CMD_PING = [0x00, 0x01],
	CMD_VERSION = [0x00, 0x02],
	CMD_CONTROL_UART_TX = [0x00, 0x03],
	CMD_SET_BT_NAME = [0x00, 0x10],
	CMD_GET_BT_NAME = [0x00, 0x11],
	CMD_SET_AUTO_RECONNECT = [0x00, 0x12],
	CMD_GET_AUTO_RECONNECT = [0x00, 0x13],
	CMD_GET_PWR_STATE = [0x00, 0x20],
	CMD_SET_PWR_NOTIFY = [0x00, 0x21],
	CMD_SLEEP = [0x00, 0x22],
	GET_POWER_TRIPS = [0x00, 0x23],
	SET_POWER_TRIPS = [0x00, 0x24],
	SET_INACTIVE_TIMER = [0x00, 0x25],
	CMD_GOTO_BL = [0x00, 0x30],
	CMD_RUN_L1_DIAGS = [0x00, 0x40],
	CMD_RUN_L2_DIAGS = [0x00, 0x41],
	CMD_CLEAR_COUNTERS = [0x00, 0x42],
	CMD_ASSIGN_TIME = [0x00, 0x50],
	CMD_POLL_TIMES = [0x00, 0x51],
	
	BEGIN_REFLASH = [0x01, 0x02],
	HERE_IS_PAGE = [0x01, 0x03],
	LEAVE_BOOTLOADER = [0x01, 0x04],
	IS_PAGE_BLANK = [0x01, 0x05],
	CMD_ERASE_USER_CONFIG = [0x01, 0x06],
	
	CMD_SET_CAL = [0x02, 0x01],
	CMD_SET_STABILIZ = [0x02, 0x02],
	CMD_SET_ROTATION_RATE = [0x02, 0x03],
	CMD_SET_CREATION_DATE = [0x02, 0x04],
	CMD_REENABLE_DEMO = [0x02, 0x06],
	CMD_GET_CHASSIS_ID = [0x02, 0x07],
	CMD_SET_CHASSIS_ID = [0x02, 0x08],
	CMD_SELF_LEVEL = [0x02, 0x09],
	CMD_SET_VDL = [0x02, 0x0A],
	CMD_SET_DATA_STREAMING = [0x02, 0x11],
	CMD_SET_COLLISION_DET = [0x02, 0x12],
	CMD_LOCATOR = [0x02, 0x13],
	CMD_SET_ACCELERO = [0x02, 0x14],
	CMD_READ_LOCATOR = [0x02, 0x15],
	CMD_SET_RGB_LED = [0x02, 0x20],
	CMD_SET_BACK_LED = [0x02, 0x21],
	CMD_GET_RBG_LED = [0x02, 0x22],
	CMD_ROLL = [0x02, 0x30],
	CMD_BOOST = [0x02, 0x31],
	CMD_MOVE = [0x02, 0x32],
	CMD_SET_RAW_MOTORS = [0x02, 0x33],
	CMD_SET_MOTION_TO = [0x02, 0x34],
	CMD_SET_OPTIONS_FLAG = [0x02, 0x35],
	CMD_GET_OPTIONS_FLAG = [0x02, 0x36],
	CMD_SET_TEMP_OPTIONS_FLAG = [0x02, 0x37],
	CMD_GET_TEMP_OPTIONS_FLAG = [0x02, 0x38],
	CMD_GET_CONFIG_BLK = [0x02, 0x40],
	CMD_SET_SSB_PARAMS = [0x02, 0x41],
	CMD_SET_DEVICE_MODE = [0x02, 0x42],
	CMD_SET_CFG_BLOCK = [0x02, 0x43],
	CMD_GET_DEVICE_MODE = [0x02, 0x44],
	CMD_GET_SSB = [0x02, 0x46],
	CMD_SET_SSB = [0x02, 0x47],
	CMD_SSB_REFILL = [0x02, 0x48],
	CMD_SSD_BUY = [0x02, 0x49],
	CMD_SSB_USE_CONSUMEABLE = [0x02, 0x4A],
	CMD_SSB_GRANT_CORES = [0x02, 0x4B],
	CMD_SSB_ADD_XP = [0x02, 0x4C],
	CMD_SSB_LEVEL_UP_ATTR = [0x02, 0x4D],
	CMD_GET_PW_SEED = [0x02, 0x4E],
	CMD_SSB_ENABLE_ASYNC = [0x02, 0x4F],
	CMD_RUN_MACRO = [0x02, 0x50],
	CMD_SAVE_TEMP_MACRO = [0x02, 0x51],
	CMD_SAVE_MACRO = [0x02, 0x52],
	CMD_INIT_MACRO_EXECUTIVE = [0x02, 0x54],
	CMD_ABORT_MACRO = [0x00, 0x55],
	CMD_MACRO_STATUS = [0x00, 0x56],
	CMD_SET_MACRO_PARAM = [0x00, 0x57],
	CMD_APPEND_TEMO_MACRO_CHUNK = [0x00, 0x58],
	CMD_ERASE_ORBBAS = [0x00, 0x60],
	CMD_APPEND_FRAG = [0x00, 0x61],
	CMD_EXEC_ORBBAS = [0x00, 0x62],
	CMD_ABORT_ORBBAS = [0x00, 0x63],
	CMD_ANSWER_INPUT = [0x00, 0x64],
	CMD_COMMIT_TO_FLASH = [0x00, 0x65])

ASYNC = dict(
	POWER = 0x01,
	DIAGNOSTICS = 0x02,
	SENSE = 0x03,
	CONTENTS = 0x04,
	PRESLEEP = 0X05,
	MARKERS = 0x06,
	COLLISION = 0x07,
	OBPRINT = 0x08,
	OBERRASC = 0x09,
	OBERRBIN = 0x0a,
	SELFLEVEL = 0x0b,
	GYROLIM = 0x0c,
	SOUL = 0x0d,
	LEVELUP = 0x0e,
	SHIELD = 0x0f,
	XP = 0x10,
	BOOST = 0x11)	
	
MRSC  = dict(
	ORBOTIX_RSP_CODE_OK = 0x00,
	ORBOTIX_RSP_CODE_EGEN = 0x01,
	ORBOTIX_RSP_CODE_ECHKSUM = 0x02,
	ORBOTIX_RSP_CODE_EFRAG = 0x03,
	ORBOTIX_RSP_CODE_EBAD_CMD = 0x04,
	ORBOTIX_RSP_CODE_EUNSUPP = 0x05,
	ORBOTIX_RSP_CODE_EBAD_MSG = 0x06,
	ORBOTIX_RSP_CODE_EPARAM = 0x07,
	ORBOTIX_RSP_CODE_EEXEC = 0x08,
	ORBOTIX_RSP_CODE_EBAD_DID = 0x09,
	ORBOTIX_RSP_CODE_MEM_BUSY = 0x0A,
	ORBOTIX_RSP_CODE_BAD_PASSWORD = 0x0B,
	ORBOTIX_RSP_CODE_POWER_NOGOOD = 0x31,
	ORBOTIX_RSP_CODE_PAGE_ILLEGAL = 0x32,
	ORBOTIX_RSP_CODE_FLASH_FAIL = 0x33,
	ORBOTIX_RSP_CODE_MA_CORRUPT = 0x34,
	ORBOTIX_RSP_CODE_MSG_TIMEOUT = 0x35)

class Communicator(bluetooth.DefaultDelegate):
	def dummy(responseStr):
		print("This is a dummy")
	posts  = []
	address  = None
	seq  = 1
	per  = None
	antidos  = None
	wakecpu  = None
	txpower  = None
	main  = None
	handler = []
	handled = []
	asynchandled = []
	asynchandler = []
	curSeq = 1
	def __init__(self, address):
		self.address  = address
		self.per  = bluetooth.Peripheral(self.address, addrType = bluetooth.ADDR_TYPE_RANDOM)
		self.per.setDelegate(self)
		self.antidos = self.per.getCharacteristics(uuid = "22bb746f2bbd75542d6f726568705327")[0]
		self.wakecpu = self.per.getCharacteristics(uuid = "22bb746f2bbf75542d6f726568705327")[0]
		self.txpower = self.per.getCharacteristics(uuid = "22bb746f2bb275542d6f726568705327")[0]
		self.main = self.per.getCharacteristics(uuid = "22bb746f2ba175542d6f726568705327")[0]
		
		self.antidos.write("011i3", withResponse = True)
		self.txpower.write("\x0007", withResponse = True)
		self.wakecpu.write("\x01", withResponse = True)
		
		

	
	def send(self, response, command, params, handler):
	
		if(response): output  = COMMAND[command] + [self.seq, len(params) + 1] + params
		
		else: output  = COMMAND[command] + [0, len(params) + 1] + params
		
		chksum  = ~ sum(output) % 256
		output  = output + [chksum]
		
		if(response): output  = [0xff, 0xff] + output
		else: output  = [0xff, 0xfe] + output
		
		msg =  "".join(struct.pack("B", x) for x in output)
		
		print("Sending: {}".format(msg.encode("hex")))
		
		self.main.write(msg, withResponse  = True)
		#print(self.seq)
		self.seq = self.seq + 1
		self.currSeq = self.seq - 1
		if(self.seq > 0xff): 
			self.seq = 1
		if(handler is not None):
			if(self.currSeq not in self.handled): 
				self.handled.append(self.currSeq)
				self.handler.append(handler)
			else:
				self.handler[self.handled.index(self.currSeq)] = handler

	
	def addAsyncHandler(self, asyncId, func):
		self.asynchandled.append(ASYNC[asyncId])
		self.asynchandler.append(func)
		
	def handleNotification(self, cHandle, data):
		
		#print("hmm")
		
		responseStr = data.encode("hex")
		
		if("ff" not in responseStr): 
			#print("oof1") 
			return
				
		
		print("Received: {} from {}".format(responseStr, cHandle))
		
		while(responseStr[0:2] != "ff"): responseStr = responseStr[1:]
		
		if(len(responseStr) < 12): 
			#print("oof2") 
			return
							
		print("Processing: {} from {}".format(responseStr, cHandle))
		
		if(responseStr[2:4] == "ff"):
			k = int(responseStr[6:8], 16)
			if(k in self.handled): self.handler[self.handled.index(k)](responseStr)
			
		elif(responseStr[2:4] == "fe"):
			k = int(responseStr[4:6], 16)
			if(k in self.asynchandled): self.asynchandler[self.asynchandled.index(k)](responseStr)
			
	
	def split(self, num, units):
		num = hex(num)[2:]
		while(len(num) < 2*units): num = "0" + num
		res = []
		for i in range(units):
			b = int(num[2*i:2*(i + 1)], 16)
			res.append(b)
		return res
	
	
class Device() :
	listening = False
	comm  = None
	listener = None
	def __init__(self, address):
		self.comm  = Communicator(address)
	
	def ping(self, response, handler = None):
		self.comm.send(response, "CMD_PING", [], handler)
		
	def roll(self, vel, heading, mode, response, handler = None):
		headingSplit = self.comm.split(heading, 2)
		self.comm.send(response, "CMD_ROLL", [vel] + headingSplit + [mode], handler)
		
	def set_rgb_led(self, red, green, blue, custom, response, handler = None):
		self.comm.send(response, "CMD_SET_RGB_LED", [red, green, blue, custom], handler)
		
	def boost(self, state, response, handler = None):
		self.comm.send(response, "CMD_BOOST", [state], handler)
		
	def set_data_streaming(self, N, M, MASK, COUNT, response, MASK2 = None, handler = None):
		N = self.comm.split(N, 2)
		M = self.comm.split(M, 2)
		MASK = self.comm.split(MASK, 4)
 		data = N + M + MASK + [COUNT]
 		
 		if(MASK2 is not None): 
 			MASK2 = self.comm.split(MASK2, 4)
 			data = data + MASK2   
 		
		self.comm.send(response, "CMD_SET_DATA_STREAMING", data, handler)

	
	def startListening(self):
		self.listener = Listener(self)
		self.listener.start()
		self.listening = True
	
	def stopListening(self):
		self.listener.stop()
		self.listener.join()
		self.listening = False
		
	def disconnect(self):
		self.comm.per.disconnect()
		
		
		
	
class Listener(threading.Thread):
	t0 = None
	period = None
	dev = None
	stop_request = None
	
	def __init__(self, dev):
		threading.Thread.__init__(self)
		self.dev = dev
		self.stop_request = threading.Event()
	
	def run(self):
		while(not self.stop_request.isSet()):
			self.read()
	
	def read(self):
		try:
			self.dev.comm.per.waitForNotifications(1)
		except Exception as e:
			print(e) 
			sys.exit(1)
	
	def stop(self):
		self.stop_request.set()
			
	
			
