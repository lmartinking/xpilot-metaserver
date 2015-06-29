#!/usr/bin/python

import socket
import threading
import SocketServer

class PlayerInfo:
	def __init__(self, player_string):
		self.team_num = None
		if player_string[len(player_string)-1] == "}":
			# extract the team number
			team_begin_idx = player_string.rfind("{")
			if team_begin_idx == -1:
				print "Missing { in the player string: " + player_string
				return

			begin_idx = team_begin_idx + 1
			end_idx = len(player_string) - 2
			if begin_idx >= end_idx:
				print "Missing team number in the player string: " + player_string
				return

			self.team_num = int(player_string[begin_idx:end_idx])

		host_begin_idx = player_string.rfind("@", 0, team_begin_idx)
		if host_begin_idx == -1:
			print "Missing @ in the player string: " + player_string
			return
		host_begin_idx2 = host_begin_idx + 1
		host_end_idx = team_begin_idx - 1
		if host_begin_idx2 >= host_end_idx:
			print "Missing hostname in the player string: " + player_string
			return
		self.hostname = player_string[host_begin_idx2:host_end_idx]

		realname_begin_idx = player_string.find("=")
		if realname_begin_idx == -1:
			print "Missing = in the player string: " + player_string
			return
		realname_begin_idx2 = realname_begin_idx + 1
		realname_end_idx = host_begin_idx - 1
		if realname_begin_idx2 >= realname_end_idx:
			print "Missing realname in the player string: " + player_string
			return
		self.realname = player_string[realname_begin_idx2:realname_end_idx]

		name_end_idx = realname_begin_idx - 1
		if name_end_idx == 0:
			print "Missing name in the player string: " + player_string
			return
		self.name = player_string[:name_end_idx]

	def to_string(self):
		s = self.name + "=" + self.realname + "@" + self.hostname
		if self.team_num != None:
			s += "{" + str(self.team_num) + "}"
		return s

class ServerInfo:
	def __init__(self, commands):
		self.num_free_bases_per_team = dict()
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
				self.users = int(params)
			elif command == "map":
				self.map_name = params
			elif command == "sizeMap":
				self.map_size = params
			elif command == "author":
				self.author = params
			elif command == "bases":
				self.num_bases = int(params)
			elif command == "fps":
				self.fps = int(params)
			elif command == "port":
				self.port = int(params)
			elif command == "mode":
				self.game_mode = params
			elif command == "teams":
				self.num_teams = int(params)
			elif command == "free":
				team_elements = params.split(",")
				for element in team_elements:
					team_tuple = element.split("=")
					if len(team_tuple) < 2:
						print "Invalid team tuple: " + element
						continue
					team_num = team_tuple[0]
					num_free_bases = int(team_tuple[1])
					self.num_free_bases_per_team[team_num] = num_free_bases
			elif command == "timing":
				self.timing = int(params)
			elif command == "stime":
				self.start_time = int(params)
			elif command == "queue":
				self.queue = int(params)
			elif command == "sound":
				self.has_sound = bool(params)
			elif command == "players":
				player_elements = params.split(",")
				for player_element in player_elements:
					player_info = PlayerInfo(player_element)
					self.players.append(player_info)
			elif command == "status":
				self.status = params

	def free_to_string(self):
		s = ""
		for i in self.num_free_bases_per_team:
			s = s + str(i) + "=" + str(self.num_free_bases_per_team[i]) + ","
		return s

	def players_to_string(self):
		s = ""
		for player in self.players:
			s += self.players_to_string() + ","
		return s

	def to_string(self):
		return "server_name: " + self.server_name + " version: " + self.version + " users: " + str(self.users) + " map: " + self.map_name + " sizeMap: " + self.map_size + " author: " + self.author + " bases: " + str(self.num_bases) + " fps: " + str(self.fps) + " port: " + str(self.port) + " mode: " + self.game_mode + " teams: " + str(self.num_teams) + " free: " + self.free_to_string() + " timing: " + str(self.timing) + " stime: " + str(self.start_time) + " queue: " + str(self.queue) + " sound: " + str(self.has_sound) + " players: " + self.players_to_string() + " status: " + self.status


def add_server(commands):
	server_def = ServerInfo(commands)
	print "Adding server " + server_def.to_string()
	# TODO add server to database

def remove_server(commands):
	if len(commands) < 2 or commands[1] != "remove":
		print "Invalid syntax:"
		print commands
		return
	elements = commands[0].split(" ")
	if len(elements) < 2:
		print "Invalid syntax:"
		print commands
		return
	server_name = elements[1]
	print "Removing server " + server_name
	# TODO remove server from database

def is_command(commands, expected_command):
	if len(commands) < 1:
		print "Not enough commands"
		return False
	elements = commands[0].split(" ")
	return len(elements) > 1 and elements[0] == expected_command

class ServerPortRequestHandler(SocketServer.BaseRequestHandler):
	def handle(self):
		data = self.request[0]
		socket = self.request[1]
		print "{} wrote:".format(self.client_address[0])
		print data

		commands = data.split("\n")
		if is_command(commands, "add"):
			add_server(commands)
		elif is_command(commands, "server"):
			remove_server(commands)

class ServerPortServer(SocketServer.ThreadingMixIn, SocketServer.UDPServer):
	pass
