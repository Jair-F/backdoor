import socket
import tools.message as message

SOCK_MSG_LEN_IND = 4 # in bytes
SOCK_STR_ENCODING = "UTF-8"

class my_socket:
    def __init__(self, sock:socket.socket):
        """
            ``sock`` already setup and connected socket object ready to send and recieve data
        """
        self.socket = sock
        # self.socket.settimeout(0) # - using default timeout

    def recv_msg(self) -> message.message:
        """
            ``return`` a message object or it raises an BrokenPipeError if connection broken
        """
        msg_len:int = int.from_bytes(self.socket.recv(SOCK_MSG_LEN_IND), signed=True)

        recv = self.socket.recv(msg_len)
        if len(recv) == 0:
            raise BrokenPipeError("Connection broken")
        
        msg = message.message(recv.decode())
        msg.command = "Hallo"
        if msg.command == "connection_close":
            return None
        else:
            return msg

            
    def send_msg(self, msg:message.message) -> bool:
        """
            ``return`` true on success, false on failure
        """
        str_msg = str(msg)
        byte_msg = str_msg.encode()
        msg_size:int = len(byte_msg)
        print(msg_size)

        """
            we first send 4 bytes only positive integer which sends 
            the byte length of the following msg_str
        """
        byte_msg_size = int.to_bytes(msg_size, length=SOCK_MSG_LEN_IND, signed=True)

        try:
            sent_data_counter = 0
            while sent_data_counter < SOCK_MSG_LEN_IND:
                recvd_bytes = self.socket.send(byte_msg_size[sent_data_counter:])
                if recvd_bytes == 0:
                    raise BrokenPipeError("Connection broken")
                sent_data_counter += recvd_bytes

            #self.socket.sendall(int.to_bytes(msg_size, length=4), SOCK_MSG_LEN_IND)
            
            sent_data_counter = 0
            while sent_data_counter < msg_size:
                recvd_bytes = self.socket.send(byte_msg[sent_data_counter:])
                if recvd_bytes == 0:
                    raise BrokenPipeError("Connection broken")
                sent_data_counter += recvd_bytes
            #self.socket.sendall(byte_msg, msg_size)
        except BrokenPipeError as err:
            print(F"CONNECTION-ERROR: {str(err)}")
            return False
        except socket.error as err:
            print(F'SOCKET-ERROR: sending data: {str(err)}')
            return False

        return True
    

if __name__ == "__main__":
    msg_size = 2930498288
    print(msg_size.bit_length()/8)