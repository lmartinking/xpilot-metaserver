import logging
import socket
from socket import SHUT_RDWR
import SocketServer
import threading
from common import *

class UserPortRequestHandler(SocketServer.StreamRequestHandler):
	def handle(self):
		client_id = IpAddrPort(self.client_address[0], self.client_address[1])
		logging.info("User " + str(client_id))

		self.data = "Nothing here yet\n"
		self.wfile.write(self.data)

		socket = self.request
		socket.shutdown(SHUT_RDWR)

class UserPortServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
	pass
