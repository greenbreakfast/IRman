import irToy
import json
import os

__version__ = "0.1"

EXIT_SUCCESS	= True
EXIT_FAILURE	= False

class irMan:
	def __init__(self, port, baudrate):
		if not port:
			raise ValueError('No port specified')
		if not baudrate:
			raise ValueError('No baudrate specified')
		self.ir = irToy.ComIRDevice(port, baudrate )
		self.bSamplingMode =	False

	def _checkPath(self, f):
		d = os.path.dirname(f)
		if not os.path.exists(d):
			os.makedirs(d)

	# if not already in sampling mode, enter sampling mode
	def enterSamplingMode(self):
		if self.bSamplingMode == False:
			success = self.ir.EnterSamplingMode()
			print '> Entered sampling mode: %d'%(success)
			if success:
				self.bSamplingMode = True
			return success
		else:
			return EXIT_SUCCESS


	# function to read info from IRtoy
	def readInfo(self):
		# check the version
		version = self.ir.GetVersion()
		print '> Version is: \'%s\''%(version)

		# get the Settings byte
		settings = self.ir.GetSettings()
		if settings:
			print '> Settings byte is ', hex(ord(settings))

	# function to read a command and write to file
	def readCommand(self, commandName):
		# enter sampling mode 
		self.enterSamplingMode()

		# enable the LED
		print '> Enabling LED'
		self.ir.SetLedMute(False)
		self.ir.SetLed(True)

		# read bytes
		print '> Reading '
		commandData = []
		while 1:
			rdData = self.ir.GetIntData(4)
			#if len(data) == 2:
			if len(rdData) >= 2:
				# add to overall list
				commandData = commandData + rdData

				# check for end of data
				if (rdData[0] == 0xff and rdData[1] == 0xff):
					print '> Received end code'
					print '> Read %d bytes'%(len(commandData))
					break

		# write the data to file
		self._checkPath(commandName)
		with open(commandName, 'w') as fp:
			json.dump(commandData, fp)

		return

	# function to transmit a command stored in a file
	def transmitCommand(self, commandName):
		# enter sampling mode 
		self.enterSamplingMode()

		# read the file
		if os.path.isfile(commandName) == False:
			print 'ERROR: command file not found'
			return

		# read the command data
		with open(commandName) as f:
			commandData = json.load(f)

		# transmit the data
		txBytes = self.ir.TransmitCommand(commandData)
		print '> Transmitted %d bytes'%(txBytes)

		return

	def close(self):
		# clean-up
		self.ir.Reset()
		self.ir.Close()
