# _*_encoding: utf-8_*_
import requests
import commands
import thread
import os

import Tkinter
from Tkinter import *
from requests import get
from ConfigParser import SafeConfigParser

import socket

path = None
command = None
stm = None
IDIP = None
savepath = None
filepath1 = None
filename1 = None
filepath2 = None
filename2 = None

top = Tkinter.Tk()
top.title("IPCS_COMMAND")
top.resizable(0,0)
top.configure(background='PaleTurquoise1')

def main():
	global id, port, PATH, COMMAND, SAVEPATH, FILEPATH1, FILENAME1, FILEPATH2, FILENAME2
	if stm == "Windows":
		Tkinter.Label(top, text="IPCS:",bg='PaleTurquoise1').grid(row=0, column=0, sticky=W)
		id = Tkinter.Entry(bg='MediumPurple1')
		id.grid(row=0, column=1)
		id.insert(1,"10.100.181.164")
	elif stm == "Linux":
		Tkinter.Label(top, text="IPCS:",bg='PaleTurquoise1').grid(row=0, column=0, sticky=W)
		id = Tkinter.Entry(bg='MediumPurple1')
		id.grid(row=0, column=1)
		id.insert(1,"1606I0000010")
	else:
		Tkinter.Label(top, text="IPCS:",bg='PaleTurquoise1').grid(row=0, column=0, sticky=W)
		id = Tkinter.Entry(bg='MediumPurple1')
		id.grid(row=0, column=1)
		id.insert(1,"1646I3000071")
	#COMMAND#
	Tkinter.Label(top, text="Port:",bg='PaleTurquoise1').grid(row=1, column=0, sticky=W)
	port = Tkinter.Entry(bg='MediumPurple1')
	port.grid(row=1, column=1)
	port.insert(1,"8000")
	Tkinter.Label(top, text="Path",bg='PaleTurquoise1').grid(row=5, column=0, sticky=W)
	PATH = Tkinter.Entry()
	PATH.grid(row=5, column=1)
	PATH.insert(1,"/home/ubuntu")
	Tkinter.Label(top, text="Command",bg='PaleTurquoise1').grid(row=6, column=0, sticky=W)
	COMMAND = Tkinter.Entry()
	COMMAND.grid(row=6, column=1)
	COMMAND.insert(1,"pwd")
	#UPLOAD#
	Tkinter.Label(top, text="Save Path",bg='PaleTurquoise1').grid(row=7, column=0, sticky=W)
	SAVEPATH = Tkinter.Entry(bg='wheat')
	SAVEPATH.grid(row=7, column=1)
	SAVEPATH.insert(1,"/home/ubuntu/")
	Tkinter.Label(top, text="File Path",bg='PaleTurquoise1').grid(row=8, column=0, sticky=W)
	FILEPATH1 = Tkinter.Entry(bg='wheat')
	FILEPATH1.grid(row=8, column=1)
	FILEPATH1.insert(1,"File Path")
	Tkinter.Label(top, text="File name",bg='PaleTurquoise1').grid(row=9, column=0, sticky=W)
	FILENAME1 = Tkinter.Entry(bg='wheat')
	FILENAME1.grid(row=9, column=1)
	FILENAME1.insert(1,"file")
	#DOWNLOAD#
	Tkinter.Label(top, text="File Path",bg='PaleTurquoise1').grid(row=10, column=0, sticky=W)
	FILEPATH2 = Tkinter.Entry()
	FILEPATH2.grid(row=10, column=1)
	FILEPATH2.insert(1,"/home/ubuntu/")
	Tkinter.Label(top, text="File name",bg='PaleTurquoise1').grid(row=11, column=0, sticky=W)
	FILENAME2 = Tkinter.Entry()
	FILENAME2.grid(row=11, column=1)
	FILENAME2.insert(1,"file")



def post_data():
	global IDIP
	check()
	if stm == "Windows":
		IDIP = ID
	elif stm == "Linux":
		ph = "avahi-resolve -n -4 " + ID + ".local | awk '{print $2}'"
		IDIP = commands.getoutput(ph)
	else:
		ph = "avahi-resolve -n -4 " + ID + ".local | awk '{print $2}'"
		IDIP = commands.getoutput(ph)
	url = "http://" + IDIP + ":" + PORT
	sensor_data = {"data":{
		"reserved0":path,
		"reserved1":command,
		"reserved2":"/home/ubuntu/henry/",
		"reserved5":filename1,
		"reserved6":'0'
		}}

	req = requests.post(url, json=sensor_data)
	thread.start_new_thread(take_data,())


