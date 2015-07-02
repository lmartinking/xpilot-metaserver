#!/usr/bin/python

import socket
import threading
import SocketServer

from clientport import *
from serverport import *
from userport import *

host = "0.0.0.0"
client_port = 4401
server_port = 5500
user_port = 4400

def start_client_port_server():
	HOST, PORT = host, client_port
	server = ClientPortServer((HOST, PORT), ClientPortRequestHandler)
	ip, port = server.server_address
	server_thread = threading.Thread(target=server.serve_forever)
	server_thread.daemon = True
	server_thread.start()
	print "Server loop running in thread:", server_thread.name
	return server

def start_server_port_server():
	HOST, PORT = host, server_port
	server = ServerPortServer((HOST, PORT), ServerPortRequestHandler)
	ip, port = server.server_address
	server_thread = threading.Thread(target=server.serve_forever)
	server_thread.daemon = True
	server_thread.start()
	print "Server loop running in thread:", server_thread.name
	return server

def start_user_port_server():
	HOST, PORT = host, user_port
	server = UserPortServer((HOST, PORT), UserPortRequestHandler)
	ip, port = server.server_address
	server_thread = threading.Thread(target=server.serve_forever)
	server_thread.daemon = True
	server_thread.start()
	print "Server loop running in thread:", server_thread.name
	return server

if __name__ == "__main__":
	client_port_server = start_client_port_server()
	server_port_server = start_server_port_server()
	user_port_server = start_user_port_server()
	server_port_server.serve_forever()
	
