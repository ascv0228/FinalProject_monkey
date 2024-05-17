from flask import send_file
import io
from PIL import Image, ImageDraw
from src import tools

IMAGE_PATH = "./res/nsysu_map.png"

def image():
    return send_file(get_image(), mimetype='image/png')

radius = 5
def get_image():
    config = tools.Config.get_config()
    image = Image.open(config["nsysu_map_destination"])
    draw = ImageDraw.Draw(image)
    
    # for device in config["device_position"]:
    #     pos = config["device_position"][device]
    #     draw.ellipse((pos["x"]-radius, pos["y"]-radius, pos["x"]+radius, pos["y"]+radius), fill="red")
    
    img_io = io.BytesIO()
    image.save(img_io, 'JPEG')
    img_io.seek(0)
    return img_io

_func = image

__exports__ = {
    "name" : _func.__code__.co_name,
    "path" : "/image",
    "methods": ['GET'],
    "execute": _func
}