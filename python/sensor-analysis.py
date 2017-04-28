#!/usr/bin/python

import os as os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import argparse as ar
import sys

'''
INPUT
1. serial number table, to define how many devices
2. which sensor need to calculate

OUTPUT
1. Sensor include Pressure, Temperature, Humidility, TVOC, CO2 , Dust
2. Sensor compensation value, each sensor for each device has different value. 
3. Graph to show sensor curve.
'''
device_list = []
df = []
delta_table = []
SUPPORT_SENSOR_TYPE = ['P', 'T', 'H', 'D', 'V', 'C']

#version number
parser = ar.ArgumentParser(description='IPCS sensor collection tools, version=0.1')
parser.add_argument('-s', dest='category', action='append', nargs='+',
                    choices=SUPPORT_SENSOR_TYPE, required=True,
                    help='select sensor category')
parser.add_argument('-o', dest='file', action='store', nargs=1,
                    help='file to describe device serial number to be tested')
                    
args = parser.parse_args()


#Set working directory
current_dir =  os.getcwd()
os.chdir( str(os.getcwd()) + "/data" )
print 'Current Working Path is '+ str(os.getcwd())


def read_sn_from_file() :
    dev = []
    try:
        devfd = open( args.file[0], 'r')
    except:
	print "Oops! File doesn't exist"
	sys.exit()

    for devname in devfd :
        dev.append( devname.strip() )

    devfd.close()
    return  dev

def load_data_from_file( device, category ) :
    dataframe = []
    for devname in device :
        name = str(devname) + '.' + str(category) + '.csv'
	try:
	    dataframe.append( pd.DataFrame(pd.read_csv( name ,header=-1, names=['Value','Time'])) )
	except:
	    print "Oops! File doesn't exist"
	    break

    return dataframe

def write_data_to_file( sensor, delta ) :
	for devname in device_list:
	    index = device_list.index( devname )
	    print index
	    print delta[index]
	    filename = str(devname) + '.delta' 
	    fd = open( filename, 'w')
	    fd.write( str(sensor) + ":" + str(delta[index]) + ",\n" )
	    fd.close()
	print 'write_data_to_file'

def calculate_pressure( df ) :
    delta = []

    for i in range(0, len(df)):
	delta.append( df[i]['Value'].min() )
    
    print min(delta)
    delta = delta - min(delta)
    print delta
    return delta

def calculate_temp( df ) :
	delta = []
	print 'calculate_temp'
def calculate_humidility( df ) :
	print 'calculate_humidility'
def calculate_co2( df ) :
	print 'calculate_co2'
def calculate_tvoc( df ) :
	print 'calculate_tvoc'
def calculate_dust( df ) :
	print 'calculate_dust'



sensor_compensation = { 'P' : calculate_pressure,
			'T' : calculate_temp,
			'H' : calculate_humidility,
			'D' : calculate_dust,
			'V' : calculate_tvoc,
			'C' : calculate_co2,
}


'''
======MAIN FUNCTION======
'''

device_list = read_sn_from_file()

for item in args.category[0] :
    print item
    df = load_data_from_file( device_list, item )
    delta_table = sensor_compensation[item]( df )

    if( delta_table is not None ):
	write_data_to_file( item, delta_table )


#
#devnames = [   devname+'.p.csv', devname+'.t.csv', devname+'.h.csv',
#	       devname+'.d.csv', devname+'.v.csv', devname+'.c.csv']
#for devname in devnames
#    devname = devfd.readline().strip()
#    df = [ pd.DataFrame(pd.read_csv( devname ,header=-1, names=['Value','Time'])) for devname in devnames ]

#print df
#df=pd.DataFrame(pd.read_csv('1646I3000071.t.csv',header=-1, names=['Value','Time']))
#df2=pd.DataFrame(pd.read_csv('1646I3000072.t.csv',header=-1, names=['Value','Time']))
#print df.shape

#print df[0].columns
#print df[1].describe()
#print df2.describe()
#print df.head(3)
#print df.dtypes

#print df.max()

#min1 = df[0]['Value'].min()
#print df[0][df[0]['Value']==min1].index
##print df2[df2['Value']==min2].index


#min_value_size = len(df[0][df[0]['Value']==min1].index)
#print min_value_size

#Plot data curve
#test = df[0].set_index('Time')
#test.plot()

#test2 = df2.set_index('Time')
#test2.plot()
#plt.show()

#parser.add_argument('integers', metavar='N', type=int, nargs='+',
#                    help='an integer for the accumulator')
#parser.add_argument('--sum', dest='accumulate', action='store_const',
#                    const=sum, default=max,
#                    help='sum the integers (default: find the max)')

#parser.add_argument(dest='path', metavar='path')


