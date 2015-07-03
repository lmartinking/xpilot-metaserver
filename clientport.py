import socket
from socket import SHUT_RDWR
import threading
import SocketServer
from database import *

class ClientPortRequestHandler(SocketServer.StreamRequestHandler):
	def handle(self):
		print "Incoming client " + format(self.client_address[0]) + ":" + str(self.client_address[1])

		for server_info in server_database.get_servers():
			to_send = server_info.to_string_client() + "\n"
			self.wfile.write(to_send)

		socket = self.request
		socket.shutdown(SHUT_RDWR)
		socket.close()

class ClientPortServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
	pass
