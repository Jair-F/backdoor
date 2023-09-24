import socket
import tools.message as message

"""
    A socket msg is build like this
    
    one byte            4 bytes integer which hold the         the message
    of msg_header       size of the sent message              itself
       |                             |                               |
       v                             v                               v
    00000000        00000000 00000000 00000000 00000000         01010101010
"""

SOCK_MSG_HEADER = 1
SOCK_MSG_LEN_IND = 4 # in bytes
SOCK_STR_ENCODING = "UTF-8"

# message header codes for communication between the sockets - closing ...
SOCK_HEADER_NORMAL_MSG = 0b00000000
SOCK_HEADER_CONNECTION_CLOSE = 0b00000001

class my_socket:
    """
        socket for messages from messgage module
    """
    def __init__(self, sock:socket.socket):
        """
            ``sock`` already setup and connected socket object ready to send and recieve data
        """
        if sock == None:
            pass # nothing until now
        else:
            self.__is_closed = False
            self.socket = sock
            # self.socket.settimeout(0) # - using default timeout

    def __recv(self, size:int) -> bytes:
        """
            ``return`` the recieved data in bytes. None if the socket is closed.
            ``size`` the number of bytes which we are expected to recieve

            raises exception if an error occours
        """
        if self.__is_closed:
            return None
        else:
            data:bytes = bytes() # the data object we return after reciving
            recv:bytes = None # bytes we recieved in the last recv period
            recvd_bytes:int = 0
            while recvd_bytes < size:
                recv = self.socket.recv(size - recvd_bytes)
                if recv == 0:
                    self.__is_closed = True
                    raise BrokenPipeError("Connection broken")
                recvd_bytes += len(recv)
                data += recv
            return data

    def __send(self, data:bytes) -> bool:
        """
            ``return`` True if the send was successfull, False if failed

            raises exception if an error occours
        """
        sent_bytes:int = 0
        data_size = len(data)

        while sent_bytes < data_size:
            sent = self.socket.send(data[sent_bytes:])
            if sent == 0:
                self.__is_closed = True
                raise BrokenPipeError("Connection brocken")
            sent_bytes += sent

        return True

    def recv_msg(self) -> message.message:
        """
            ``return`` a message object or None if the socket is closed
            
            raises an BrokenPipeError if connection broken
        """
        # receiving the msg header
        msg_header:bytes = self.__recv(SOCK_MSG_HEADER) # one byte of header

        if msg_header == SOCK_HEADER_CONNECTION_CLOSE:
            self.__is_closed = True
            return None
        else:
            # receiving the size of the msg
            msg_size:int = int.from_bytes(self.__recv(SOCK_MSG_LEN_IND), signed=True) # the size in bytes
            # receiving the msg itself
            msg:str = self.__recv(msg_size).decode(SOCK_STR_ENCODING) # the message itself

            return message.message(msg)

            
    def send_msg(self, msg:message.message) -> bool:
        """
            ``return`` true on success, false on failure
        """
        success:bool = True
        byte_msg:bytes = str(msg).encode(SOCK_STR_ENCODING)

        # sending the msg header
        if not self.__send(int.to_bytes(SOCK_HEADER_NORMAL_MSG, length=1, signed=True)): success = False

        # sending the msg size
        if not self.__send(int.to_bytes(len(byte_msg), length=4, signed=True)) : success = False

        # sending the msg
        if not self.__send(byte_msg): success = False

        if not success:
            self.__is_closed = True

        return success


    def close(self) -> bool:
        """
            ``return`` True if the socket managed to notify the other side about the close, False if not
        """
        success:bool = self.__send(int.to_bytes(SOCK_HEADER_CONNECTION_CLOSE, length=1, signed=True))
        # send a close msg to the other socket
        self.socket.shutdown()
        self.socket.close()
        self.__is_closed = True
        return success
    
    @property
    def is_closed(self) -> bool:
        """
            ``return`` True if the connection is closed. False if not
        """
        return self.__is_closed
