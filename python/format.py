#!/usr/bin/python
import serial
import re
import os

str = "P1034.8\nT24.5\nV-3247";
#print str.split( )

# Create a list.
elements = []

# Append empty lists in first two indexes.
elements.append([])
elements.append([])

pat = '[a-zA-Z]+[0-9\.\-]+'
result = re.findall(pat, str)
print result