def take_data():
	UURL = "http://" + IDIP + ":" + PORT + "/command"
	response = requests.request("GET", UURL)
	print response.text

def _download():
	check()
	if stm == "Windows":
		IDIP = ID
	elif stm == "Linux":
		ph = "avahi-resolve -n -4 " + ID + ".local | awk '{print $2}'"
		IDIP = commands.getoutput(ph)
	else:
		ph = "avahi-resolve -n -4 " + ID + ".local | awk '{print $2}'"
		IDIP = commands.getoutput(ph)
	url = "http://" + IDIP + ":" + PORT
	sensor_data = {"data":{
		"reserved0":" ",
		"reserved2":filepath2,
		"reserved5":filename2,
		"reserved6":'2'
		}}
	requests.post(url, json=sensor_data)
	UURL = "http://" + IDIP + ":" + PORT + "/command"
	response = requests.request("GET", UURL)
	print "updata_data: %s%s"%(filepath2, filename2)
	print ''

	port_uu = 9600
	address = (IDIP, port_uu)
	socket02 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	socket02.connect(address)
	print('start send Data')
	#ki = os.path.abspath('.') + '/'
	fo = open('C:/Users/Yakumo/Desktop/' + filename2, "w")
	while True:
		imgData = socket02.recv(512)
		if not imgData:
			break
		fo.write(imgData)
	fo.close()
	print('transmit end')
	socket02.close()


def _updata():
	check()
	if stm == "Windows":
		IDIP = ID
	elif stm == "Linux":
		ph = "avahi-resolve -n -4 " + ID + ".local | awk '{print $2}'"
		IDIP = commands.getoutput(ph)
	else:
		ph = "avahi-resolve -n -4 " + ID + ".local | awk '{print $2}'"
		IDIP = commands.getoutput(ph)
	url = "http://" + IDIP + ":" + PORT
	sensor_data = {"data":{
		"reserved0":" ",
		"reserved2":savepath,
		"reserved5":filename1,
		"reserved6":'1'
		}}
	requests.post(url, json=sensor_data)
	UURL = "http://" + IDIP + ":" + PORT + "/command"
	response = requests.request("GET", UURL)
	print "updata_data: %s%s"%(filepath1, filename1)
	print ''

	port_uu = 9700
	address = (IDIP, port_uu)
	socket02 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	socket02.connect(address)
	print('start send Data')
	fo = open(filepath1 + filename1, "rb")
	while True:
		imgData = fo.readline(512)
		if not imgData:
			break
		socket02.send(imgData)
	fo.close()
	print('transmit end')
	socket02.close()



def system():
	global stm
	stm = str(var.get())
	main()


def check():
	global ID, PORT, path, command, savepath, filepath1, filename1, filepath2, filename2
	ID = id.get()
	PORT = port.get()
	path = PATH.get()
	command = COMMAND.get()
	savepath = SAVEPATH.get()
	filepath1 = FILEPATH1.get()
	filename1 = FILENAME1.get()
	filepath2 = FILEPATH2.get()
	filename2 = FILENAME2.get()

def _thread1():
	thread.start_new_thread(_updata,())
def _thread2():
	thread.start_new_thread(_download,())

if __name__ == '__main__':
	main()
	var = StringVar()
	Tkinter.Button(top, text="Enter", command=post_data).grid(column=2,row=5,ipady = 5, ipadx = 14, rowspan = 2)
	Tkinter.Button(top, text="Upload", command=_thread1).grid(column=2,row=7,ipady = 18, ipadx = 7, rowspan = 3)
	Tkinter.Button(top, text="Download", command=_thread2).grid(column=2,row=10,ipady = 5, ipadx = 0, rowspan = 2)
	system1 = Radiobutton(top, text="ＳＮ", variable=var, value='Linux',command=system,bg='PaleTurquoise1',activebackground='PaleTurquoise1').grid(column=3,row=0,ipady = 0, ipadx = 3, rowspan = 2, sticky=N)
	system2 = Radiobutton(top, text="ＩＰ", variable=var, value='Windows',command=system,bg='PaleTurquoise1',activebackground='PaleTurquoise1').grid(column=3,row=1,ipady = 0, ipadx = 3, rowspan = 2, sticky=W)


top.mainloop()
