#!/usr/bin/python
import time;

cutime = time.time()
print "Time :", cutime
localtime = time.localtime(time.time())
print "Local current time :", localtime

time.sleep(2);
cutime = time.time()
print "Time :", cutime
