#!/usr/bin/python

import socket
import sys

#HOST, PORT = "meta2.xpilot.org", 4401
HOST, PORT = "localhost", 4401
data = " ".join(sys.argv[1:])

# Create a socket (SOCK_STREAM means a TCP socket)
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
	# Connect to server and send data
	sock.connect((HOST, PORT))
	#sock.sendall(data + "\n")

	data = sock.recv(1024)
	string = ""
	while len(data):
		string = string + data
		data = sock.recv(1024)
	print string

finally:
	sock.close()
