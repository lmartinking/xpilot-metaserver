import socket
import threading
import SocketServer

class UserPortRequestHandler(SocketServer.StreamRequestHandler):
	def handle(self):
		print "Incoming user " + format(self.client_address[0]) + ":" + str(self.client_address[1])

		self.data = self.rfile.readline().strip()
		print "Received: " + self.data
		self.wfile.write(self.data.upper())

class UserPortServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
	pass
