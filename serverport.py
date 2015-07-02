#!/usr/bin/python

import socket
import threading
import SocketServer

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
				print "Missing { in the player string: " + player_string
				return

			begin_idx = team_begin_idx + 1
			end_idx = len(player_string) - 1
			if begin_idx >= end_idx:
				print "Missing team number in the player string: " + player_string
				return
			try:
				self.team_num = int(player_string[begin_idx:end_idx])
			except ValueError:
				return

		host_begin_idx = player_string.rfind("@", 0, team_begin_idx)
		if host_begin_idx == -1:
			print "Missing @ in the player string: " + player_string
			return
		host_begin_idx2 = host_begin_idx + 1
		host_end_idx = team_begin_idx
		if host_begin_idx2 >= host_end_idx:
			print "Missing hostname in the player string: " + player_string
			return
		self.hostname = player_string[host_begin_idx2:host_end_idx]

		realname_begin_idx = player_string.find("=")
		if realname_begin_idx == -1:
			print "Missing = in the player string: " + player_string
			return
		realname_begin_idx2 = realname_begin_idx + 1
		realname_end_idx = host_begin_idx
		if realname_begin_idx2 >= realname_end_idx:
			print "Missing realname in the player string: " + player_string
			return
		self.realname = player_string[realname_begin_idx2:realname_end_idx]

		name_end_idx = realname_begin_idx
		if name_end_idx == 0:
			print "Missing name in the player string: " + player_string
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
		return True

class ServerInfo:
	def __init__(self, commands):
		self.num_free_bases_per_team = []
		self.players = []

		for command_str in commands:
			if not command_str:
				continue
			elements = command_str.split(" ")
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
				try:
					self.port = int(params)
				except ValueError:
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

	def free_to_string(self):
		s = ""
		for i in range(self.num_free_bases_per_team):
			s = s + str(i) + "=" + str(self.num_free_bases_per_team[i])
			if i < len(self.num_free_bases_per_team) - 1:
				s += ","
		return s

	def players_to_string(self):
		s = ""
		for i in range(self.players):
			s += str(self.players[i])
			if i < len(self.players) - 1:
				s += ","
		return s

	def __str__(self):
		return "server_name: " + self.server_name + " version: " + self.version + " users: " + str(self.num_users) + " map: " + self.map_name + " sizeMap: " + self.map_size + " author: " + self.map_author + " bases: " + str(self.num_bases) + " fps: " + str(self.fps) + " port: " + str(self.port) + " mode: " + self.game_mode + " teams: " + str(self.num_teams) + " free: " + self.free_to_string() + " timing: " + str(self.timing) + " stime: " + str(self.start_time) + " queue: " + str(self.queue) + " sound: " + str(self.has_sound) + " players: " + self.players_to_string() + " status: " + self.status

	def is_valid(self):
		return True

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

class ServerPortRequestHandler(SocketServer.BaseRequestHandler):
	def handle(self):
		data = self.request[0]
		socket = self.request[1]
		print "Packet from " + format(self.client_address[0])

		lines = data.split("\n")
		command_type = CommandType(lines)

		handler = ServerPortRequestHandlerImpl()
		if command_type.is_add_server():
			handler.handle_add_server(lines)
		elif command_type.is_remove_server():
			handler.handle_remove_server(lines)

class ServerPortRequestHandlerImpl:
	def handle_add_server(self, lines):
		server_def = ServerInfo(lines)
		print "Adding server " + str(server_def)
		# TODO add server to database

	def handle_remove_server(self, lines):
		server_name = self.get_remove_server_name(lines)
		print "Removing server " + server_name
		# TODO remove server from database

	def get_remove_server_name(self, lines):
		if len(lines) != 2 or lines[1] != "remove":
			return None
		elements = lines[0].split(" ")
		if len(elements) != 2:
			return None
		return elements[1]

class CommandType:
	def __init__(self, subcommands_lines):
		self.type = -1
		if not subcommands_lines:
			return

		first = subcommands_lines[0]
		if first.startswith("add "):
			self.type = 0
		elif first.startswith("server "):
			if len(subcommands_lines) == 2 and subcommands_lines[1] == "remove":
				self.type = 1

	def is_add_server(self):
		return self.type == 0

	def is_remove_server(self):
		return self.type == 1

	def is_invalid(self):
		return self.type == -1

class ServerPortServer(SocketServer.ThreadingMixIn, SocketServer.UDPServer):
	pass
