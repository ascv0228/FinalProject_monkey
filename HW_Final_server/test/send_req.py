import requests

ngrok_server = "bee-content-finch.ngrok-free.app"

# 發送 GET 請求
response = requests.get(f'https://{ngrok_server}/receiveWarning?mac_id=test&has_monkey=1', timeout=1)

print("Response content:", response.content)

# 這裡可以繼續執行其他程式碼，不會等待請求的回應
print("Request sent...")