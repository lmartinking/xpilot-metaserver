#!/usr/bin/python

import logging
import signal
import socket
import SocketServer
import sys
import threading

from clientport import *
from database import *
from serverport import *
from userport import *

host = "0.0.0.0"
client_port = 4401
server_port = 5500
user_port = 4400

def start_client_port_server():
	HOST, PORT = host, client_port
	SocketServer.TCPServer.allow_reuse_address = True
	server = ClientPortServer((HOST, PORT), ClientPortRequestHandler)
	ip, port = server.server_address
	server_thread = threading.Thread(target=server.serve_forever)
	server_thread.daemon = True
	server_thread.start()
	return server

def start_server_port_server():
	HOST, PORT = host, server_port
	server = ServerPortServer((HOST, PORT), ServerPortRequestHandler)
	ip, port = server.server_address
	server_thread = threading.Thread(target=server.serve_forever)
	server_thread.daemon = True
	server_thread.start()
	return server

def start_user_port_server():
	HOST, PORT = host, user_port
	SocketServer.TCPServer.allow_reuse_address = True
	server = UserPortServer((HOST, PORT), UserPortRequestHandler)
	ip, port = server.server_address
	server_thread = threading.Thread(target=server.serve_forever)
	server_thread.daemon = True
	server_thread.start()
	return server

def start_database():
	database_thread = threading.Thread(target = ServerDatabase.handle, args = (server_database, 0))
	database_thread.start()
	return database_thread

def init_logging():
	logging.basicConfig(filename='metaserver.log', format='%(asctime)s %(message)s', level=logging.DEBUG)

if __name__ == "__main__":
	init_logging()
	client_port_server = start_client_port_server()
	server_port_server = start_server_port_server()
	user_port_server = start_user_port_server()
	database_thread = start_database()
	try:
		server_port_server.serve_forever()
	except KeyboardInterrupt:
		server_database.is_exiting = True
		server_port_server.shutdown()
	database_thread.join()
