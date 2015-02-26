#!/usr/bin/env python
import serial
from optparse import OptionParser, OptionGroup 
from time import sleep
from datetime import datetime

DEFAULT_DEVICE = "/dev/ttyUSB0"
DEFAULT_BAUD = 38400
DEFAULT_SLEEP = 0.01
TIMEMOUT = 0.01


def stress_test(device, baud, sleep_time):
    print("Stress testing rtiduino controller on port %s baudrate %s" % (device, baud))
    print("Sleep time set to %f" % sleep_time)
    try:
        ser = serial.Serial(device, baud, timeout=TIMEMOUT)
    except serial.serialutil.SerialException as e:
        print e
        exit(1)
    i = 0
    start = datetime.utcnow()
    while(True):
        ser.write("AQBWCE")
        resp = str(ser.readline())
        if not resp.startswith("OK"):
            print "ERROR: %s" % resp
            break
        else:
            i = i+1
        if i%500 == 0:
            print "Count = %d" % i

        sleep(sleep_time)
    print "Count = %d" % i
    print "Failed at %s" % datetime.utcnow()
    print "Ran for %s" % (datetime.utcnow() - start)


def main():
    parser = OptionParser(version="%prog 0.0.1")
    parser.add_option("-D", "--device", action="store",
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
    if options.sleep is None:
        sleep_time = float(DEFAULT_SLEEP)
    else:
        sleep_time = float(options.sleep)
    stress_test(device, baud, sleep_time)



if __name__ == "__main__":
    main()
