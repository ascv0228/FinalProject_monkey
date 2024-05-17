import flask
import json
import os
from flask_cors import CORS
from typing import Dict
import time
import threading
from PIL import Image, ImageDraw
import os
import asyncio


import src.loader as loader
from src import tools
from src.monitor import Monitor


class App:
    monitors_dict: Dict[str, Monitor] = {}
    monitor_wait_set = set()

    def __init__(self, main_filename) -> None:
        self.load_config()
        self.app = flask.Flask(main_filename)
        CORS(self.app)

    def add_urls(self) -> None:
        print("----------- do add_urls-------------")
        methodDict = loader.importFile(self.config["import_path"])
        # print(methodDict)
        for n, o in methodDict.items():
            try:
                self.app.add_url_rule(o["path"], n, view_func=o["execute"], methods=o["methods"])
                print(f"{o['path']}")
            except Exception as e:
                print(e)


    def run(self):
        self.add_urls()
        self.app.run(host=self.config["server_host"], port=self.config["server_port"], debug=True, threaded=True)

    def load_config(self):
        self.config = tools.Config.get_config()
        for mac_id in self.config["device_position"]:
            pos = self.config["device_position"][mac_id]
            monitor = Monitor(mac_id, pos["x"], pos["y"])
            self.monitors_dict[mac_id] = monitor

    def line_notify(self, msg, img_path):
        for token in self.config["line_receive_token"]:
            tools.line_notify_message_image(token, msg, img_path)
        return
    
    def draw_nsysu_map(self):
        monitors_dict = self.monitors_dict
        image_source_path = self.config["nsysu_map_source"]
        image = Image.open(image_source_path)
        draw = ImageDraw.Draw(image)
        radius = 10

        for mac_id in monitors_dict:
            m = monitors_dict[mac_id]
            draw.ellipse((m.x-radius, m.y-radius, m.x+radius, m.y+radius), fill=m.get_color())

        image_destination_dir, filename = os.path.split(self.config["nsysu_map_destination"])
        if not os.path.exists(image_destination_dir):
            os.makedirs(image_destination_dir)
        image.save(self.config["nsysu_map_destination"], "JPEG")
        return
    
    def update_moniter(self, mac_id, hasMonkey, warning_time):
        if self.monitors_dict.get(mac_id, None) is None:
            return

        isChanged = self.monitors_dict[mac_id].update_status(hasMonkey, warning_time)
        if not isChanged:
            return
        self.draw_nsysu_map()
        
        # 現在有猴子
        if self.monitors_dict[mac_id].check_hasMonkey():
            warning_time_struct = time.localtime(warning_time)
            msg = time.strftime("猴子出沒警告 %Y-%m-%d %H:%M:%S", warning_time_struct)
            self.line_notify(msg, self.config["nsysu_map_destination"])
            event_thread = threading.Thread(target=self.auto_timing_update, args=(mac_id,))
            event_thread.start()
            # event_thread.join()
            return
        
        # 現在沒猴子
        warning_time_struct = time.localtime(int(time.time()))
        msg = time.strftime("猴子警告解除 %Y-%m-%d %H:%M:%S", warning_time_struct)
        self.line_notify(msg, self.config["nsysu_map_destination"])
        return
    
    def auto_timing_update(self, mac_id):
        time.sleep(self.config["warning_wait_minutes"] * 60)
        # 等待時間結束，先確認是否真的沒猴子(被其他線呈改變時間)
        if not self.monitors_dict[mac_id].check_hasMonkey():
            self.update_moniter(mac_id, False, 0)
        return
    
    def threading_monitor_warning(self):
        while True:
            for m in self.monitor_wait_set:
                if not self.monitors_dict[m].check_hasMonkey():
                    self.update_moniter(m, False, 0)
    

    
# app = App(__name__)
# if __name__ == '__main__':
#     app.run()