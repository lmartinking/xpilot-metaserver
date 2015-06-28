#!/usr/bin/python

import socket
import threading
import SocketServer

class UserPortRequestHandler(SocketServer.StreamRequestHandler):
    def handle(self):
	self.data = self.rfile.readline().strip()
	print "{} wrote:".format(self.client_address[0])
	print self.data
	self.wfile.write(self.data.upper())

class UserPortServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    pass
