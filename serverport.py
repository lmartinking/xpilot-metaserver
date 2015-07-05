import base64
import socket
import SocketServer
import threading
from common import *
from player import *
from server import *
from team import *

class ServerPortRequestHandler(SocketServer.BaseRequestHandler):
	def handle(self):
		server_id = IpAddrPort(self.client_address[0], self.client_address[1])

		data = self.request[0]
		lines = data.split("\n")
		command_type = CommandType(lines)

		handler = ServerPortRequestHandlerImpl(self.server.server_database)
		if command_type.is_add_server():
			handler.handle_add_server(server_id, lines)
		elif command_type.is_remove_server():
			handler.handle_remove_server(server_id, lines)
		else:
			logging.debug("Server " + str(server_id) + " : invalid command (Base64) " + base64.b64encode(data))

class ServerPortRequestHandlerImpl:
	def __init__(self, server_database):
		self.server_database = server_database

	def handle_add_server(self, server_id, lines):
		server_info = ServerInfo(server_id, lines)
		server_info_prev = self.server_database.get_server(server_id)
		database_changed = False
		if server_info_prev:
			unchanged = server_info_prev.equals_info_from_server(server_info)
			if unchanged:
				logging.debug("Server " + str(server_id) + " : has not changed")
			else:
				self.server_database.add_server(server_info)
				database_changed = True
				logging.info("Server " + str(server_id) + " : updated " + server_info.to_json())
		else:
			self.server_database.add_server(server_info)
			database_changed = True
			logging.info("Server " + str(server_id) + " : added " + server_info.to_json())
		if database_changed:
			self.server_database.write_to_file()

	def handle_remove_server(self, server_id, lines):
		removed = self.server_database.remove_server(server_id)
		if removed:
			logging.info("Server " + str(server_id) + " : removed")
			self.server_database.write_to_file()
		else:
			logging.info("Server " + str(server_id) + " : not in database")

class CommandType:
	def __init__(self, subcommands_lines):
		self.type = -1
		if not subcommands_lines:
			return

		first = subcommands_lines[0]
		if first.startswith("add "):
			self.type = 0
		elif first.startswith("server "):
			if len(subcommands_lines) == 2 and subcommands_lines[1] == "remove":
				self.type = 1

	def is_add_server(self):
		return self.type == 0

	def is_remove_server(self):
		return self.type == 1

	def is_invalid(self):
		return self.type == -1

class ServerPortServer(SocketServer.ThreadingMixIn, SocketServer.UDPServer):
	pass
