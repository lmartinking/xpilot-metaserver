import base64
import select
import socket
import SocketServer
import threading
import time
from common import *
from player import *
from server import *
from team import *

class ServerPortRequestHandler(SocketServer.BaseRequestHandler):
	def handle(self):
		server_id = IpAddrPort(self.client_address[0], self.client_address[1])

		data = self.request[0].rstrip("\0")
		logging.debug("Received " + data)
		lines = data.split("\n")
		command_type = CommandType(lines)

		handler = ServerPortRequestHandlerImpl(self.server.server_database)
		if command_type.is_add_server():
			server_info = handler.handle_add_server(server_id, lines)
			if server_info:
				self.get_server_rtt(server_info)
				self.server.server_database.write_to_file()
		elif command_type.is_remove_server():
			removed = handler.handle_remove_server(server_id, lines)
			if removed:
				self.server.server_database.write_to_file()
		else:
			logging.debug("Server " + str(server_id) + " : invalid command (Base64) " + base64.b64encode(data))

	def get_server_rtt(self, server_info):
		time_before = time.time()
		sock = self.create_ping_socket()
		received = self.send_and_receive_ping(sock, server_info)
		if received:
			time_after = time.time()
			server_info.rtt = time_after - time_before
			logging.debug("RTT is " + str(server_info.rtt) + " seconds")
		else:
			server_info.rtt = None
			logging.debug("Ping timed out")

	def send_and_receive_ping(self, sock, server_info):
		source_port = sock.getsockname()[1]
		ping_packet = self.create_ping_packet(source_port)
		server_addr = (server_info.server_id.ip_addr, server_info.server_id.port)
		sock.sendto(ping_packet, server_addr)
		ping_packet_str = str(bytearray(ping_packet)).encode('hex')
		logging.debug("Sent ping request " + ping_packet_str)
		ready = select.select([sock], [], [], self.server.ping_timeout)
		if ready[0]:
			recv_data = sock.recv(256)
			recv_data_str = str(bytearray(recv_data)).encode('hex')
			logging.debug("Received ping response " + recv_data_str)
			return True
		return False

	def create_ping_socket(self):
		sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		sock.setblocking(0)
		sock.bind(("", 0))
		return sock

	def create_ping_packet(self, source_port):
		ping_packet = bytearray()
		magic_word = int("0xf4ed", 16)
		magic_word_bytes = reversed(int_to_bytes(magic_word, 4))
		ping_packet.extend(magic_word_bytes)
		ping_packet.insert(len(ping_packet), "p")
		ping_packet.insert(len(ping_packet), 0)
		source_port_bytes = reversed(int_to_bytes(source_port, 2))
		ping_packet.extend(source_port_bytes)
		ping_packet.insert(len(ping_packet), 1)
		return ping_packet

class ServerPortRequestHandlerImpl:
	def __init__(self, server_database):
		self.server_database = server_database

	def handle_add_server(self, server_id, lines):
		server_info = ServerInfo(server_id, lines)
		server_info_prev = self.server_database.get_server(server_id)
		added = False
		if server_info_prev:
			unchanged = server_info_prev.equals_info_from_server(server_info)
			if unchanged:
				logging.debug("Server " + str(server_id) + " : has not changed")
			else:
				# TODO get rid of this when periodic pinging of servers is implemented
				server_info.rtt = server_info_prev.rtt
				self.server_database.add_server(server_info)
				added = True
				logging.info("Server " + str(server_id) + " : updated " + server_info.to_json())
			server_info_prev.update_time = server_info.update_time
		else:
			self.server_database.add_server(server_info)
			added = True
			logging.info("Server " + str(server_id) + " : added " + server_info.to_json())
		return server_info if added else None

	def handle_remove_server(self, server_id, lines):
		removed = self.server_database.remove_server(server_id)
		if removed:
			logging.info("Server " + str(server_id) + " : removed")
		else:
			logging.info("Server " + str(server_id) + " : not in database")
		return removed

class CommandType:
	def __init__(self, subcommands_lines):
		self.type = -1
		if not subcommands_lines:
			return

		first = subcommands_lines[0]
		if first.startswith("add "):
			self.type = 0
		elif first.startswith("server "):
			if len(subcommands_lines) == 2:
				if subcommands_lines[1] == "remove":
					self.type = 1

	def is_add_server(self):
		return self.type == 0

	def is_remove_server(self):
		return self.type == 1

	def is_invalid(self):
		return self.type == -1

class ServerPortServer(SocketServer.ThreadingMixIn, SocketServer.UDPServer):
	pass
