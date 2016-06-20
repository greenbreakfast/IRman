import irMan
import sys
import os
import json
import time

ACTION_INFO			= 'info'
ACTION_READ			= 'read'
ACTION_TRANSMIT		= 'transmit'

### FUNCTIONS ###
# usage function
def usage():
	print 'Usage: irManService.py info'
	print '   Read version information from IR Device'
	print ''
	print 'Usage: irManService.py read <COMMAND NAME>'
	print '   Read an IR command name and save to a file specified by the COMMAND NAME argument'
	print ''
	print 'Usage: irManService.py transmit <COMMAND NAME> <COMMAND DELAY>'
	print '   Transmit one or more existing COMMANDS with a DELAY specified in seconds'
	print ''
	exit()

# check that number of arguments matches expectations
def checkNumArgs(numArgs, expectedNum, bMissingMsg=False):
	if numArgs < expectedNum:
		if bMissingMsg:
			print 'ERROR: missing argument!'
			print ''
		usage()

# check if a string contains just a number
def isNumber(s):
	try:
		int(s)
		return True
	except ValueError:
		return False



### MAIN PROGRAM ###
# find the directory of the script 
dirName = os.path.dirname(__file__)

# read the config file
with open( '/'.join([dirName, 'config.json']) ) as f:
	config = json.load(f)

# parse the results
commandDir 	= '/'.join([dirName, config['command_dir'] ])

# setup irMan
try:
	device 	= irMan.irMan(config['port'], config['baudrate'])
except ValueError as err:
	print('ERROR', err.args)
	exit()

# read the arguments
numArgs = len(sys.argv)
checkNumArgs(numArgs, 2)

action 	= sys.argv[1]

# further argument parsing
if action == ACTION_READ or action == ACTION_TRANSMIT:
	checkNumArgs(numArgs, 3, True)

	# parse the command names
	argList 	= sys.argv[2:numArgs]
	commands 	= []
	for val in argList:
		if isNumber(val):
			# argument is delay for previous command
			commands[-1]['delay'] 	= int(val)
		else:
			# argument is a command
			obj 	= 	{ 	'name': '/'.join([commandDir, val]),
							'delay': 0
						}
			commands.append(obj)
		

# run the commands
if action == ACTION_INFO:
	device.readInfo()
elif action == ACTION_READ:
	commandName = commands[0]['name']
	device.readCommand(commandName)
elif action == ACTION_TRANSMIT:
	print '> Transmitting command:'
	for command in commands:
		device.transmitCommand(command['name'])
		time.sleep(command['delay'])
else:
	print 'ERROR: invalid command!'
	print
	usage()


# clean-up
device.close()

