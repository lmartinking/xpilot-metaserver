
import socket
import threading
import SocketServer
from server import *
from player import *
from team import *
from database import *

class ServerPortRequestHandler(SocketServer.BaseRequestHandler):
	def handle(self):
		logging.info("Incoming server " + format(self.client_address[0]) + ":" + str(self.client_address[1]))

		data = self.request[0]
		lines = data.split("\n")
		command_type = CommandType(lines)

		server_id = ServerId(self.client_address[0], self.client_address[1])
		handler = ServerPortRequestHandlerImpl()
		if command_type.is_add_server():
			handler.handle_add_server(server_id, lines)
		elif command_type.is_remove_server():
			handler.handle_remove_server(server_id, lines)

class ServerPortRequestHandlerImpl:
	def handle_add_server(self, server_id, lines):
		server_info = ServerInfo(server_id, lines)
		server_info_prev = server_database.get_server(server_id)
		database_changed = False
		if server_info_prev:
			unchanged = server_info_prev.equals_info_from_server(server_info)
			if not unchanged:
				server_database.add_server(server_info)
				database_changed = True
				logging.info("Updated server " + server_info.to_json())
		else:
			server_database.add_server(server_info)
			database_changed = True
			logging.info("Added server " + server_info.to_json())
		if database_changed:
			server_database.write_to_file()

	def handle_remove_server(self, server_id, lines):
		removed = server_database.remove_server(server_id)
		if removed:
			logging.info("Removed server " + str(server_id))
			server_database.write_to_file()
		else:
			logging.info("Server " + str(server_id) + " not in database")

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
