import logging

class PlayerInfo:
	def __init__(self, player_string):
		self.name = None
		self.realname = None
		self.hostname = None
		self.team_num = None

		if player_string[len(player_string)-1] == "}":
			# extract the team number
			team_begin_idx = player_string.rfind("{")
			if team_begin_idx == -1:
				logging.info("Missing { in the player string: " + player_string)
				return

			begin_idx = team_begin_idx + 1
			end_idx = len(player_string) - 1
			if begin_idx >= end_idx:
				logging.info("Missing team number in the player string: " + player_string)
				return
			try:
				self.team_num = int(player_string[begin_idx:end_idx])
			except ValueError:
				return

		host_begin_idx = player_string.rfind("@", 0, team_begin_idx)
		if host_begin_idx == -1:
			logging.info("Missing @ in the player string: " + player_string)
			return
		host_begin_idx2 = host_begin_idx + 1
		host_end_idx = team_begin_idx
		if host_begin_idx2 >= host_end_idx:
			logging.info("Missing hostname in the player string: " + player_string)
			return
		self.hostname = player_string[host_begin_idx2:host_end_idx]

		realname_begin_idx = player_string.find("=")
		if realname_begin_idx == -1:
			logging.info("Missing = in the player string: " + player_string)
			return
		realname_begin_idx2 = realname_begin_idx + 1
		realname_end_idx = host_begin_idx
		if realname_begin_idx2 >= realname_end_idx:
			logging.info("Missing realname in the player string: " + player_string)
			return
		self.realname = player_string[realname_begin_idx2:realname_end_idx]

		name_end_idx = realname_begin_idx
		if name_end_idx == 0:
			logging.info("Missing name in the player string: " + player_string)
			return
		self.name = player_string[:name_end_idx]

	def __eq__(self, other):
		return self.name == other.name and self.realname == other.realname and self.hostname == other.hostname and self.team_num == other.team_num

	def __str__(self):
		s = self.name + "=" + self.realname + "@" + self.hostname
		if self.team_num != None:
			s += "{" + str(self.team_num) + "}"
		return s

	def is_valid(self):
		# TODO implement
		return True
