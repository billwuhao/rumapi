# -*- coding: utf-8 -*-

import base64
import uuid
import filetype
import time
import random
import io
import os
from PIL import Image
from datetime import datetime
from pytest import Instance
import urllib3
from pygifsicle import gifsicle

upm = urllib3.PoolManager(timeout=5)
headers = {
    "USER-AGENT": "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)"
}


def image_to_bytes(image):
    """获取图片字节

    image: 图片网络地址 url 或本地路径
    headers: 获取网络图片的请求头
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


def zip_image(img_bytes, kb=200):
    """压缩图片(非动图)到指定大小 (kb) 以下
    
    img_bytes: 图片字节
    kb: 指定压缩大小, 默认 200kb

    返回压缩后的图片字节
    """
    with io.BytesIO(img_bytes) as im:
        size = len(im.getvalue()) / 1024
        if size < kb:
            return img_bytes
        while size >= kb:
            img = Image.open(im)
            x, y = img.size
            out = img.resize((int(x * 0.95), int(y * 0.95)), Image.ANTIALIAS)
            im.close()
            im = io.BytesIO()
            out.save(im, 'jpeg')
            size = len(im.getvalue()) / 1024
        return im.getvalue()


def zip_gif(gif, kb=200, width=250, cover=True):
    """压缩动图(gif)到指定大小和尺寸以下
    
    gif: gif 格式动图本地路径
    kb: 指定压缩大小, 默认 200kb
    width: 指定宽度, 会保留图片纵横比
    cover: 是否覆盖原图, 默认覆盖

    返回压缩后图片字节

    该方法需要安装 gifsicle 软件和 pygifsicle 模块
    """
    destination = None
    if not cover:
        destination = f"{os.path.splitext(gif)[0]}-zip.gif"
    gifsicle(gif,
             destination=destination,
             optimize=True,
             options=["--lossy=100", "--resize-width",
                      str(width)])
    if not cover:
        gif = destination

    size = os.path.getsize(gif) / 1024
    while size >= kb:
        gifsicle(gif, optimize=True, options=["--scale", "0.9"])
        size = os.path.getsize(gif) / 1024
    return image_to_bytes(gif)


def image_obj(image, kb=200):
    """将图片处理成可通过 RUM API 发送的图片对象, 要求大小小于 200kb
    
    image: 一张图片的网址(url)或本地路径(gif 只能是本地路径)
    """
    img_bytes = image_to_bytes(image)
    if filetype.guess(img_bytes).extension == "gif":
        zimg = zip_gif(image, kb=kb, cover=False)
    else:
        zimg = zip_image(img_bytes, kb=kb)
    image_obj = {
        "mediaType": filetype.guess(zimg).mime,
        "content": base64.b64encode(zimg).decode("utf-8"),
        "name": f"{uuid.uuid4()}-{datetime.now().isoformat()}"
    }
    return image_obj


def image_objs(images):
    """将一张或多张图片处理成可通过 RUM API 发送的图片对象列表, 要求总大小小于 200kb
    
    images: 一张或多张(最多4张)图片网址(url)或本地路径(gif 只能是本地路径), 
        一张是字符串, 多张则是它们组成的列表
    """
    if isinstance(images, str):
        images = [images]
    kb = int(200 // len(images))
    image_objs = []
    for i in images:
        image = image_obj(i, kb=kb)
        image_objs.append(image)

    return image_objs