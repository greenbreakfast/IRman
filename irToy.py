import time
import serial

__version__ = "0.1"


REG_RESET 					= 0x00
REG_TRANSMIT 				= 0x03
REG_FREQ_REPORT 			= 0x04

REG_SETUP_SAMPLE_TIMER 		= 0x05
REG_SETUP_FREQ_MOD_TIMER	= 0x06

REG_LED_MUTE_ON 			= 0x10
REG_LED_MUTE_OFF 			= 0x11
REG_LED_ON 					= 0x12
REG_LED_OFF 				= 0x13

REG_SETTINGS 				= 0x23

REG_ENABLE_XMIT_BYTE_COUNT 			= 0x24
REG_ENABLE_XMIT_NOTIFY_COMPLETE 	= 0x25
REG_ENABLE_XMIT_HANDSHAKE 			= 0x26

REG_IO_WRITE 				= 0x30
REG_IO_DIR 					= 0x31
REG_IO_READ  				= 0x32
	
REG_UART_SETUP 				= 0x40
REG_UART_CLOSE 				= 0x41
REG_UART_WRITE 				= 0x42



class ComIRDevice:
	def __init__(self,port,baudrate):
		self.__bDebug = False
		self.__ser=serial.Serial(port,baudrate,timeout=.3)
		self.__ser.flushInput()
		#self.__ser.baudrate=Baud

	def SetDebug(self, bDebug):
		self.__bDebug = bDebug

	def GetData(self,numData):
		#return self.__ser.read(numData)
		mylist=list(self.__ser.read(numData))
		return mylist

	def GetIntData(self,numData):
		mylist=self.GetData(numData)
		intlist = []
		for data in mylist:
			intlist.append( ord(data) )
		return intlist

	
	def ReadString(self,numData):
		return str(self.__ser.read(numData))

	def GetSerialPort(self):
		return self.__ser

	def Close(self):
		if(self.__ser.isOpen()):
			self.__ser.close()
			
	def SendAscii(self,ascdata):
		num = self.__ser.write(chr(ascdata))
		return num
	
	def SendChar(self,chardata):
		num = self.__ser.write(chardata)
		return num

	def SendAsciiBuffer(self, bufferData):
		# count = 0
		# for data in bufferData:
		# 	self.SendAscii(data)
		# 	count += 1
		# return count
		chrBuffer = [ chr(x) for x in bufferData]
		self.SendAscii(REG_TRANSMIT)
		self.__ser.write(chrBuffer)
		# self.__ser.write( [chr(0xff), chr(0xff)] )

		return len(bufferData) + 1

	def TransmitCommand(self, commandData):
		# self.SendAscii(REG_TRANSMIT)
		self.FlushBuffers()
		txCmd = bytearray(commandData)
		# txBytes = self.SendAscii(txCmd)
		self.SendAscii(REG_TRANSMIT)
		txBytes = self.__ser.write(txCmd)
		print commandData
		self.__ser.write( bytearray([0xff, 0xff]) )

		return txBytes

	def TransmitCommandV2(self, commandData):
		# Set the modes
		self.FlushBuffers()
		print ' - enabling modes'
		self.EnableTransmitByteCount()
		self.EnableTransmitNotifyComplete()
		self.EnableTransmitHandshake()
		time.sleep(.05)

		# start transmit
		print ' - starting transmit mode'
		self.SendAscii(REG_TRANSMIT)

		# get first handshake
		print ' - waiting for handshake'
		response = self.GetIntData(1)
		print ' - reponse: ', response

		# transmit 
		txCmd = bytearray(commandData)
		txBytes = self.__ser.write(txCmd)

		print ' - waiting for final handshake'
		response = self.GetIntData(1)
		print ' - reponse: ', response

		print ' - transmit count'
		response = self.GetIntData(3)
		print ' - reponse: ', response

		print ' - waiting for notify complete'
		response = self.GetIntData(1)
		print ' - reponse: ', response


		return txBytes

	   
	def FlushBuffers(self):
		self.__ser.flushInput()
		self.__ser.flush()
		self.__ser.flushOutput()   
		
	def GetVersion(self):
		self.FlushBuffers()
		self.SendChar('v')
		time.sleep(.05)
		return str(self.__ser.read(4))

	def GetSettings(self):
		self.FlushBuffers()
		self.SendAscii(REG_SETTINGS)
		time.sleep(.05)
		return self.__ser.read()

	def SetLedMute(self, bMute):
		if bMute:
			reg = REG_LED_MUTE_ON
		else:
			reg = REG_LED_MUTE_OFF
		self.FlushBuffers()
		self.SendAscii(reg)
		time.sleep(.05)

	def SetLed(self, bOn):
		if bOn:
			reg = REG_LED_ON
		else:
			reg = REG_LED_OFF
		self.FlushBuffers()
		self.SendAscii(reg)
		time.sleep(.05)

	def EnableTransmitByteCount(self):
		self.FlushBuffers()
		self.SendAscii(REG_ENABLE_XMIT_BYTE_COUNT)

	def EnableTransmitNotifyComplete(self):
		self.FlushBuffers()
		self.SendAscii(REG_ENABLE_XMIT_NOTIFY_COMPLETE)

	def EnableTransmitHandshake(self):
		self.FlushBuffers()
		self.SendAscii(REG_ENABLE_XMIT_HANDSHAKE)

	def ResetMode(self):
		self.SendAscii(0x00)
		self.SendAscii(0x00)
		self.SendAscii(0x00)
		self.SendAscii(0x00)
		self.SendAscii(0x00)
		time.sleep(.05)
		self.FlushBuffers()

	def Reset(self):
		self.SendAscii(0xFF)
		self.SendAscii(0xFF)
		self.SendAscii(0xFF)
		self.SendAscii(0xFF)
		self.SendAscii(0xFF)
		self.SendAscii(0x00)
		time.sleep(.05)
		# self.FlushBuffers()
	
	def EnterSamplingMode(self):
		self.ResetMode()
		self.SendChar('s') # sampling mode 
		response = self.ReadString(3)
		print '  - Response: %s'%(response)   
		if(response=='S01'):
			return True
		return False
		
