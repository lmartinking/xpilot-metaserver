import logging
import socket
from socket import SHUT_RDWR
import socketserver
import threading
from common import *

class UserPortRequestHandler(socketserver.StreamRequestHandler):
	def handle(self):
		client_id = IpAddrPort(self.client_address[0], self.client_address[1])
		logging.info("User " + str(client_id))

		self.data = "Nothing here yet\n"
		self.wfile.write(self.data)

		socket = self.request
		socket.shutdown(SHUT_RDWR)

class UserPortServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
	pass
