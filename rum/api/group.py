# -*- coding: utf-8 -*-

from munch import Munch
from rum.img import image_obj, image_objs
from rum.api.base import BaseAPI


class Group(BaseAPI):
    """基于组的方法"""
    def content(self,
                group_id,
                reverse=False,
                trx_id=None,
                num=None,
                senders=None):
        """按条件获取某个组的内容, 默认获取全部内容
        
        group_id: 组的 ID
        reverse: 如果是 True, 从最新的内容开始获取
        trx_id: 某条内容的 ID, 如果提供, 从该条之后(不包含)获取
        num: 要获取内容条数
        senders: 内容发布/产生者的 ID 的列表
            如果提供, 获取列表 ["string"] 中 发布/产生者 发布或产生的内容

        返回值字段:
        [
            {
                "TrxId": "string",
                "Publisher": "string",
                "Content": {},
                "TypeUrl": "string",
                "TimeStamp": 0
            }
        ]
        """
        reverse = "&reverse=true" if reverse else ""
        trx_id = f"&starttrx={trx_id}" if trx_id else ""
        num = f"&num={num}" if trx_id else ""

        return self._post(
            f"/app/api/v1/group/{group_id}/content?{reverse}{trx_id}{num}",
            json=Munch(senders=senders))
        # 调试用 API
        # return self._get(f"/api/v1/group/{group_id}/content")

    def seed(self, group_id):
        """获取已加入的某个组的种子
        
        group_id: 组的 ID
        
        返回种子, 字段如
            {
                "genesis_block": {
                    "BlockId": "string",
                    "GroupId": "string",
                    "ProducerPubKey": "string",
                    "Hash": "string",
                    "Signature": "string",
                    "TimeStamp": "string"
                },
                "group_id": "string",
                "group_name": "string",
                "owner_pubkey": "string",
                "owner_encryptpubkey": "string",
                "consensus_type": "string",
                "encryption_type": "string",
                "cipher_key": "string",
                "app_key": "string",
                "signature": "string"
            }
        """
        return self._get(f"/api/v1/group/{group_id}/seed")

    def clear(self, group_id):
        """清除某个组的数据, 只能清除 quorum, 不能清除前端
        
        group_id: 组的 ID

        成功清除, 返回值字段:
            {
                "group_id": "string",
                "signature": "string"
            }
        """
        return self._post(f"/api/v1/group/clear", json={"group_id": group_id})

    def leave(self, group_id):
        """离开一个组
        
        group_id: 组的 ID

        成功离开, 返回值字段:
            {
                "group_id": "string",
                "signature": "string"
            }
        """
        return self._post(f"/api/v1/group/leave", json={"group_id": group_id})

    def startsync(self, group_id):
        """开始同步一个组
        
        group_id: 组的 ID
        
        开始同步返回: { "GroupId": "string", "Error": ""}
        正在同步中返回: {"error": "GROUP_ALREADY_IN_SYNCING"}
        """
        return self._post(f"/api/v1/group/{group_id}/startsync")

    def block(self, group_id, block_id):
        """获取某个组的某个块信息
        
        group_id: 组的 ID
        block_id: 块 ID

        返回值字段:
        {
            "BlockId": "string",
            "GroupId": "string",
            "PrevBlockId": "string",
            "PreviousHash": "string",
            "Trxs": [
                {
                    "TrxId": "string",
                    "GroupId": "string",
                    "Data": "string",
                    "TimeStamp": "string",
                    "Version": "string",
                    "Expired": 0,
                    "SenderPubkey": "string",
                    "SenderSign": "string"
                }
            ],
            "ProducerPubKey": "string",
            "Hash": "string",
            "Signature": "string",
            "TimeStamp": "string"
        }
        """
        return self._get(f"/api/v1/block/{group_id}/{block_id}")

    def trx(self, group_id, trx_id):
        """获取某个组的某条内容信息
        
        group_id: 组的 ID
        trx_id: 某条内容(trx)的 ID

        返回值字段:
            {
                "Data": "string",
                "Expired": 0,
                "GroupId": "string",
                "SenderPubkey": "string",
                "SenderSign": "string",
                "TimeStamp": "0",
                "TrxId": "string",
                "Version": "string"
            }
        """
        return self._get(f"/api/v1/trx/{group_id}/{trx_id}")

    def _send(self, group_id, obj, sendtype="Add"):
        """发送对象到一个组
        
        group_id: 组的 ID
        obj: 要发送的对象
        sendtype: 发送类型, "Add"(发送内容), "Like"(点赞), "Dislike"(点踩)

        返回值 {"trx_id": "string"}
        """
        data = Munch(type=sendtype,
                     object=obj,
                     target={
                         "id": group_id,
                         "type": "Group"
                     })
        return self._post(f"/api/v1/group/content", json=data)

    def like(self, group_id, trx_id):
        """点赞某个组的某条内容"""
        return self._send(group_id, {"id": trx_id}, "Like")

    def dislike(self, group_id, trx_id):
        """点踩某个组的某条内容"""
        return self._send(group_id, {"id": trx_id}, "Dislike")

    def send(self, group_id, text=None, title=None, images=None, trx_id=None):
        """发送内容到一个组或回复某条内容
        
        group_id: 组的 ID
        text: 要发送的文本内容
        title: 论坛模板必须提供的文章标题
        images: 一张或多张(最多4张)图片网址(url)或本地路径组成的列表
        trx_id: 某条内容(trx)的 ID, 如果提供, 内容将回复给这条指定内容
            text 和 images 必须至少一个不是 None

        返回值 {"trx_id": "string"}
        """
        if images is not None:
            images = image_objs(images)
        obj = Munch(type="Note", content=text, name=title, image=images)
        if trx_id is not None:
            obj.inreplyto = {"trxid": trx_id}
        return self._send(group_id, obj)

    def announce(self, group_id, action='add', type='user', memo='申请成为用户'):
        """申请加入/宣布退出 producer 或私有组的用户
        
        group_id: 组的 ID
        action: "add" 或 "remove", 加入或退出
        type: "user" 或 "producer"
        memo: 附加信息, 例如邀请码等

        返回值字段:
            {
                "action": "string",
                "encrypt_pubkey": "string",
                "group_id": "string",
                "sign": "string",
                "sign_pubkey": "string",
                "trx_id": "string",
                "type": "string"
            }
        """
        data = Munch(group_id=group_id, action=action, type=type, memo=memo)
        return self._post(f"/api/v1/group/announce", json=data)

    def announced_producers(self, group_id):
        """获取申请加入/宣布退出的 producers
        
        返回值字段:
            [
                {
                    "action": "string",
                    "announcedPubkey": "string",
                    "announcerSign": "string",
                    "memo": "string",
                    "result": "string",
                    "timeStamp": 0
                }
            ]
        """
        return self._get(f"/api/v1/group/{group_id}/announced/producers")

    def announced_users(self, group_id):
        """获取申请加入/宣布退出私有组的 users
        
        返回值字段:
            [
                {
                    "announcedEncryptPubkey": "string",
                    "announcedSignPubkey": "string",
                    "announcerSign": "string",
                    "memo": "string",
                    "result": "string",
                    "timeStamp": 0
                }
            ]
        """
        return self._get(f"/api/v1/group/{group_id}/announced/users")

    def producers(self, group_id):
        """获取已经批准的 producers
        
        返回值字段:
            [
                {
                    "ProducerPubkey": "string",
                    "OwnerPubkey": "string",
                    "OwnerSign": "string",
                    "TimeStamp": 0,
                    "BlockProduced": 3
                }
            ]
        """
        return self._get(f"/api/v1/group/{group_id}/producers")

    def update_user(self, user_pubkey, group_id, action='add'):
        """组创建者添加或移除私有组用户
        
        user_pubkey: 用户公钥
        group_id: 组 ID
        action: "add" 或 "remove", 添加或移除

        返回值字段:
            {
                "group_id": "string",
                "user_pubkey": "string",
                "owner_pubkey": "string",
                "sign": "string",
                "trx_id": "string",
                "memo": "string",
                "action": "ADD"
            }
        """
        data = Munch(user_pubkey=user_pubkey, group_id=group_id, action=action)
        return self._post(f"/api/v1/group/user", json=data)

    def update_producer(self, producer_pubkey, group_id, action='add'):
        """组创建者添加或移除 producer
        
        producer_pubkey: producer 公钥
        group_id: 组 ID
        action: "add" 或 "remove", 添加或移除

        返回值字段:
            {
                "group_id": "string",
                "producer_pubkey": "string",
                "owner_pubkey": "string",
                "sign": "string",
                "trx_id": "string",
                "memo": "string",
                "action": "ADD"
            }
        """
        data = Munch(producer_pubkey=producer_pubkey,
                     group_id=group_id,
                     action=action)
        return self._post(f"/api/v1/group/producer", json=data)

    def update_profile(self, group_id, name, image=None, mixin_id=None):
        """更新组的用户配置, 如自己的昵称, 头像, 绑定 mixin 等
        
        group_id: 组的 ID
        name: 昵称
        image: 头像, 图片的网址(url)或本地路径, 不提供, 将使用系统默认头像更新
        mixin_id: mixin 账号 uuid

        更新成功, 返回值: {'trx_id': 'string'}
        """
        if image is not None:
            image = image_obj(image)
        data = Munch(type='Update',
                     person=Munch(name=name, image=image),
                     target={
                         'id': group_id,
                         'type': 'Group'
                     })
        if mixin_id is not None:
            data.person.wallet = {
                "id": mixin_id,
                "type": "mixin",
                "name": "mixin messenger"
            }
        return self._post(f"/api/v1/group/profile", json=data)

    def deniedlist(self, group_id):
        """获取某个组黑名单列表
        
        返回值字段:
            [
                {
                    "GroupId": "string",
                    "PeerId": "string",
                    "GroupOwnerPubkey": "string",
                    "GroupOwnerSign": "string",
                    "TimeStamp": 0,
                    "Action": "add",
                    "Memo": ""
                }
            ]
        """
        return self._get(f"/api/v1/group/{group_id}/deniedlist")

    def update_deniedlist(self, peer_id, group_id, action='add'):
        """组创建者将用户加入或移除黑名单列表
        
        peer_id: 用户节点 ID
        group_id: 组 ID
        action: "add" 或 "del", 加入或移除

        返回值字段:
            {
                "group_id": "string",
                "peer_id": "string",
                "owner_pubkey": "string",
                "sign": "string",
                "trx_id": "string",
                "action": "add",
                "memo": ""
            }
        """
        data = Munch(peer_id=peer_id, group_id=group_id, action=action)
        return self._post(f"/api/v1/group/deniedlist", json=data)

    def configs(self, group_id):
        """获取组的所有配置项列表
        
        返回值字段:
            [
                {
                    "Name": "test_string",
                    "Type": "STRING"
                }
            ]
        """
        return self._get(f"/api/v1/group/{group_id}/config/keylist")

    def config(self, group_id, keyname):
        """获取组的某个配置项信息
        
        group_id: 组的 ID
        keyname: 配置项名称

        返回值字段:
            {
                "Name": "string",
                "Type": "string",
                "Value": "string",
                "OwnerPubkey": "string",
                "OwnerSign": "string",
                "Memo": "string",
                "TimeStamp": 0
            }
        """
        return self._get(f"/api/v1/group/{group_id}/config/{keyname}")

    def update_config(self, group_id, name, type, value, action, memo):
        """组创建者更新组的某个配置项
        
        group_id: 组的 ID
        name: 配置项的名称
        type: 配置项的类型, 可选值为 "int", "bool", "string"
        value: 配置项的值, 必须与 type 相对应
        action: "add" 或 "del", 增加/修改 或 删除
        memo: 附加信息
        """
        data = Munch(group_id=group_id,
                     name=name,
                     type=type,
                     value=value,
                     action=action,
                     memo=memo)
        return self._post(f"/api/v1/group/config", json=data)

    def schema(self, group_id):
        """获取组的概要
        
        返回值字段:
            [
                {
                    "Type": "string",
                    "Rule": "string",
                    "TimeStamp": 0
                }
            ]
        """
        return self._get(f"/api/v1/group/{group_id}/app/schema")

    def update_schema(self, group_id, rule, type, action, memo):
        """组创建者更新组的概要
        
        group_id: 组的 ID
        rule: 概要规则
        type: 概要类型 "schema_type"
        action: "add" 或 "remove", 添加或删除
        memo: 附加信息

        返回值字段:
            {
                "rule": "string",
                "type": "string",
                "group_id": "string",
                "action": "string",
                "memo": "string"
            }
        """
        data = Munch(group_id=group_id,
                     rule=rule,
                     type=type,
                     action=action,
                     memo=memo)
        return self._post(f"/api/v1/group/schema", json=data)