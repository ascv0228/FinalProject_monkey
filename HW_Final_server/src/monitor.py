import threading
import time
import src.tools as tools
from typing import Dict
import io

# UPDATE_TIME_MINUTE = 1


class Monitor:
    __slots__ = "mac_id", "x", "y", "hasMonkey", "time", "warning_wait_minutes"
    def __init__(self, mac_id, x, y):
        self.mac_id = mac_id
        self.x = x
        self.y = y
        self.hasMonkey = False
        self.time = 0
        self.warning_wait_minutes = tools.Config.get_config()["warning_wait_minutes"]

    def set_status(self, hasMonkey, time):
        self.hasMonkey = hasMonkey
        self.time = time if hasMonkey else 0

    def check_hasMonkey(self, new_warning_time=None):
        if self.hasMonkey == False or new_warning_time == 0:
            return False
        
        if new_warning_time is None:
            new_warning_time = int(time.time())
        return (new_warning_time - self.time) < (self.warning_wait_minutes * 60 - 1)
    
    def update_status(self, hasMonkey, new_warning_time) -> bool: # 有沒有更新hasMonkey
        # 本來沒猴或猴子警告時間已到
        if not self.check_hasMonkey(new_warning_time):
            if hasMonkey and new_warning_time > self.time:
                self.set_status(hasMonkey, new_warning_time)
                return True
            
            if hasMonkey and new_warning_time <= self.time:
                return False
            
            # 本來有猴，但是等待時間已到，後來沒猴
            if self.hasMonkey:
                self.set_status(hasMonkey, 0)
                return True
            
            return False
        # 本來有猴且猴子警告時間未到
        if hasMonkey:
            if new_warning_time > self.time:
                self.set_status(hasMonkey, new_warning_time)
                return True
            return False

    def get_color(self):
        return "red" if self.check_hasMonkey() else "green"



