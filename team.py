class TeamInfo:
	def __init__(self, element):
		self.valid = False
		self.num = None
		self.free_bases = None

		team_tuple = element.split("=")
		if len(team_tuple) < 2:
			return
		try:
			self.num = int(team_tuple[0])
		except ValueError:
			return
		try:
			self.free_bases = int(team_tuple[1])
		except ValueError:
			return
		self.valid = True

	def __str__(self):
		return "Team " + str(self.num) + ", free: " + str(self.free_bases)

	def __eq__(self, other):
		return self.num == other.num and self.free_bases == other.free_bases

	def is_valid(self):
		return self.valid
