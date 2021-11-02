import requests
from urllib.parse import urlparse
import os
import base64


def img_download(url):
    r = requests.get(url, allow_redirects=True)
    url_name = urlparse(url)
    filename = os.path.basename(url_name.path)
    save_path = 'Input/'
    complete_name = os.path.join(save_path, filename)
    open(complete_name, 'wb').write(r.content)
    return filename


def img_upload(filename):
    save_path = 'Output/'
    complete_name = os.path.join(save_path, filename.replace(".", "-out."))
    with open(complete_name, "rb") as file:
        url = "https://api.imgbb.com/1/upload"
        payload = {
            "key": 'bdb69daed59158e681e9be9158fdcb63',
            "image": base64.b64encode(file.read()),
        }
        res = requests.post(url, payload)
    result = res.json()
    return result
