import json
import os
import subprocess

DOMAIN = "bee-content-finch.ngrok-free.app"
# 讀取 JSON 檔案
with open('config.json') as f:
    config = json.load(f)

# 獲取埠號
port = config['server_port']

ngrok_cmd = f'start ngrok http --domain={DOMAIN} {port}'
server_cmd = f'start python d:/HW_Final_server/server_main.py'
# 執行 ngrok 命令
# os.system(f'{ngrok_cmd} & {server_cmd}')
subprocess.run(f'{ngrok_cmd}', shell=True)
subprocess.run(f'{server_cmd}', shell=True)


# https://bee-content-finch.ngrok-free.app/receiveWarning?mac_id=test&has_monkey=1