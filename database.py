import time

class ServerDatabase:
	def __init__(self):
		self.servers = dict()
		self.is_exiting = False
		self.server_timeout = 5*60;

	def add_server(self, server_info):
		status = 0
		if server_info.server_id in self.servers:
			status = 1
		self.servers[server_info.server_id] = server_info
		return status

	def remove_server(self, server_id):
		self.servers.pop(server_id)

	def get_server(self, server_id):
		return self.servers[server_id]

	def get_servers(self):
		return self.servers.values()

	def handle(self, args):
		server_timeout_counter = 0
		while not self.is_exiting:
			if server_timeout_counter >= self.server_timeout:
				self.flush_timed_out_servers()
				server_timeout_counter = 0
			time.sleep(1)
			server_timeout_counter += 1

	def flush_timed_out_servers(self):
		for server_info in self.servers.values():
			if server_info.get_time_since_update() >= self.server_timeout:
				print "Timed out server " + str(server_info.server_id)
				self.remove_server(server_info.server_id)

server_database = ServerDatabase()
