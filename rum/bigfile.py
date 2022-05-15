import base64
import filetype
import json
import os
import hashlib

_chunksize = 150 * 1024


def _split_file(filepath):
    """拆分大文件, 返回拆分后字节列表

    Args:
        filepath (str): 文件路径
    """
    file_total_size = os.path.getsize(filepath)
    chunks = divmod(file_total_size, _chunksize)
    file_obj = open(filepath, "rb")

    segments = []
    for i in range(int(chunks[0])):
        file_obj.seek(i * _chunksize)
        ibytes = file_obj.read(_chunksize)
        segments.append(ibytes)

    if chunks[1] != 0:
        segments.append(file_obj.read(chunks[1]))
    file_obj.close()

    return segments


def file_info(filepath):
    """生成文件信息

    Args:
        filepath (str): 文件路径
    """
    file_name = os.path.basename(filepath)
    with open(filepath, "rb") as f:
        sha256 = hashlib.sha256(f.read()).hexdigest()
    fileinfo = {
        "mediaType": filetype.guess(filepath).mime,
        "name": file_name,
        "title": file_name.split(".")[0],
        "sha256": sha256,
        "segments": [],
    }

    n = 1
    for i in _split_file(filepath):
        fileinfo["segments"].append(
            {"id": f"seg-{n}", "sha256": hashlib.sha256(i).hexdigest()}
        )
        n += 1

    return json.dumps(fileinfo).encode()


def file_to_postobjs(filepath):
    """生成 RUM 发送对象列表

    Args:
        filepath (str): 文件路径
    """
    fileinfo = {
        "type": "File",
        "name": "fileinfo",
        "file": {
            "mediaType": "application/json",
            "content": base64.b64encode(file_info(filepath)).decode(),
        },
    }

    objs = [fileinfo]
    n = 1
    for i in _split_file(filepath):
        segment = {
            "type": "File",
            "name": f"seg-{n}",
            "file": {
                "mediaType": "application/octet-stream",
                "content": base64.b64encode(i).decode(),
            },
        }
        objs.append(segment)
        n += 1

    return objs


def parse_fileinfo(fileinfo):
    """解析文件信息

    Args:
        fileinfo (str): 文件信息的 base64 字符串
    """
    return json.loads(base64.b64decode(fileinfo.encode()).decode())


def filter_file_content(trxs, info=False):
    """筛选大文件的内容

    Args:
        trxs (list): Trx 列表
        info (bool): 如果为 True, 只返回大文件的信息
    """
    file_trxs = (i for i in trxs if i["Content"].get("type") == "File")

    all_content = {}
    file_content = {}
    for i in file_trxs:
        content = i["Content"]["file"]["content"]
        if i["Content"]["name"] == "fileinfo":
            content = parse_fileinfo(content)
            all_content[content["sha256"]] = [content]
        else:
            content = base64.b64decode(content)
            file_content[hashlib.sha256(content).hexdigest()] = content

    if info:
        return all_content

    for k, v in all_content.items():
        for i in v[0]["segments"]:
            if i["sha256"] in file_content:
                all_content[k].append(file_content[i["sha256"]])
            else:
                print(f'File {v[0]["name"]} missing {v[0]["id"]}')

    return all_content
