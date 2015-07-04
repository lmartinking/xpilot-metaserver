
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

		handler = ServerPortRequestHandlerImpl()
		server_id = ServerId(self.client_address[0], self.client_address[1])
		if command_type.is_add_server():
			handler.handle_add_server(server_id, lines)
		elif command_type.is_remove_server():
			handler.handle_remove_server(server_id, lines)

class ServerPortRequestHandlerImpl:
	def handle_add_server(self, server_id, lines):
		server_info = ServerInfo(server_id, lines)
		logging.info("Adding server " + server_info.to_json())
		server_database.add_server(server_info)
		server_database.write_to_file()

	def handle_remove_server(self, server_id, lines):
		server_name = self.get_remove_server_name(lines)
		logging.info("Removing server " + str(server_id) + " with name " + server_name)
		server_database.remove_server(server_id)
		server_database.write_to_file()

	def get_remove_server_name(self, lines):
		if len(lines) != 2 or lines[1] != "remove":
			return None
		elements = lines[0].split(" ")
		if len(elements) != 2:
			return None
		return elements[1]

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
