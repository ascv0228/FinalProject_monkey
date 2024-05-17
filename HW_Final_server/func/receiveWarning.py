from flask import request
import time
# import asyncio

from server_main import app

def receiveWarning():
    mac_id = request.args.get('mac_id', None)
    has_monkey = request.args.get('has_monkey', None)
    if mac_id is None or has_monkey is None:
        return "Missing 'mac_id' or 'has_monkey' parameter", 400
    
    app.update_moniter(mac_id, has_monkey, int(time.time()))
    return "OK",200

_func = receiveWarning

__exports__ = {
    "name" : _func.__code__.co_name,
    "path" : "/receiveWarning",
    "methods": ['GET'],
    "execute": _func
}

if __name__ == "__main__":
    print(_func.__code__.co_name)
