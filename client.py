import json
import socket
import ssl
import sys

import tools.message as message
import tools.my_socket as my_socket


if __name__ == "__main__":
    conn = socket.create_connection(("localhost",9090))
    m_socket = my_socket.my_socket(conn)
    
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
