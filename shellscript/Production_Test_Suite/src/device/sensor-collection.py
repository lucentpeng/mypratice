#!/usr/bin/python
import serial
import re
import os
import time;
import socket;
import sys;
import argparse as ar
from threading import Thread, Lock

'''
INPUT
1. serial number table, to define how many devices
2. which sensor need to calculate

OUTPUT
1. Sensor include Pressure, Temperature, Humidility, TVOC, CO2 , Dust
2. Sensor compensation value, each sensor for each device has different value.
3. Graph to show sensor curve.
'''
#version number
parser = ar.ArgumentParser(description='IPCS sensor collection tools, version=0.1')
parser.add_argument('-t', dest='time_delay', action='store', nargs=1, required=True,
                    help='Set delay time from PC')
parser.add_argument('-c', dest='critera', action='store', nargs=1,
                    help='Set data collection critera')

args = parser.parse_args()

#Set working directory
current_dir =  os.getcwd()
os.chdir( str(os.getcwd()) + "/production_test_suite" )
print 'Current Working Path is '+ str(os.getcwd())

"""=====Input Variable Start======
If test mode is on, use hard code input
In the other side, use argv input"""
#There are many IPCS on the test chamber, PC need send reference time related to 1st test device.
t_ref = int(args.time_delay[0])
threadshold = float(args.critera[0])   #Data collection Critera , it is pressure value
collect = 0	    #Flag to identify collection start ot stop
mutex = Lock()	    #Mutex to control collect flag
"""=====Input Variable End======"""

#Output Data Pattern
Ppat = re.compile('^P[0-9]+\.[0-9]')
Apat = re.compile('[PCVTHD][\-0-9.]+')


num = [ 'P', 'T', 'H', 'D', 'V', 'C', 'L']

def open_file() :
    fd = []
    #Read ipcs host name, the host name should be serial number of board
    hostname = str(socket.gethostname())
    for n in num :
	filename = hostname + '.' + n + '.csv'
	fd.append(open(filename, 'w'))
    return fd

def write_to_file( fd, sensor, value, timestamp ) :
	idx = num.index( sensor )
	print("COLLECTION<==TYPE({0:s}),VALUE({1:.1f}),TIME({2:d})".format(sensor, float(value),int(timestamp)))
	fd[idx].write( str(value) + ',' + str(int(timestamp)) + '\n')
	fd[idx].flush()

def close_file( fd ) :
    print 'Close sensor collection data.'
    for index in range(len(fd)) :
	fd[index].close()

def open_serial_port() : #Open ttyS1 UART port.
    port = serial.Serial(
	    port = '/dev/ttyS1',
	    baudrate = 57600,
	    parity = serial.PARITY_NONE,
	    stopbits = serial.STOPBITS_ONE,
	    bytesize = serial.EIGHTBITS,
	    timeout=1 # add this
	)
    print port.name
    return port

def collect_on( ct ) :
    global collect
    global mutex

    mutex.acquire();
    try:
	if ct is not None :
	    collect = ct
	return collect
    finally:
	mutex.release()


def readLightSensor( fd ) :
    global t_ref
    while True:
	try:
	    adc = os.popen('cat /sys/bus/iio/devices/iio:device0/in_voltage0_raw').read()
	except :
	    print "Oops! Try again..."
	    break
	if collect_on(None) == 1 :
	    lux = abs(int(adc)) * 101 >> 8
	    t_sensor = time.time() - t_start + t_ref
	    write_to_file( fd, 'L', lux, t_sensor)
	    time.sleep(5) #update lux per 5 seconds

def trigger_decision( stype, value) :
	if( stype == 'P' ) :
	    if (float(value) < threadshold):
		print 'Activate collection. Reason:' + str(stype) + ' Sensor'
		collect_on(1)
	    else:
		print 'Deactive collection. Reason:' + str(stype) + ' Sensor'
		collect_on(0)


def do_collection( port, fd ) :
    global t_ref
    while os.path.isfile("RUN"):
	try:
	    raw = port.read(1)           # Wait forever for anything
	    data_left = port.inWaiting()  # Get the number of characters ready to be read
	    raw += port.read(data_left) # Do the read and combine it with the first character
	    print raw
	except :
	    print "Oops! Try again..."
	    port = open_serial_port()

	t_sensor = time.time() - t_start + t_ref
	#    print "elspase time is %d" %(t_sensor-t_start+t_ref)

	it = re.finditer(Apat, raw)
	for match in it:
	    print "'{g}' was found, {s}".format(g=match.group(), s=match.span())
	    g = match.group()
	    sensor_type = g[0]

	    value = filter(lambda form: form in '0123456789.', g)
	    trigger_decision( sensor_type, value)

	    if (collect_on(None) == 1):
		write_to_file( fd, sensor_type, value, t_sensor)

###################################
print 'ipcs 3.0 sensor test start!'

t_start = time.time()
print "start time is %d" %(t_start)

port = open_serial_port()
fd = open_file()

thread_light = Thread(target=readLightSensor, args=(fd,))
thread_light.setDaemon(True)
thread_light.start()

do_collection( port, fd );

close_file(fd)
print 'Close ttyS1 UART port.'
port.close()

print 'ipcs 3.0 sensor test finish!'
###################################
