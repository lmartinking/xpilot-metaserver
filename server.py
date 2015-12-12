import common
import jsonpickle
import time
from player import *
from team import *

class ServerInfo:
	def __init__(self, server_id, commands):
		self.init_params()

		self.server_id = server_id
		self.update_time = time.time()

		prev_command_str = None

		for command_str in commands:
			if not command_str:
				continue

			elements = command_str.split(" ")
			if elements[0] != "add":
				if prev_command_str == None:
					continue
				command_str = prev_command_str + "\n" + command_str
				elements = command_str.split(" ")
			prev_command_str = command_str

			command = elements[1]
			params = ' '.join(elements[2:])
			if command == "server":
				self.server_name = params
			elif command == "version":
				self.version = params
			elif command == "users":
				try:
					self.num_users = int(params)
				except ValueError:
					pass
			elif command == "map":
				self.map_name = params
			elif command == "sizeMap":
				self.map_size = params
			elif command == "author":
				self.map_author = params
			elif command == "bases":
				try:
					self.num_bases = int(params)
				except ValueError:
					pass
			elif command == "fps":
				try:
					self.fps = int(params)
				except ValueError:
					pass
			elif command == "port":
				# port is saved in server_id
				pass
			elif command == "mode":
				self.game_mode = params
			elif command == "teams":
				try:
					self.num_teams = int(params)
				except ValueError:
					pass
			elif command == "free":
				team_elements = params.split(",")
				for element in team_elements:
					team_info = TeamInfo(element)
					if team_info.is_valid():
						self.num_free_bases_per_team.append(team_info)
			elif command == "timing":
				try:
					self.timing = int(params)
				except ValueError:
					pass
			elif command == "stime":
				try:
					self.start_time = int(time.time()) - int(params)
				except ValueError:
					pass
			elif command == "queue":
				try:
					self.queue = int(params)
				except ValueError:
					pass
			elif command == "sound":
				if params == "yes":
					self.has_sound = True
				else:
					self.has_sound = False
			elif command == "players":
				player_elements = params.split(",")
				for player_element in player_elements:
					player_info = PlayerInfo(player_element)
					if player_info.is_valid():
						self.players.append(player_info)
			elif command == "status":
				self.status = params

	def init_params(self):
		# parameters received from the game server
		self.server_name = None
		self.version = None
		self.map_name = None
		self.map_size = None
		self.map_author = None
		self.num_users = None
		self.num_bases = None
		self.fps = None
		self.game_mode = None
		self.num_teams = None
		self.num_free_bases_per_team = []
		self.timing = None
		self.start_time = None
		self.queue = None
		self.has_sound = None
		self.players = []
		self.status = None

		# parameters computed by the meta server
		self.server_id = None
		self.update_time = None
		self.rtt = None
		self.time_last_ping = 0

	def free_to_string(self):
		s = ""
		for i in range(len(self.num_free_bases_per_team)):
			team = self.num_free_bases_per_team[i]
			if team.num != -1:
				s = s + str(team.num)
			s = s + "=" + str(team.free_bases)
			if i < len(self.num_free_bases_per_team) - 1:
				s += ","
		return s

	def players_to_string(self):
		s = ""
		for i in range(len(self.players)):
			s += str(self.players[i])
			if i < len(self.players) - 1:
				s += ","
		return s

	def to_string_client(self):
		return colon2hyphen(self.version) + ":" + colon2hyphen(self.server_name) + ":" + str(self.server_id.port) + ":" + str(self.num_users) + ":" + colon2hyphen(self.map_name) + ":" + colon2hyphen(self.map_size) + ":" + colon2hyphen(self.map_author) + ":ok:" + str(self.num_bases) + ":" + str(self.fps) + ":" + colon2hyphen(self.players_to_string()) + ":" + self.get_sound_str() + ":" + str(self.get_uptime()) + ":" + str(self.get_num_free_teams()) + ":" + str(self.timing) + ":" + format(self.server_id.ip_addr) + ":" + self.free_to_string() + ":" + str(self.queue)

	def get_num_free_teams(self):
		num_free_teams = 0
		for i in range(len(self.num_free_bases_per_team)):
			team = self.num_free_bases_per_team[i]
			if team.num != -1 and team.free_bases > 0:
				num_free_teams += 1
		return num_free_teams

	def get_uptime(self):
		if self.start_time == None:
			return None
		return int(time.time()) - self.start_time

	def get_time_since_update(self):
		return time.time() - self.update_time

	def get_sound_str(self):
		return "yes" if self.has_sound else "no"

	def is_valid(self):
		# TODO implement
		return True

	def to_json(self):
		return jsonpickle.encode(self)

	# We compare all fields received from the server except uptime.
	# The reason is that we calculate start time based on uptime and sometimes there may be discrepancies by +-1 second, depending on clock skew and lag.
	def equals_info_from_server(self, other):
		return self.server_id == other.server_id and self.server_name == other.server_name and self.version == other.version and self.map_name == other.map_name and self.map_size == other.map_size and self.map_author == other.map_author and self.num_users == other.num_users and self.num_bases == other.num_bases and self.fps == other.fps and self.game_mode == other.game_mode and self.num_teams == other.num_teams and self.num_free_bases_per_team == other.num_free_bases_per_team and self.timing == other.timing and self.queue == other.queue and self.has_sound == other.has_sound and self.players == other.players and self.status == other.status

