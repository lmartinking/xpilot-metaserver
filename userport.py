import logging
import socket
from socket import *
import threading
import SocketServer

class UserPortRequestHandler(SocketServer.StreamRequestHandler):
	def handle(self):
		logging.info("Incoming user " + format(self.client_address[0]) + ":" + str(self.client_address[1]))

		self.data = "Nothing here yet\n"
		self.wfile.write(self.data)

		socket = self.request
		socket.shutdown(SHUT_RDWR)

class UserPortServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
	pass
