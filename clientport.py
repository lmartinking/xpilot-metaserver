import logging
import socket
from socket import SHUT_RDWR
import SocketServer
import threading
from common import *

class ClientPortRequestHandler(SocketServer.StreamRequestHandler):
	def handle(self):
		client_id = IpAddrPort(self.client_address[0], self.client_address[1])
		logging.info("Client " + str(client_id))

		for server_info in self.server.server_database.get_servers():
			to_send = server_info.to_string_client() + "\n"
			self.wfile.write(to_send)

		socket = self.request
		socket.shutdown(SHUT_RDWR)
		socket.close()

class ClientPortServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
	pass
