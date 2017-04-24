#!/usr/bin/python
import serial
import re
import os
import time;
import socket;
import sys;

#=====Input Variable Start======#
#If test mode is on, use hard code input
#In the other side, use argv input
test_mode = 1
t_ref = 0
#=====Input Variable End======#

#Flag to show sensor collection status
collect = 0

#Output Data Pattern
Ppat = re.compile('^P[0-9]+\.[0-9]')
Apat = re.compile('[POCVTHZ][0-9.]+')

#Read ipcs host name, the host name should be serial number of board
hostname = socket.gethostname()
print hostname
print 'ipcs 3.0 sensor test!'
fd = [	open('p.txt','w'), open('c.txt','w'), open('o.txt','w'),
	open('v.txt','w'), open('t.txt','w'),
	open('h.txt','w'), open('z.txt','w')			]
num = [ 'P', 'C', 'O', 'V', 'T', 'H', 'Z']

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


t_start = time.time()
print "start time is %d" %(t_start)


port = open_serial_port()

while os.path.isfile("run"):
    raw = port.read(1)           # Wait forever for anything
    data_left = port.inWaiting()  # Get the number of characters ready to be read
    raw += port.read(data_left) # Do the read and combine it with the first character
    print raw

    t_sensor = time.time() - t_start + t_ref
#    print "elspase time is %d" %(t_sensor-t_start+t_ref)

    if Ppat.search(raw):
	value = filter(lambda form: form in '0123456789.', Ppat.findall(raw)[0])
#	print value
	if (float(value) < 1100.0):
	    print 'Pressure value <= critera'
	    print 'Start to collect sensor data.'
	    collect = 1
	    fd[0].write( str(value) + ',' + str(int(t_sensor)) + '\n')
	    fd[0].flush
	else:
	    print 'Pressure value > critera'
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
	    print("COLLECTION<==TYPE({0:s}),VALUE({1:.1f}),TIME({2:d})".format(sensor_type, float(value),int(t_sensor)))
	    fd[ num.index(sensor_type) ].write( str(value) + ',' + str(int(t_sensor)) + '\n' )
	    fd[ num.index(sensor_type) ].flush()
#	    print "match is:"+ g
#	    i = 0;
#	    while ( len(list) > 0 ):
#		value = filter(lambda form: form in '0123456789.', list[i])
#		print "Apat:",list[i]
#		list.pop()
#		i += 1
		

print 'Close sensor collection data.'
fd[0].close()
fd[1].close()
print 'Close ttyS1 UART port.'
port.close()
