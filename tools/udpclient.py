#!/usr/bin/python

import socket
import sys

HOST, PORT = "localhost", 5500
SRCPORT = 15345

# add server
data = "add server localhost\nadd users 0\nadd version 1.4.6fxi~7\nadd map Xpilot-Tournament Map (Blood's Music)\nadd sizeMap 100x100\nadd author \"Patrick Kenny - pkenny@eecs.umich.edu\"\nadd bases 8\nadd fps 50\nadd port 15345\nadd mode ok\nadd teams 2\nadd free 2=4,4=4\nadd timing 0\nadd stime 1435952538\nadd queue 0\nadd sound no\n\nadd status SERVER VERSION...: 1.4.6fxi~7\nSTATUS...........: ok\nMAX SPEED........: 50 fps\nWORLD (100x100)..: Xpilot-Tournament Map (Blood's Music)\nAUTHOR.....: \"Patrick Kenny - pkenny@eecs.umich.edu\"\nPLAYERS ( 0/ 8)..:\nadd players Test1=test@xpilot.org{2},Test2=test@xpilot.org{4}"
# remove server
#data = "server localhost\nremove"

# SOCK_DGRAM is the socket type to use for UDP sockets
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(('', SRCPORT))

sock.sendto(data, (HOST, PORT))
#received = sock.recv(1024)

