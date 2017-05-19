# _*_encoding: utf-8_*_

from BaseHTTPServer import BaseHTTPRequestHandler
import cgi
import json
import re
from collections import OrderedDict
import socket
import struct
import fcntl
import time
import thread
import time

import commands, subprocess, os

post_values = None
cmd = None
CWD = None
IDIP = None
pt = None
dataname = None

#HOST_NAME = getip('eth0')#linux
#HOST_NAME = '10.100.182.210' #win7
PORT_NUMBER = 9803


class TodoHandler(BaseHTTPRequestHandler):
    TODOS = []
    dt = ['test']
    #print TODOS


    def do_GET(self):
	    global cmd, CWD, pt, dataname
	    message = json.dumps(post_values)
	    msg = json.dumps(self.dt)

	    if self.path.endswith("/command"):
		    self.send_response(200)
		    self.send_header('Content-type', 'text/html')
		    self.end_headers()

		    CWD = re.search('\"reserved0\": \"(.*?)\"', message)
		    cmd = re.search('\"reserved1\": \"(.*?)\"', message)

		    pt = re.search('\"reserved2\": \"(.*?)\"', message)
		    upd = re.search('\"reserved3\": \"(.*?)\"', message)
		    dow = re.search('\"reserved4\": \"(.*?)\"', message)
		    dataname = re.search('\"reserved5\": \"(.*?)\"', message)
		    statu = re.search('\"reserved6\": \"(.*?)\"', message)
		    print statu
		    if statu.group(1) == '1':
			    thread.start_new_thread(receive,())

		    elif statu.group(1) == '2':
			    thread.start_new_thread(send,())

		    elif CWD.group(1) == 'kill':
			    IDIP.kill()
			    self.wfile.write("Close")
		    else:
			    thread.start_new_thread(start,())
			    time.sleep(0.1)
			    stdoutput,erroutput=IDIP.communicate(input=None)
			    red = str(stdoutput)
			    err = str(erroutput)
			    self.wfile.write(red)
			    self.wfile.write(err)


    def do_POST(self):
	    global post_values
	    ctype, pdict = cgi.parse_header(self.headers['content-type'])
	    if ctype == 'application/json':
		    length = int(self.headers['content-length'])
		    post_values = json.loads(self.rfile.read(length))
		    self.TODOS.append(post_values)
		    #values = '{test:}'
		    #self.dt.append(values)

	    else:
		    self.send_error(415, "Only json data is supported.")
		    return

	    self.send_response(200,'test')
	    self.send_header('Content-type', 'application/json')
	    self.end_headers()
	    self.wfile.write(post_values)
	    print "Receive: %s\n"%json.dumps(post_values, indent = 1)

def start( ):
    global IDIP
    IDIP = subprocess.Popen(cmd.group(1), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=CWD.group(1))

def getip(ethname):
    s=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(s.fileno(), 0X8915, struct.pack('256s', ethname[:15]))[20:24])

def receive():
    address = (getip('eth0'), 9700)
    message = json.dumps(post_values)
    socket01 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket01.bind(address)
    socket01.listen(3)
    print('Socket Startup')
    conn, addr = socket01.accept()
    print('Connected by', addr)
    ##################################################
    fi = open(pt.group(1) + dataname.group(1), 'w')
    while True:
	    Data = conn.recv(512)
	    if not Data:
		    break
	    fi.write(Data)
    fi.close()
    ##################################################
    conn.close()
    socket01.close()
    print('server close')

def send():
    address = (getip('eth0'), 9700)
    message = json.dumps(post_values)
    socket01 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket01.bind(address)
    socket01.listen(3)
    print('Socket Startup')
    conn, addr = socket01.accept()
    print('Connected by', addr)
    ##################################################
    fo = open(pt.group(1) + dataname.group(1), 'rb')
    while True:
	    Data = fo.readline(512)
	    if not Data:
		    break
	    conn.sendall(Data)
    fo.close()
    ##################################################
    conn.close()
    socket01.close()
    print('server close')



if __name__ == '__main__':
    from BaseHTTPServer import HTTPServer
    server = HTTPServer((getip('eth0'), PORT_NUMBER), TodoHandler)
    print("Starting server, use <Ctrl-C> to stop")
    thread.start_new_thread(server.serve_forever(),)
