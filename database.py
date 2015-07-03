class ServerDatabase:
	def __init__(self):
		self.servers = dict()

	def add_server(self, server_info):
		status = 0
		#print "add_server server_id=" + str(server_info.server_id)
		if server_info.server_id in self.servers:
			status = 1
		self.servers[server_info.server_id] = server_info
		#print "add_server status=" + str(status)
		return status

	def remove_server(self, server_id):
		self.servers.pop(server_id)

	def get_server(self, server_id):
		return self.servers[server_id]

	def get_servers(self):
		return self.servers.values()

server_database = ServerDatabase()
