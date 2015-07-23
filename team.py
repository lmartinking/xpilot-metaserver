class TeamInfo:
	def __init__(self, element):
		self.num = None
		self.free_bases = None

		team_tuple = element.split("=")
		if len(team_tuple) < 2:
			return
		
		if self.num == "":
			self.num = -1
		else:
			try:
				self.num = int(team_tuple[0])
			except ValueError:
				return
		
		try:
			self.free_bases = int(team_tuple[1])
		except ValueError:
			return

	def __str__(self):
		if self.num == -1:
			teams_str = "No teams"
		else:
			teams_str = "Team " + str(self.num)
		return teams_str + ", free: " + str(self.free_bases)

	def __eq__(self, other):
		return self.num == other.num and self.free_bases == other.free_bases

	def is_valid(self):
		return (not self.num == None) and (not self.free_bases == None)
