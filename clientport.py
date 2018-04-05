import logging
import socket
from socket import SHUT_RDWR
import SocketServer
import threading
from common import *
import traceback

class ClientPortRequestHandler(SocketServer.StreamRequestHandler):
	def handle(self):
		try:
			client_id = IpAddrPort(self.client_address[0], self.client_address[1])
			logging.info("Client " + str(client_id))

			socket = self.request

			for server_info in self.server.server_database.get_servers():
				if not server_info.rtt == None:
					to_send = server_info.to_string_client() + "\n"
					try:
						self.wfile.write(to_send.encode("iso-8859-1"))
					except Exception, e:
						logging.info("Socket exception: " + str(client_id) + ", " + traceback.format_exc())

			socket.shutdown(SHUT_RDWR)
			socket.close()
		except Exception, e:
			logging.exception(e)

class ClientPortServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
	pass
