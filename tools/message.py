import copy
import json

class message:
    def __init__(self, msg):
        if isinstance(msg, str):
            self.msg = json.loads(msg)
        elif isinstance(msg, list) or isinstance(msg, tuple) or isinstance(msg, dict):
            self.msg = copy.deepcopy(msg)

    def __str__(self) -> str:
        """ 
            ``return`` returns the set msg as a string
        """
        msg = json.dumps(self.msg, indent=None, separators=(',', ':'))
        return msg
    
    @property
    def msg(self, msg:dict) -> dict:
        if msg != None:
            self.msg = msg
        else:
            raise ValueError("msg not set")

    @property
    def msg(self) -> dict:
        return self.msg
    
    @property
    def command(self) -> str:
        return self.msg[0]["command"]
    
    @property
    def command_attr(self) -> list:
        return self.msg[1]

if __name__ == "__main__":
    msg = message('{"command": "shell","command_attr": {"argv": ["--help","--help"]}}')
    print(str(msg))
    with open("output.txt", "w") as file:
        file.write(msg)
        file.close()