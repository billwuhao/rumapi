import base64
import urllib3
import uuid
import filetype
import time
import random
import io
from PIL import Image
from datetime import datetime

from api import Api
from config import *

api = Api(PORT, HOST, CACERT)
upm = urllib3.PoolManager(timeout=3)


def image_to_bytes(image: str, headers: dict[str, str]) -> bytes:
    """Convert picture to bytes.

    image: Picture url or path
    headers: Request header when getting network picture
    """
    # download image from url
    if image.startswith(('http://', 'https://')):
        img_bytes = upm.request('GET', image, headers=headers).data
        time.sleep(random.uniform(2, 3))
    # load image from file
    else:
        with open(image, 'rb') as f:
            img_bytes = f.read()
    return img_bytes


def zip_image(img_bytes: bytes, kb: int = 200) -> bytes:
    """Compress the picture below the specified size(kb).
    
    img_bytes: Picture bytes stream
    kb: Specified size
    """
    with io.BytesIO(img_bytes) as im:
        size = len(im.getvalue()) // 1024
        if size <= kb:
            return img_bytes
        while size > kb:
            img = Image.open(im)
            x, y = img.size
            out = img.resize((int(x * 0.95), int(y * 0.95)), Image.ANTIALIAS)
            im.close()
            im = io.BytesIO()
            out.save(im, 'jpeg')
            size = len(im.getvalue()) // 1024
        return im.getvalue()


def send_post(groub_id: str,
              msg: str = '',
              title: str = '',
              images: list[str] = None,
              trxid: str = None,
              headers: dict[str, str] = None) -> dict[str, str]:
    """Send content to a specified group, or reply to someone.
    
    groub_id: Groub ID
    msg: Text message
    title: Article title. BBS use it as title which should not be ""
    images: Picture urls or paths list. No more than 4 pictures,
        and total size less than 200 KB
    trxid: ID of the Trx being replied to
    headers: Request header when getting network picture
    """

    payload = {
        "type": "Add",
        "object": {
            "type": "Note",
            "content": msg,
            "name": title,
            "image": [],
            "inreplyto": {
                "trxid": trxid
            }
        },
        "target": {
            "id": groub_id,
            "type": "Group"
        }
    }

    if trxid is None:
        payload["object"].pop("inreplyto")
    if images is not None:
        for i in images:
            img_bytes = image_to_bytes(i, headers=headers)
            zimg = zip_image(img_bytes, int(200 / len(images)))
            image = {
                "mediaType": filetype.guess(zimg).mime,
                "content": base64.b64encode(zimg).decode("utf-8"),
                "name": f"{uuid.uuid4()}-{datetime.now().isoformat()}"
            }
            payload["object"]["image"].append(image)

    return api.post_content(payload)


if __name__ == "__main__":
    groub_id = "4b4444ae-b6f4-4b89-8094-e2d8e3f2d7a2"
    msg = "hello"
    title = "Title"
    images = [
        r"D:\Jupyter\imgs\2486.jpg",
        r"D:\Jupyter\imgs\1592.jpg",
        r"D:\Jupyter\imgs\948.jpg",
    ]
    trxid = None  # "c79f742e-c736-4ae7-a481-7df0edea9d08"
    headers = {
        "USER-AGENT":
        "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)"
    }
    print(send_post(groub_id, msg, title, images, trxid, headers))
