import base64
import socketserver
import threading
import time
from common import *
from player import *
from server import *
from team import *

class ServerPortRequestHandler(socketserver.BaseRequestHandler):
        def handle(self):
                try:
                        server_id = IpAddrPort(self.client_address[0], self.client_address[1])

                        data = self.request[0].decode('utf-8').rstrip('\0')
                        #data = str(bytes)
                        logging.debug("Received " + data)
                        lines = data.split("\n")
                        command_type = CommandType(lines)

                        handler = ServerPortRequestHandlerImpl(self.server.server_database)
                        if command_type.is_add_server():
                                server_info = handler.handle_add_server(server_id, lines)
                                if server_info:
                                        #self.get_server_rtt(server_info)
                                        self.server.server_database.write_to_file()
                        elif command_type.is_remove_server():
                                removed = handler.handle_remove_server(server_id, lines)
                                if removed:
                                        self.server.server_database.write_to_file()
                        else:
                                logging.info("Server " + str(server_id) + " : invalid command (Base64) " + str(base64.b64encode(data)))
                except Exception as e:
                        logging.exception(e)

class ServerPortRequestHandlerImpl:
        def __init__(self, server_database):
                self.server_database = server_database

        def handle_add_server(self, server_id, lines):
                server_info = ServerInfo(server_id, lines)
                server_info_prev = self.server_database.get_server(server_id)
                added = False
                if server_info_prev:
                        unchanged = server_info_prev.equals_info_from_server(server_info)
                        if unchanged:
                                logging.debug("Server " + str(server_id) + " : has not changed")
                        else:
                                # TODO get rid of this when periodic pinging of servers is implemented
                                server_info.rtt = server_info_prev.rtt
                                self.server_database.add_server(server_info)
                                added = True
                                logging.info("Server " + str(server_id) + " : updated " + server_info.to_json())
                        server_info_prev.update_time = server_info.update_time
                else:
                        self.server_database.add_server(server_info)
                        added = True
                        logging.info("Server " + str(server_id) + " : added " + server_info.to_json())
                return server_info if added else None

        def handle_remove_server(self, server_id, lines):
                removed = self.server_database.remove_server(server_id)
                if removed:
                        logging.info("Server " + str(server_id) + " : removed")
                else:
                        logging.info("Server " + str(server_id) + " : not in database")
                return removed

class CommandType:
        def __init__(self, subcommands_lines):
                self.type = -1
                if not subcommands_lines:
                        return

                first = subcommands_lines[0]
                if first.startswith("add "):
                        self.type = 0
                elif first.startswith("server "):
                        if len(subcommands_lines) == 2:
                                if subcommands_lines[1] == "remove":
                                        self.type = 1

        def is_add_server(self):
                return self.type == 0

        def is_remove_server(self):
                return self.type == 1

        def is_invalid(self):
                return self.type == -1

class ServerPortServer(socketserver.ThreadingMixIn, socketserver.UDPServer):
        pass
