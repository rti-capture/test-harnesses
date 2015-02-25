#!/usr/bin/env python
import serial
from optparse import OptionParser, OptionGroup 
from time import sleep

VERSION_NUMBER = "0.0.1"
DEFAULT_DEVICE = "/dev/ttyUSB0"
DEFAULT_BAUD = 38400
DEFAULT_SLEEP = 1
TIMEMOUT = 0.1


def stress_test(device, baud, sleep):
	print("Stress testing rtiduino controller on port %s baudrate %s" % (device, baud))
	print("Sleep time set to %d" % sleep)
	ser = serial.Serial(device, baud, timeout=TIMEMOUT)
	while(True):
		ser.write("AQBWCE")


def main():
    parser = Optionparser(version="%prog %s"% VERSION_NUMBER)
    parser.add_option("-d", "--device", action="store",
    	type="string", dest="device",
    	help="The serial port to use")
    parser.add_option("-b", "--baud", action="store",
    	type="string", dest="baud",
    	help="The baudrate to use")
    parser.add_option("-s", "--sleep", action="store",
    	type="string", dest="sleep",
    	help="The amount of time to sleep between sucessive messages")
    (options, args) = parser.parse_args()
   
    if options.device is None:
    	device = DEFAULT_DEVICE
    else:
    	device = options.device
	if options.baud is None:
		baud = DEFAULT_BAUD
	else:
		baud = options.baud
	stress_test(device, baud)



if __name__ == "__main__":
	main()
