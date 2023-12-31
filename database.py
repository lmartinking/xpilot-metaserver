import jsonpickle
import json
import logging
import time

class ServerDatabase:
        def __init__(self, server_timeout, servers_file):
                self.servers = dict()
                self.is_exiting = False
                self.server_timeout = server_timeout;
                self.servers_file = servers_file

        def add_server(self, server_info):
                self.servers[server_info.server_id] = server_info

        def remove_server(self, server_id):
                removed = False
                try:
                        self.servers.pop(server_id)
                        removed = True
                except KeyError:
                        pass
                return removed

        def get_server(self, server_id):
                server_info = None
                try:
                        server_info = self.servers[server_id]
                except KeyError:
                        pass
                return server_info

        def get_servers(self):
                return list(self.servers.values())

        def handle(self, args):
                server_timeout_counter = 0
                while not self.is_exiting:
                        if server_timeout_counter >= self.server_timeout:
                                flushed_count = self.flush_timed_out_servers()
                                if flushed_count > 0:
                                        self.write_to_file()
                                server_timeout_counter = 0
                        time.sleep(1)
                        server_timeout_counter += 1

        def flush_timed_out_servers(self):
                flushed_count = 0
                for server_info in self.get_servers():
                        if server_info.get_time_since_update() >= self.server_timeout:
                                logging.info("Timed out server " + str(server_info.server_id))
                                self.remove_server(server_info.server_id)
                                flushed_count += 1
                return flushed_count

        def write_to_file(self):
                file = open(self.servers_file, "w")
                json_obj = jsonpickle.encode(self.get_servers())
                #json_str = json.dumps(json_obj)
                logging.info("json_str: " + json_obj)
                file.write(json_obj)#str.encode("utf-8"))
                file.close()
                logging.debug("Written database to file")
