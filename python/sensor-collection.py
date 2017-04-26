#!/usr/bin/python
import serial
import re
import os
import time;
import socket;
import sys;
from threading import Thread

"""=====Input Variable Start======
If test mode is on, use hard code input
In the other side, use argv input"""
t_ref = 0	    #There are many IPCS on the test chamber, PC need send reference time related to 1st test device.
threadshold = 1100   #Data collection Critera , it is pressure value
"""=====Input Variable End======"""

#Output Data Pattern
Ppat = re.compile('^P[0-9]+\.[0-9]')
Apat = re.compile('[PCVTHD][0-9.]+')


num = [ 'P', 'T', 'H', 'D', 'V', 'C', 'L']

def open_file() :
    fd = []
    #Read ipcs host name, the host name should be serial number of board
    hostname = str(socket.gethostname())
    for n in num :
	filename = hostname + '.' + n.lower() + '.csv'
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



def readLightSensor( fd ):
    while True:
	adc = os.popen('cat /sys/bus/iio/devices/iio:device0/in_voltage0_raw').read()
	lux = abs(int(adc)) * 101 >> 8
	t_sensor = time.time() - t_start + t_ref
	write_to_file( fd, 'L', lux, t_sensor)
	time.sleep(5) #update lux per 5 seconds


def do_collection( port, fd ) :
    collect = 0	    #Flag to identify collection start ot stop
    while os.path.isfile("run"):
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

	if Ppat.search(raw):
	    value = filter(lambda form: form in '0123456789.', Ppat.findall(raw)[0])
	    #	print value
	    if (float(value) < threadshold):
		print 'Start to collect sensor data.'
		collect = 1
		write_to_file( fd, 'P', value, t_sensor)
	    else:
		print 'Stop to collect sensor data'
		collect = 0

	if (collect == 1):
	    it = re.finditer(Apat, raw)
	    for match in it:
		print "'{g}' was found, {s}".format(g=match.group(), s=match.span())
		g = match.group()
		sensor_type = g[0]
		print sensor_type

		value = filter(lambda form: form in '0123456789.', g)

		if( sensor_type != 'P' ) :
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
