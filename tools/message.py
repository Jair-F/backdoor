import copy
import json

class message:
    def __init__(self, msg):
        if isinstance(msg, str):
            self._msg = json.loads(msg)
        elif isinstance(msg, list) or isinstance(msg, tuple) or isinstance(msg, dict):
            self._msg = copy.deepcopy(msg)

    def __str__(self) -> str:
        """ 
            ``return`` returns the set msg as a string
        """
        msg = json.dumps(self._msg, indent=None, separators=(',', ':'))
        return msg
    
    @property
    def msg(self, msg:dict) -> dict:
        if msg != None:
            self._msg = msg
        else:
            raise ValueError("msg not set")

    @property
    def msg(self) -> dict:
        return self._msg
    
    @property
    def command(self) -> str:
        return self._msg[0]["command"]
    
    @property
    def command_attr(self) -> list:
        return self._msg[1]

