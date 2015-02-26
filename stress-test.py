#!/usr/bin/env python
import serial
from optparse import OptionParser, OptionGroup 
from time import sleep
from datetime import datetime

DEFAULT_DEVICE = "/dev/ttyUSB0"
DEFAULT_BAUD = 38400
DEFAULT_SLEEP = 0.01
TIMEMOUT = 0.01
LED_PATTERN= [[1, 8, 0],[1, 128,0],[2, 128,0],[4, 128, 0],[8, 128, 0],[1, 16, 0],[1, 64,0],[2, 64, 0],[4, 64, 0],[8, 64, 0],[1, 32, 0],[2, 32, 0],[4, 32, 0],[8, 32, 0],[2, 16, 0],[4, 16, 0],[8, 16, 0],[4, 8, 0],[8, 8, 0],[16, 8, 0],[16, 128, 0],[32, 128, 0],[64, 128, 0],[18, 128, 0],[16, 16, 0],[16, 64, 0],[32, 64, 0],[64, 64, 0],[128, 128, 0],[16, 32, 0],[32, 32, 0],[64, 32, 0],[128, 32, 0],[32, 16, 0],[64, 16, 0],[128, 16, 0],[64, 8, 0],[128, 8, 0],[0, 8, 1],[0, 128, 1],[0, 128, 2],[0, 128, 4],[0, 128, 8],[0, 16, 1],[0, 64, 1],[0, 64, 2],[0, 64, 4],[0, 64, 8],[0, 32, 1],[0, 32, 2],[0, 32, 4],[0, 32, 8],[0, 16, 2],[0, 16, 4],[0, 16, 8],[0, 8, 4],[0, 8, 8],[0, 8, 16],[0, 128, 16],[0, 128, 32],[0, 128, 64],[0, 128, 128],[0, 16, 16],[0, 64, 16],[0, 64, 32],[0, 64, 64],[0, 64, 128],[0, 32, 16],[0, 32, 32],[0, 32, 64],[0, 32, 128],[0, 16, 32],[0, 16, 64],[0, 16, 128],[0, 8, 64],[0, 8, 128]]


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
        pat = LED_PATTERN[i%76]
        ser.write("A%sB%sC%s" %(chr(pat[0]), chr(pat[1]), char(pat[2])))
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
