import logging
import select
import socket
import time
from common import *

class ServerPinger:
	def __init__(self, ping_interval, ping_timeout, servers_database):
		self.is_exiting = False
		self.ping_interval = ping_interval
		self.ping_timeout = ping_timeout
		self.servers_database = servers_database
		logging.info("Started server pinger with ping_interval=" + str(ping_interval) + ", ping_timeout=" + str(ping_timeout))

	def handle(self, args):
		while not self.is_exiting:
			pinged_count = self.ping_servers()
			if pinged_count > 0:
				self.servers_database.write_to_file()
			time.sleep(1)

	def ping_servers(self):
		now = time.time()
		pinged_count = 0
		for server_info in self.servers_database.get_servers():
			if now >= server_info.time_last_ping + self.ping_interval:
				rtt = self.get_server_rtt(server_info.server_id)
				if rtt:
					logging.info("Server " + str(server_id) + " : RTT is " + str(rtt) + " seconds")
				else:
					logging.info("Server " + str(server_id) + " : ping timed out")
				server_info.rtt = rtt
				server_info.time_last_ping = time.time()
				pinged_count += 1
		return pinged_count

	def get_server_rtt(self, server_id):
		time_before = time.time()
		sock = self.create_ping_socket()
		received = self.send_and_receive_ping(sock, server_id)
		if received:
			time_after = time.time()
			rtt = time_after - time_before
			return rtt
		return None

	def send_and_receive_ping(self, sock, server_id):
		source_port = sock.getsockname()[1]
		ping_packet = self.create_ping_packet(source_port)
		server_addr = (server_id.ip_addr, server_id.port)
		sock.sendto(ping_packet, server_addr)
		ping_packet_str = str(bytearray(ping_packet)).encode('hex')
		logging.debug("Sent ping request " + ping_packet_str)
		ready = select.select([sock], [], [], self.ping_timeout)
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

