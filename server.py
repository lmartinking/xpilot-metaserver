import jsonpickle
import time
from player import *
from team import *

class ServerId:
	def __init__(self, server_ip, server_port):
		self.ip_addr = server_ip
		self.port = server_port

	def __eq__(self, other):
		return (self.ip_addr, self.port) == (other.ip_addr, other.port)

	def __hash__(self):
		return hash((self.ip_addr, self.port))

	def __str__(self):
		return "ip_addr=" + format(self.ip_addr) + " port=" + str(self.port)

class ServerInfo:
	def __init__(self, server_id, commands):
		self.init_params()

		self.server_id = server_id
		self.update_time = int(time.time())

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
					self.start_time = int(params)
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
		self.server_id = None
		self.update_time = None
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

	def free_to_string(self):
		s = ""
		for i in range(len(self.num_free_bases_per_team)):
			team = self.num_free_bases_per_team[i]
			s = s + str(team.num) + "=" + str(team.free_bases)
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
		return self.version + ":" + self.server_name + ":" + str(self.server_id.port) + ":" + str(self.num_users) + ":" + self.map_name + ":" + self.map_size + ":" + self.map_author + ":ok:" + str(self.num_bases) + ":" + str(self.fps) + "::" + self.get_sound_str() + ":" + str(self.get_uptime()) + ":" + str(len(self.num_free_bases_per_team)) + ":" + str(self.timing) + ":" + format(self.server_id.ip_addr) + ":" + self.free_to_string() + ":" + str(self.queue)

	def get_uptime(self):
		if self.start_time == None:
			return None
		return int(time.time()) - self.start_time

	def get_time_since_update(self):
		return int(time.time()) - self.update_time

	def get_sound_str(self):
		return "yes" if self.has_sound else "no"

	def is_valid(self):
		# TODO implement
		return True

	def to_json(self):
		return jsonpickle.encode(self)
