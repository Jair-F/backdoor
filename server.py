import json
import socket
import ssl
import threading
import time
import sys

import tools.message as message
import tools.my_socket as my_socket

class Server():
    def __init__(self) -> None:
        pass

    def handle(self):
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
    
    return None


if __name__ == "__main__":
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
        thread = threading.Thread(target=handle_server, args=(conn, addr,))
        thread.start()
        client_threads.append(thread)
        #handle_server(conn, addr)
        print(addr)

        if len(client_threads) > 0:
            for thread in client_threads:
                if not thread.is_alive():
                    thread.join()
                    client_threads.remove(thread)
    

    server.close()
