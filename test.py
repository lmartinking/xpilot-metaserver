#!/usr/bin/python

import unittest
from serverport import *

class TestCommandTypeAddServer(unittest.TestCase):
	def setUp(self):
		data = "add server localhost"
		self.lines = data.split("\n")

	def test(self):
		command_type = CommandType(self.lines)
		self.assertTrue(command_type.is_add_server())

class TestPlayerInfoServerName(unittest.TestCase):
	def setUp(self):
		self.server_name = "localhost"
		data = "add server " + self.server_name
		self.lines = data.split("\n")

	def test(self):
		server = ServerInfo(None, self.lines)
		self.assertEqual(server.server_name, self.server_name)

class TestPlayerInfoNumUsers(unittest.TestCase):
	def setUp(self):
		self.num_users = 2
		data = "add users " + str(self.num_users)
		self.lines = data.split("\n")

	def test(self):
		server = ServerInfo(None, self.lines)
		self.assertEqual(server.num_users, self.num_users)

class TestPlayerInfoVersion(unittest.TestCase):
	def setUp(self):
		self.version = "1.4.6fxi~7"
		data = "add version " + self.version
		self.lines = data.split("\n")

	def test(self):
		server = ServerInfo(None, self.lines)
		self.assertEqual(server.version, self.version)

class TestPlayerInfoMapName(unittest.TestCase):
	def setUp(self):
		self.map_name = "Xpilot-Tournament Map (Blood's Music)"
		data = "add map " + self.map_name
		self.lines = data.split("\n")

	def test(self):
		server = ServerInfo(None, self.lines)
		self.assertEqual(server.map_name, self.map_name)

class TestPlayerInfoMapSize(unittest.TestCase):
	def setUp(self):
		self.map_size = "100x100"
		data = "add sizeMap " + self.map_size
		self.lines = data.split("\n")

	def test(self):
		server = ServerInfo(None, self.lines)
		self.assertEqual(server.map_size, self.map_size)

class TestPlayerInfoMapAuthor(unittest.TestCase):
	def setUp(self):
		self.map_author = "\"Patrick Kenny - pkenny@eecs.umich.edu\""
		data = "add author " + self.map_author
		self.lines = data.split("\n")

	def test(self):
		server = ServerInfo(None, self.lines)
		self.assertEqual(server.map_author, self.map_author)

class TestPlayerInfoFps(unittest.TestCase):
	def setUp(self):
		self.fps = 50
		data = "add fps " + str(self.fps)
		self.lines = data.split("\n")

	def test(self):
		server = ServerInfo(None, self.lines)
		self.assertEqual(server.fps, self.fps)

@unittest.skip("")
class TestPlayerInfoPort(unittest.TestCase):
	def setUp(self):
		self.port = 15345
		data = "add port " + str(self.port)
		self.lines = data.split("\n")

	def test(self):
		server = ServerInfo(None, self.lines)
		self.assertEqual(server.port, self.port)

class TestPlayerInfoMode(unittest.TestCase):
	def setUp(self):
		self.game_mode = "ok"
		data = "add mode " + self.game_mode
		self.lines = data.split("\n")

	def test(self):
		server = ServerInfo(None, self.lines)
		self.assertEqual(server.game_mode, self.game_mode)

class TestPlayerInfoNumTeams(unittest.TestCase):
	def setUp(self):
		self.num_teams = 2
		data = "add teams " + str(self.num_teams)
		self.lines = data.split("\n")

	def test(self):
		server = ServerInfo(None, self.lines)
		self.assertEqual(server.num_teams, self.num_teams)

class TestPlayerInfoNumFreeBasesPerTeam(unittest.TestCase):
	def setUp(self):
		data = "add free 2=4,4=4"
		self.expected = []
		team1 = TeamInfo("2=4")
		team2 = TeamInfo("4=4")
		self.expected.append(team1)
		self.expected.append(team2)
		self.lines = data.split("\n")

	def test(self):
		server = ServerInfo(None, self.lines)
		self.assertEqual(server.num_free_bases_per_team, self.expected)

class TestTeamInfo(unittest.TestCase):
	def setUp(self):
		pass

	def test(self):
		team = TeamInfo("2=4")
		self.assertEqual(team.num, 2)
		self.assertEqual(team.free_bases, 4)
		self.assertTrue(team.is_valid())

class TestTeamInfoInvalid(unittest.TestCase):
	def setUp(self):
		pass

	def test(self):
		team = TeamInfo("?")
		self.assertFalse(team.is_valid())

