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
    df_out = None
    for devname in device :
        name = str(devname) + '.' + str(category) + '.csv'
#	print name
	try:
	    if( df_out is None ) :
		df_out = pd.read_csv( name ,header=-1, names=['Value','Time'] )
		df_out.insert( 0, 'Device', devname)
	    else :
		df_in = pd.read_csv( name ,header=-1, names=['Value','Time'] )
		df_in.insert( 0, 'Device', devname)
#		df_out[:len(df_out.index)].append( df_in[1:30] )
		df_out = pd.concat( [df_out, df_in], axis=0 , ignore_index=True )
	except:
	    print "Oops! File doesn't exist"
	    break
#    print df_out
#    df_out.to_csv('pd.csv', float_format='%.2f', na_rep="NAN!")
    return df_out

def write_data_to_file( sensor, delta ) :
	for devname in devlist:
	    index = devlist.index( devname )
	    print index
	    print delta[index]
	    filename = str(devname) + '.delta' 
	    fd = open( filename, 'w')
	    fd.write( str(sensor) + ":" + str(delta[index]) + ",\n" )
	    fd.close()
	print 'write_data_to_file'

def calculate_pressure( df ) :
    # Get the min value of pressure
	print 123
	return None

def calculate( df ) :
	MIN = df['Value'].min() 
#	dfs = df.sort_values(['Value'])
#	print dfs
#	print devname
#	print df.loc[ devname ]
	df_min = df[ df['Value'] == MIN]
#	print df_min.values[:,2]
#	for value in df_min.values[:,2] :
#	    print df_min.values[0][value]
	print df_min.values[len(df_min)/2-1][1]
#	df_gold = df_min.at[len(df_min)/2 - 1, 'Time']
	a = df.values
	b = np.sort( a, axis=0 )
	
#	print b[:,1].tolist().index( MIN )
#	print b[:,2].tolist()
#	print b
#	b = np.split( a, 3, axis=0 )
	
#	print df_min['Time'].median()

#	for devname in devlist:
#	    print df_min[df_min['Device'] == devname]
#	    print len(df_min[df_min['Device'] == devname].index)
	# Get data frame from min value of pressure
#    df2 = df[df['Device'] == devname]



    # Find median time
#    MED = df_min['Time'].median() 
#    print df[df['Value'] == MIN & df['Time'] == MED]
#    df2.to_csv('123.csv')
#    print out['min']
    
#    print MED
#    print df_min
#    print df.dtypes
#print df[0][df[0]['Value']==min1].index
#    print df
#    print df['Value' == MIN]
#    for i in range(0, len(df)):
#	delta.append( df['Value'].min() )
#    
#    print min(delta)
#    delta = delta - min(delta)
#    print delta
#min_value_size = len(df[df[0]['Value']==min1].index)
	return None

def calculate_temp( df ) :
	calculate(df)
	print 'calculate_temp'
def calculate_humidility( df ) :
	calculate(df)
	print 'calculate_humidility'
def calculate_co2( df ) :
	calculate(df)
	print 'calculate_co2'
def calculate_tvoc( df ) :
	calculate(df)
	print 'calculate_tvoc'
def calculate_dust( df ) :
	calculate(df)
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

devlist = read_sn_from_file()
devsize = len(devlist)

for item in args.category[0] :
    print item
    df = load_data_from_file( devlist, item )
    delta_table = sensor_compensation[item]( df )

#    if( delta_table is not None ):
#	write_data_to_file( item, delta_table )


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

