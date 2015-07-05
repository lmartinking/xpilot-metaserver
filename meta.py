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

# parameters - change if necessary
host = "0.0.0.0"
client_port = 4401
server_port = 5500
user_port = 4400
server_timeout = 10*60	# in seconds

# parameters - do not change
meta_version = "0.1"

def start_client_port_server(server_database):
	HOST, PORT = host, client_port
	SocketServer.TCPServer.allow_reuse_address = True
	server = ClientPortServer((HOST, PORT), ClientPortRequestHandler)
	server.server_database = server_database
	ip, port = server.server_address
	server_thread = threading.Thread(target=server.serve_forever)
	server_thread.daemon = True
	server_thread.start()
	logging.info("Started client port thread at " + format(HOST) + ":" + str(PORT))
	return server

def start_server_port_server(server_database):
	HOST, PORT = host, server_port
	server = ServerPortServer((HOST, PORT), ServerPortRequestHandler)
	server.server_database = server_database
	ip, port = server.server_address
	server_thread = threading.Thread(target=server.serve_forever)
	server_thread.daemon = True
	server_thread.start()
	logging.info("Started server port thread at " + format(HOST) + ":" + str(PORT))
	return server

def start_user_port_server():
	HOST, PORT = host, user_port
	SocketServer.TCPServer.allow_reuse_address = True
	server = UserPortServer((HOST, PORT), UserPortRequestHandler)
	ip, port = server.server_address
	server_thread = threading.Thread(target=server.serve_forever)
	server_thread.daemon = True
	server_thread.start()
	logging.info("Started user port thread at " + format(HOST) + ":" + str(PORT))
	return server

def start_database(server_timeout):
	server_database = ServerDatabase(server_timeout)
	database_thread = threading.Thread(target = ServerDatabase.handle, args = (server_database, None))
	database_thread.start()
	logging.info("Started server database with server_timeout=" + str(server_timeout))
	return (database_thread, server_database)

def init_logging():
	logging.basicConfig(filename='metaserver.log', format='%(asctime)s %(message)s', level=logging.INFO)

if __name__ == "__main__":
	init_logging()
	logging.info("Starting XPilot MetaServer " + meta_version)
	(database_thread, server_database) = start_database(server_timeout)
	server_port_server = start_server_port_server(server_database)
	client_port_server = start_client_port_server(server_database)
	user_port_server = start_user_port_server()
	try:
		server_port_server.serve_forever()
	except KeyboardInterrupt:
		server_database.is_exiting = True
		server_port_server.shutdown()
	database_thread.join()
