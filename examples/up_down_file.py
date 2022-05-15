"""上传下载大文件"""
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from rum import Rum

rum = Rum(host='127.0.0.1',port='9999',crtfile=r'D:\rum\server.crt')

filepath = r"D:\书籍\《模型思维》.pdf"
outputdir = 'D:\\'

#发送大文件
rum.send_file(group_id='d34f000b-2463-4db4-8c38-96965ef804c5',filepath=filepath)

#下载大文件
rum.load_files(group_id='d34f000b-2463-4db4-8c38-96965ef804c5',output=outputdir)