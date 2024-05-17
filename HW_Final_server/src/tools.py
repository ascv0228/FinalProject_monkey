import json




class Config:
    config = None

    @classmethod
    def get_config(cls):
        if cls.config is None:
            with open('./config.json', 'r') as json_file:
                cls.config = json.load(json_file)
        
        return cls.config


import requests


def line_notify_message_image(token, message, image_path):
    url = "https://notify-api.line.me/api/notify"
    headers = {"Authorization": "Bearer " + token}

    files = {'imageFile': open(image_path, 'rb')}
    data = {'message': message}

    r = requests.post(url, headers=headers, files=files, data=data)

    return r.status_code


# "xN3t9VFsxg9hzfsGTF2blXgojyDYCNlUqawS1bLhKtg",