class TestPlayerInfoTiming(unittest.TestCase):
	def setUp(self):
		self.timing = 0
		data = "add timing " + str(self.timing)
		self.lines = data.split("\n")

	def test(self):
		server = ServerInfo(None, self.lines)
		self.assertEqual(server.timing, self.timing)

class TestPlayerInfoStartTime(unittest.TestCase):
	def setUp(self):
		self.start_time = 0
		data = "add stime " + str(self.start_time)
		self.lines = data.split("\n")

	def test(self):
		server = ServerInfo(None, self.lines)
		self.assertEqual(server.start_time, self.start_time)

class TestPlayerInfoQueue(unittest.TestCase):
	def setUp(self):
		self.queue = 0
		data = "add queue " + str(self.queue)
		self.lines = data.split("\n")

	def test(self):
		server = ServerInfo(None, self.lines)
		self.assertEqual(server.queue, self.queue)

class TestPlayerInfoSoundNo(unittest.TestCase):
	def setUp(self):
		self.has_sound = False
		data = "add sound no"
		self.lines = data.split("\n")

	def test(self):
		server = ServerInfo(None, self.lines)
		self.assertEqual(server.has_sound, self.has_sound)

class TestPlayerInfoSoundNoInvalid(unittest.TestCase):
	def setUp(self):
		self.has_sound = False
		data = "add sound "
		self.lines = data.split("\n")

	def test(self):
		server = ServerInfo(None, self.lines)
		self.assertEqual(server.has_sound, self.has_sound)

class TestPlayerInfoSoundYes(unittest.TestCase):
	def setUp(self):
		self.has_sound = True
		data = "add sound yes"
		self.lines = data.split("\n")

	def test(self):
		server = ServerInfo(None, self.lines)
		self.assertEqual(server.has_sound, self.has_sound)

class TestPlayerInfoSound(unittest.TestCase):
	def setUp(self):
		self.has_sound = False
		data = "add sound no"
		self.lines = data.split("\n")

	def test(self):
		server = ServerInfo(None, self.lines)
		self.assertEqual(server.has_sound, self.has_sound)

class TestPlayerInfoStatus(unittest.TestCase):
	def setUp(self):
		self.status = "SERVER VERSION...: 1.4.6fxi~7\nSTATUS...........: ok\nMAX SPEED........: 50 fps\nWORLD (100x100)..: Xpilot-Tournament Map (Blood's Music)\nAUTHOR.....: \"Patrick Kenny - pkenny@eecs.umich.edu\"\nPLAYERS ( 0/ 8)..:"
		data = "add status " + self.status
		self.lines = data.split("\n")

	def test(self):
		server = ServerInfo(None, self.lines)
		self.assertEqual(server.status, self.status)

class TestPlayerInfoPlayers(unittest.TestCase):
	def setUp(self):
		players_str = "Player1=test@xpilot.org{2},Player2=test@xpilot.org{4}"
		data = "add players " + players_str
		self.players = []
		players_str_list = players_str.split(",")
		self.players.append(PlayerInfo(players_str_list[0]))
		self.players.append(PlayerInfo(players_str_list[1]))
		self.lines = data.split("\n")

	def test(self):
		server = ServerInfo(None, self.lines)
		self.assertEqual(server.players, self.players)

class TestPlayerInfo(unittest.TestCase):
	def setUp(self):
		pass

	def test(self):
		player = PlayerInfo("Player1=test@xpilot.org{2}")
		self.assertEqual(player.name, "Player1")
		self.assertEqual(player.realname, "test")
		self.assertEqual(player.hostname, "xpilot.org")
		self.assertEqual(player.team_num, 2)

class TestCommandTypeRemoveServer(unittest.TestCase):
	def setUp(self):
		data = "server localhost\nremove"
		self.lines = data.split("\n")

	def test(self):
		command_type = CommandType(self.lines)
		self.assertTrue(command_type.is_remove_server())

class TestCommandTypeEmptyInvalid(unittest.TestCase):
	def setUp(self):
		data = ""
		self.lines = data.split("\n")

	def test(self):
		command_type = CommandType(self.lines)
		self.assertTrue(command_type.is_invalid())
		
class TestCommandTypeUnknownInvalid(unittest.TestCase):
	def setUp(self):
		data = "xxunknown_stringxx"
		self.lines = data.split("\n")

	def test(self):
		command_type = CommandType(self.lines)
		self.assertTrue(command_type.is_invalid())

if __name__ == "__main__":
	unittest.main()
