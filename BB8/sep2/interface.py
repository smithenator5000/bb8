import bluepy.btle as bluetooth
import threading
import struct

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
	CMD_GET_RGB_LED = [0x02, 0x22],
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
	CMD_ABORT_MACRO = [0x02, 0x55],
	CMD_MACRO_STATUS = [0x02, 0x56],
	CMD_SET_MACRO_PARAM = [0x02, 0x57],
	CMD_APPEND_TEMO_MACRO_CHUNK = [0x02, 0x58],
	CMD_ERASE_ORBBAS = [0x02, 0x60],
	CMD_APPEND_FRAG = [0x02, 0x61],
	CMD_EXEC_ORBBAS = [0x02, 0x62],
	CMD_ABORT_ORBBAS = [0x02, 0x63],
	CMD_ANSWER_INPUT = [0x02, 0x64],
	CMD_COMMIT_TO_FLASH = [0x02, 0x65])

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

class Comm(bluetooth.DefaultDelegate, threading.Thread): #class dealing with sending and receiving Sphero commands
	device = None
	per = None
	msg = []
	handle = []
	async = []
	end = None
	address = None
	antidos = None
	wakecpu = None
	txpower = None
	main = None
	refresh = None
	pending = None
	def __init__(self, device, refresh):
		threading.Thread.__init__(self)
		self.device = device
		self.address  = device.address
		self.per  = bluetooth.Peripheral(self.address, addrType = bluetooth.ADDR_TYPE_RANDOM)
		self.per.setDelegate(self)
		
		self.antidos = self.per.getCharacteristics(uuid = "22bb746f2bbd75542d6f726568705327")[0]
		self.wakecpu = self.per.getCharacteristics(uuid = "22bb746f2bbf75542d6f726568705327")[0]
		self.txpower = self.per.getCharacteristics(uuid = "22bb746f2bb275542d6f726568705327")[0]
		self.main = self.per.getCharacteristics(uuid = "22bb746f2ba175542d6f726568705327")[0]
		self.notify = self.per.getCharacteristics(uuid = "22bb746f2ba675542d6f726568705327")[0]
		
		self.antidos.write("011i3", withResponse = True)
		self.txpower.write("\x0007", withResponse = True)
		self.wakecpu.write("\x01", withResponse = True)
		
		self.end = threading.Event()
		self.refresh = refresh
		self.pending = False
	
	def addMessage(self, msgk, handler):
		self.msg.append([msgk.seq, msgk])
		if(handler is not None): self.handle.append([msgk.seq, handler])
		else: self.handle.append([msgk.seq, self.dummy])
	
	def dummy(self, x):
		i = 1
	
	def addRegime(self, asyncID, handler):
		self.async.append([ASYNC[asyncID], handler])
		
	def send(self):
		if(len(self.msg) == 0): return
		msgk = self.msg[0][1]
		#print("Sending {}".format(msgk.construct().encode("hex")))
		self.main.write(msgk.construct(), withResponse = msgk.response)
		if(not msgk.response): self.msg = self.msg[1:][:]
		
	def run(self):
		while(not self.end.isSet()):
			self.send()
			self.per.waitForNotifications(self.refresh)
	
	def handleNotification(self, cHandle, data):
		responseStr = data.encode("hex")
		#print(responseStr)
		if("ff" not in responseStr): return
		while(responseStr[0:2] != "ff"): responseStr = responseStr[1:]
		if(len(responseStr) < 12): return
		if(responseStr[2:4] not in ["ff", "fe"]): return
		if(responseStr[2:4] == "ff"):
			seq = int(responseStr[6:8], 16)
			try:
				a = self.msg[:][0].index(seq)
				self.msg = self.msg[0:a][:] + self.msg[(a+1):][:]
			except: print("Ah, well")
			if(len(self.handle) > 0):
				if(seq in self.handle[:][0]):
					k = self.handle[:][0].index(seq)
					self.handle[k][1](responseStr)
					self.handle = self.handle[0:k][:] + self.handle[(k+1):][:]
					
			
		elif(responseStr[2:4] == "fe"):
			j = int(responseStr[4:6], 16)
			if(len(self.async) > 0):
				if(j in self.async[:][0]):
					k = self.async[:][0].index(j)
					self.async[k][1](responseStr)
	
class Device: #class dealing with user control of Sphero
	adress = None
	comm = None
	seq = None
	def __init__(self, address, refresh):
		self.address = address
		self.comm = Comm(self, refresh)
		self.seq = 1
	
	def inc_seq(self):
		self.seq = self.seq + 1
		if(self.seq > 0xff): self.seq = 1
		
	def ping(self, response, handler = None):
		msg = Message(response, "CMD_PING", self.seq, [])
		self.comm.addMessage(msg, handler)
		self.inc_seq()
	
	def set_rgb_led(self, response, red, green, blue, custom, handler = None):
		msg = Message(response, "CMD_SET_RGB_LED", self.seq, [red, green, blue, custom])
		self.comm.addMessage(msg, handler)
		self.inc_seq()
		
	def get_rgb_led(self, response, handler = None):
		msg = Message(response, "CMD_GET_RGB_LED", self.seq, [])
		self.comm.addMessage(msg, handler)
		self.inc_seq()
	
	def roll(self, response, speed, heading, mode, handler = None):
		heading = self.split(heading, 2)
		msg = Message(response, "CMD_ROLL", self.seq, [speed] + heading + [mode])
		self.comm.addMessage(msg, handler)
		self.inc_seq()
		
	def set_data_streaming(self, response, N, M, MASK, COUNT, MASK2 = None, handler = None):
		N = self.split(N, 2)
		M = self.split(M, 2)
		MASK = self.split(MASK, 4)
		data = N + M + MASK + [COUNT]
		if(MASK2 is not None):
			MASK2 = self.split(MASK2, 4)
			data = data + MASK2
		msg = Message(response, "CMD_SET_DATA_STREAMING", self.seq, data)
		self.comm.addMessage(msg, handler)
		self.inc_seq()
	
	def execute_ob(self, response, area, start, handler = None):
		start = self.split(start, 2)
		msg = Message(response, "CMD_EXEC_ORBBAS", self.seq, [area] + start)
		print(msg.construct().encode("hex"))
		self.comm.addMessage(msg, handler)
		self.inc_seq()
		
	def set_sensor_handler(self, handler):
		self.comm.addRegime("SENSE", handler)
			
	def begin(self): #begins comm thread
		self.comm.start()
	
	def end(self): #ends comm thread
		self.comm.end.set()
		self.comm.join()
		
	def disconnect(self):
		self.comm.per.disconnect()
		
	def split(self, num, units):
		num = hex(num)[2:]
		while(len(num) < 2*units): num = "0" + num
		res = []
		for i in range(units):
			b = int(num[2*i:2*(i + 1)], 16)
			res.append(b)
		return res
	
class Message: #class representing standard messages
	response = None
	command = None
	data = None
	seq = None
	def __init__(self, response, command, seq, data):
		self.response = response
		self.command = command
		self.data = data
		self.seq = seq
	
	def construct(self):
		if(self.response): output  = COMMAND[self.command] + [self.seq, len(self.data) + 1] + self.data
		
		else: output  = COMMAND[self.command] + [0, len(self.data) + 1] + self.data
		
		chksum  = ~ sum(output) % 256
		output  = output + [chksum]
		
		if(self.response): output  = [0xff, 0xff] + output
		else: output  = [0xff, 0xfe] + output
		
		msg =  "".join(struct.pack("B", x) for x in output)
		
		return msg
		
		
