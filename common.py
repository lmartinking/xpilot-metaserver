class IpAddrPort:
	def __init__(self, server_ip, server_port):
		self.ip_addr = server_ip
		self.port = server_port

	def __eq__(self, other):
		return (self.ip_addr, self.port) == (other.ip_addr, other.port)

	def __hash__(self):
		return hash((self.ip_addr, self.port))

	def __str__(self):
		return format(self.ip_addr) + ":" + str(self.port)
