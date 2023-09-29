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
        """
            returns the python object of the whole msg.
        """
        return self._msg
    
    @property
    def status_code(self) -> int:
        return self._msg["status_code"]

    @property
    def status_msg(self) -> str:
        return self._msg["status_msg"]
