#!/usr/bin/env python

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
from faqport import *
from pinger import *

# parameters - change if necessary
host = "0.0.0.0"
client_port = 4401
server_port = 5500
user_port = 4400
faq_port = 4402
server_timeout = 10*60	# in seconds
ping_timeout = 2	# in seconds
ping_interval = 60	# in seconds
servers_file = "servers.txt"
log_file = "metaserver.log"
faq_file = "FAQ"

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

def start_server_port_server(server_database, ping_timeout):
	HOST, PORT = host, server_port
	server = ServerPortServer((HOST, PORT), ServerPortRequestHandler)
	server.server_database = server_database
	server.ping_timeout = ping_timeout
	ip, port = server.server_address
	server_thread = threading.Thread(target=server.serve_forever)
	server_thread.daemon = True
	server_thread.start()
	logging.info("Started server port thread at " + format(HOST) + ":" + str(PORT) + " with ping_timeout=" + str(ping_timeout))
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

def start_faq_port_server():
	HOST, PORT = host, faq_port
	SocketServer.TCPServer.allow_reuse_address = True
	server = FaqPortServer((HOST, PORT), FaqPortRequestHandler)
	server.faq_file = faq_file
	ip, port = server.server_address
	server_thread = threading.Thread(target=server.serve_forever)
	server_thread.daemon = True
	server_thread.start()
	logging.info("Started FAQ port thread at " + format(HOST) + ":" + str(PORT))
	return server

def start_database(server_timeout, servers_file):
	server_database = ServerDatabase(server_timeout, servers_file)
	database_thread = threading.Thread(target = ServerDatabase.handle, args = (server_database, None))
	database_thread.start()
	logging.info("Started server database with server_timeout=" + str(server_timeout) + ", servers_file=" + servers_file)
	return (database_thread, server_database)

def start_pinger(ping_interval, ping_timeout, servers_database):
	server_pinger = ServerPinger(ping_interval, ping_timeout, servers_database)
	pinger_thread = threading.Thread(target = ServerPinger.handle, args = (server_pinger, None))
	pinger_thread.start()
	return (pinger_thread, server_pinger)

def init_logging(log_file):
	logging.basicConfig(filename = log_file, format = "%(asctime)s %(message)s", level = logging.INFO)

if __name__ == "__main__":
	init_logging(log_file)
	logging.info("Starting XPilot MetaServer " + meta_version)
	(database_thread, server_database) = start_database(server_timeout, servers_file)
	(pinger_thread, server_pinger) = start_pinger(ping_interval, ping_timeout, server_database)
	server_port_server = start_server_port_server(server_database, ping_timeout)
	client_port_server = start_client_port_server(server_database)
	user_port_server = start_user_port_server()
	faq_port_server = start_faq_port_server()
	try:
		server_port_server.serve_forever()
	except KeyboardInterrupt:
		server_database.is_exiting = True
		server_pinger.is_exiting = True
		server_port_server.shutdown()
	database_thread.join()
	pinger_thread.join()
