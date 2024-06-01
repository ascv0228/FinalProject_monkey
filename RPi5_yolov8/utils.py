import cv2
import time
from ultralytics.utils.plotting import Annotator
import requests
import time
from PIL import Image
from io import BytesIO

def draw_annotation(img, label_names, results):
    # print("draw_annotation")
    annotator = Annotator(img)
    for r in results:
        boxes = r.boxes
        for box in boxes:
            b = box.xyxy[0]  # get box coordinates in (top, left, bottom, right) format
            c = box.cls
            annotator.box_label(b, label_names[int(c)])
    annotated_img = annotator.result() if annotator else img.copy()
    return annotated_img

def sendLineNotify(image_array):
    # print("sendLineNotify")
    try:
        t = time.time()
        t1 = time.localtime(t)
        now = time.strftime('%Y/%m/%d %H:%M:%S', t1)
        url = 'https://notify-api.line.me/api/notify'
        token = '3KtNYflJ7kAo9xS7CdTZ5W9a4ich0Zc81qFOZn16CZZ'
        headers = {
        'Authorization': 'Bearer ' + token
        }
        data = {
        'message': now
        }
        image_array=cv2.cvtColor(image_array, cv2.COLOR_BGR2RGB)
        # Convert numpy array to PIL Image
        image = Image.fromarray(image_array.astype('uint8'), 'RGB')

        # Save the image to a BytesIO object
        image_file = BytesIO()
        image.save(image_file, format='JPEG')
        image_file.seek(0)  # Move the cursor to the start of the file

        # Create a 'files' dictionary to hold the file data
        files = {'imageFile': image_file}

        # Send POST request
        requests.post(url, headers=headers, data=data, files=files)
        image_file.close()  # Close the BytesIO object
    except Exception as e:
        print("Failed to send notification:", e)
    finally:
        image_file.close()

import uuid

def get_mac_address():
    try:
        mac = uuid.UUID(int=uuid.getnode()).hex[-12:]
        return ":".join([mac[e:e+2] for e in range(0, 11, 2)])
    except:
        return "00:00:00:00:00:00"
    
import requests
def sendWebNotify():
    DOMAIN = "bee-content-finch.ngrok-free.app"
    mac_id = get_mac_address()
    response = requests.get(f'https://{DOMAIN}/receiveWarning?mac_id={mac_id}&has_monkey=1', timeout=1)
    print("Response content:", response.content)
    return
    