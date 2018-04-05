import logging
import socket
from socket import SHUT_RDWR
import SocketServer
import threading
from common import *
import traceback

class FaqPortRequestHandler(SocketServer.StreamRequestHandler):
	def handle(self):
		try:
			client_id = IpAddrPort(self.client_address[0], self.client_address[1])
			logging.info("Sending FAQ to " + str(client_id))

			faq_file = open(self.server.faq_file, "r")
			faq_data = faq_file.read()
			faq_data = to_unicode_if_string(faq_data)

			socket = self.request

			try:
				self.wfile.write(faq_data.encode("iso-8859-1"))
			except Exception, e:
				logging.info("Socket exception: " + str(client_id) + ", " + traceback.format_exc())
			faq_file.close()

			socket.shutdown(SHUT_RDWR)
			socket.close()
		except Exception, e:
			logging.exception(e)

class FaqPortServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
	pass
