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
devlist = []
device_size = 0
df = []
delta_table = []
SENSORS = {'P': 'press_k', 'T':'temp_k', 'H':'humi_k', 'D':'dust_k', 'V':'tvoc_k', 'C':'co2_k', 'L':'light_k'}

#version number
parser = ar.ArgumentParser(description='IPCS sensor collection tools, version=0.1')
parser.add_argument('-s', dest='category', action='append', nargs='+',
                    choices=SENSORS.keys(), required=True,
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
    df = []
    for devname in device :
        name = str(devname) + '.' + str(category) + '.csv'
#	print name
	try:
	    df.append( pd.DataFrame(pd.read_csv( name ,header=-1, names=['Value','Time'])) )
	except:
	    print "Oops! File doesn't exist"
	    break
#    print df
#    df.to_csv('pd.csv', float_format='%.2f', na_rep="NAN!")
    return df

def write_data_to_file( sensor, delta ) :
    print delta
    for devname in devlist:
	filename = str(devname) + '.def' 
	fd = open( filename, 'a')
	index = devlist.index( devname )
	fd.write( SENSORS[sensor] + ":" + str(delta[index]) + "\n" )
	fd.close()
    print 'write_data_to_file'

def find_peak_low( df, rdigit ) :
    MIN = 1000000
    delta = []

    for devdf in df :
	val = devdf['Value'].min()
	idx = devdf['Value'].idxmin()
	print val,idx

	if( val < MIN ) :
	    MIN = val
	    MIN_IDX = idx + 1
	    MIN_TIME = devdf.ix[idx,['Time']].values[0]

    print MIN,MIN_IDX, MIN_TIME

    for devdf in df :
	Min = devdf['Time'] <= MIN_TIME
	Max = devdf['Time'] >= MIN_TIME

#	print Min
	if( any(Min)) :
	    idx_Min = devdf.ix[Min, 'Time'].idxmax()
	else :
	    idx_Min = 0

	if( any(Max) ) :
	    idx_Max = devdf.ix[Max, 'Time'].idxmin()
	else :
	    idx_Max = len(Max)

	print idx_Min, idx_Max
	df_out = devdf.ix[idx_Min:idx_Max, ['Value']]
	df_out = (df_out - MIN)
	df_out = df_out.mean()
	delta.append(df_out.values[0])
	
    delta = [ round(val, rdigit) for val in delta ]

    if( rdigit is 0 ) :
	delta[:] = [int(a) for a in delta]
    return delta

def find_peak_high( df, rdigit ) :
    MAX = 0
    delta = []

    for devdf in df :
	val = devdf['Value'].max()
	idx = devdf['Value'].idxmax()
#	print val,idx

	if( val > MAX ) :
	    MAX = val
	    MAX_IDX = idx + 1
	    MAX_TIME = devdf.ix[idx,['Time']].values[0]

    print MAX,MAX_IDX, MAX_TIME

    for devdf in df :
	Min = devdf['Time'] <= MAX_TIME
	Max = devdf['Time'] >= MAX_TIME
#	print Min
	if( any(Min)) :
	    idx_Min = devdf.ix[Min, 'Time'].idxmax()
	else :
	    idx_Min = 0

	if( any(Max) ) :
	    idx_Max = devdf.ix[Max, 'Time'].idxmin()
	else :
	    idx_Max = len(Max)

	print 'idx_Min','idx_Max',idx_Min,idx_Max
	df_out = devdf.ix[idx_Min:idx_Max, ['Value']]
	df_out = (df_out - MAX) 
	df_out = df_out.mean()
	delta.append(df_out.values[0])

	delta = [ round(val, rdigit) for val in delta ]
#    print delta

	if( rdigit is 0 ) :
	    delta[:] = [int(a) for a in delta]
    return delta

def calculate_pressure( df ) :
    delta = []

    for i in range(0, len(df)):
	delta.append( df[i]['Value'].min() )
    
    print min(delta)
    delta = delta - min(delta)
    return delta

def calculate_temp( df ) :
    delta = find_peak_low(df,2)
    print 'calculate_temp'
    return delta
def calculate_humidility( df ) :
    delta = find_peak_high(df,1)
    print 'calculate_humidility'
    return delta
def calculate_co2( df ) :
    delta = find_peak_high(df,0)
    print 'calculate_co2'
    return delta
def calculate_tvoc( df ) :
    delta = find_peak_low(df,0)
    print 'calculate_tvoc'
    return delta
def calculate_dust( df ) :
    delta = find_peak_high(df,2)
    print 'calculate_dust'
    return delta
def calculate_light( df ) :
    delta = find_peak_high(df,0)
    print 'calculate_dust'
    return delta

def verify_sensor( stype, df ) :
    val = []
    for devdf in df :
	val.append( devdf['Value'].max() )

#    if( stype is "L" ) :
##    else if( stype is "D" ) :
 #   else #P, T, H , D , V, L


sensor_compensation = { 'P' : calculate_pressure,
			'T' : calculate_temp,
			'H' : calculate_humidility,
			'D' : calculate_dust,
			'V' : calculate_tvoc,
			'C' : calculate_co2,
			'L' : calculate_light,
}


'''
======MAIN FUNCTION======
'''

devlist = read_sn_from_file()
devsize = len(devlist)

for devname in devlist:
    filename = str(devname) + '.def' 
    index = devlist.index( devname )
    if( os.path.isfile(filename) ) :
	os.remove(filename)

for item in args.category[0] :
    print item
    df = load_data_from_file( devlist, item )
    delta_table = sensor_compensation[item]( df )
    print delta_table
    if( delta_table is not None ):
	write_data_to_file( item, delta_table )


#Plot data curve
#test = df[0].set_index('Time')
#test.plot()

#test2 = df2.set_index('Time')
#test2.plot()
#plt.show()

