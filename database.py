class ServerDatabase:
	def __init__(self):
		self.servers = dict()

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

server_database = ServerDatabase()
