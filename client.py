import json
import socket
import ssl

import tools.message as message
import tools.my_socket as my_socket


if __name__ == "__main__":
    conn = socket.create_connection(("localhost",9090))
    m_socket = my_socket.my_socket(conn)
    msg = m_socket.recv_msg()
    print(F"recieved: {msg}")

    msg = message.message(F"""{{
        "command": "shell",
    "command_attr": {{
    }}
    }}""")
    if m_socket.send_msg(msg):
        print("success sending the message")
    else:
        print("failed to send the message")
