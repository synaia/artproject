from io import BytesIO
import base64
from rembg import remove
from PIL import Image
import time


def image_to_base64(file_name):
    if isinstance(file_name, str):
        try:
            file_name = Image.open(f'../uploaded/{file_name}.png')
        except Exception as ex:
            return None

    buf = BytesIO()
    file_name.save(buf, format='PNG')
    byte_im = buf.getvalue()
    return base64.b64encode(byte_im).decode('ascii')


def remove_it(file):
    infile = Image.open(file)
    # infile.thumbnail((300, 200), Image.ANTIALIAS)
    infile.thumbnail((infile.size[0] // 2, infile.size[1] // 2), Image.ANTIALIAS)
    newfile = remove(infile) # remove bg / model
    bg = Image.open("../uploaded/abstract-blur-background.jpeg")
    bg.thumbnail((newfile.size[0], newfile.size[1]), Image.ANTIALIAS)
    bg.paste(newfile, (0, 0), newfile)
    bg.save(f'../uploaded/{int(time.time())}.png')
    return image_to_base64(bg)
