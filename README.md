# IRman

Learning and transmitting IR commands with the [Dangerous Prototypes USB IR Toy](http://dangerousprototypes.com/docs/USB_Infrared_Toy).


# Components

* `config.json`
  * Holds info on the serial port and baudrate to use when communicating with the IR Toy as well as the directory to hold the IR commands
* `irToy.py`
  * Class to perform all low-level interactions via serial with the IR Toy
* `irMan.py`
  * Wrapper class around `irToy` that provides recording and transmitting functionality
* `irManService.py`
  * Main program 


# Usage

Run-down of how to use the program.

## Read Settings

To read the IR Toy version info:
```
python irManService.py info
```

It should return something like:
```
> Version is: 'V222'
```

Where `V2` indicates the hardware version and `22` is the firmware version



## Learn a Command

Learning commands from remotes:
```
python irManService.py read <COMMAND NAME>
```

* When the LED on the IR Toy lights up, it is ready to learn a command from a remote.
* Point the remote at the IR Toy and press the desired button
* The IR Toy will encode the command and it will be saved to the `commands` directory under the name specified in the `<COMMAND NAME>` in the argument

**Example**
```
python irManService.py read tv/power
```
Will save the command for the Power button from your TV remote to `commands/tv/power`


## Transmit a Command

To transmit learned commands:
```
python irManService.py transmit <COMMAND NAME>
```

Note that the command must have been previously learned in order to transmit!

**Example**
To transmit the command learned in the section above:
```
python irManService.py transmit tv/power
```
Now your TV should be on!


## Transmit Multiple Commands

It will be handy to string together sequences of multiple commands:
```
python irManService.py transmit tv/mute stereo/power stereo/input1
```
The above will transmit:
* the command to mute the tv
* the command to toggle power on the stereo
* the command to set the stereo to input1


### Adding Delay

It is also possible to add a **delay** between transmitted commands:
```
python irManService.py transmit tv/mute 1 stereo/power 2 stereo/input1
```
The above will:
* transmit the command to mute the tv
* wait 1 second
* the command to toggle power on the stereo
* wait 2 seconds
* the command to set the stereo to input1

If no delay number is specified, the default is no delay between commands. 


## Happy transmissions!

