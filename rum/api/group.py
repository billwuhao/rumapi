from munch import Munch
from rum.img import image_obj, image_objs, group_icon
from rum.api.base import BaseAPI


class Group(BaseAPI):
    """基于组的方法"""
    def content(self,
                group_id,
                reverse=False,
                trx_id=None,
                num=None,
                senders=None):
        """按条件获取某个组的内容, 默认获取最前面的 20 条内容
        
        group_id: 组的 ID
        reverse: 如果是 True, 从最新的内容开始获取
        trx_id: 某条内容的 ID, 如果提供, 从该条之后(包含)获取
        num: 要获取内容条数
        senders: 内容发布/产生者的 ID 的列表
            如果提供, 获取列表中 发布/产生者 发布或产生的内容

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
        trx_id = f"&includestarttrx={trx_id}" if trx_id else ""
        num = f"&num={num}" if num else ""

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
        images: 一张或多张(最多4张)图片网址(url)或本地路径(gif 只能是本地路径), 
            一张是字符串, 多张则是它们组成的列表
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
        image: 头像, 图片的网址(url)或本地路径(gif 只能是本地路径),
            不提供, 将使用系统默认头像更新
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

    def chainconfig(self,
                    group_id,
                    type='set_trx_auth_mode',
                    trx_type='post',
                    trx_auth_mode='follow_alw_list',
                    action='add',
                    pubkey=None,
                    memo=''):
        """组创建者配置内容授权方式或更新黑/白名单
        
        group_id: 组的 ID
        type: 配置类型, "set_trx_auth_mode"(配置规则), "upd_alw_list"(更新白名单), 
            "upd_dny_list"(更新黑名单)
        trx_type: 可配置的内容(trx)类型, 有 "post", "announce",
            "req_block_forward", "req_block_backward",
            "block_synced", "block_produced", "ask_peerid",
            如果 type 是 "set_trx_auth_mode", 则只能是上述中的一个且是字符串,
            否则, 可以是它们中的一个或多个组成的列表
        trx_auth_mode: 内容(trx)授权方式, "follow_alw_list"(白名单方式), 
            "follow_dny_list"(黑名单方式)
        action: "add"(添加), "remove"(移除)
        pubkey: 要添加或删除的用户的 ID
        memo: Memo

        如果 type 是 "set_trx_auth_mode", 则 trx_type 和 trx_auth_mode 必须提供

        如果 type 是 "upd_alw_list" 或 "upd_dny_list", 则 action, trx_type, pubkey 
        必须提供, 即将某个用户加入/移除某个(些) trx_type 白名单或黑名单

        组创建之后, 所有类型的内容(trx)的授权方式默认都是黑名单方式, 
        成为组的用户之后, 自动获得所有授权, 除非被加入黑名单; 
        
        某个类型 trx 授权方式修改为白名单方式后, 所有用户失去该类型 trx 
        的操作权限, 除非被加入白名单; 
        
        白名单优先级最高，某个用户被加入某个(些) trx 类型的白名单后, 无论授权方式是什么,
        也无论该用户是否在该类型的黑名单中, 总是拥有权限, 避免混淆, 应小心配置;

        该方法默认将 "post" 配置为白名单方式, 之后如果将某个用户加入白名单,
        则只有该用户有权发送内容到组内

        返回值字段:
            {
                "group_id": "string",
                "owner_pubkey": "string",
                "signature": "string",
                "trx_id": "string"
            }
        """
        if type == 'set_trx_auth_mode':
            config = Munch(trx_type=trx_type, trx_auth_mode=trx_auth_mode)
        else:
            if isinstance(trx_type, str):
                trx_type = [trx_type]
            config = Munch(trx_type=trx_type, action=action, pubkey=pubkey)

        data = Munch(group_id=group_id,
                     type=type,
                     config=str(dict(config)).replace("'", '"'),
                     memo=memo)

        return self._post(f"/api/v1/group/chainconfig", json=data)

    def denylist(self, group_id):
        """获取某个组的黑名单
        
        返回值字段:
            [
                {
                    "Pubkey": "string",
                    "TrxType": ["string"],
                    "GroupOwnerPubkey": "string",
                    "GroupOwnerSign": "string",
                    "TimeStamp": 0,
                    "Memo": ""
                }
            ]
        """
        return self._get(f"/api/v1/group/{group_id}/trx/denylist")

    def allowlist(self, group_id):
        """获取某个组的白名单
        
        group_id: 组 ID

        返回值字段:
            [
                {
                    "Pubkey": "string",
                    "TrxType": ["string"],
                    "GroupOwnerPubkey": "string",
                    "GroupOwnerSign": "string",
                    "TimeStamp": 0,
                    "Memo": ""
                }
            ]
        """
        return self._get(f"/api/v1/group/{group_id}/trx/allowlist")

    def auth_mode(self, group_id, trx_type):
        """获取某个组某个 trx 类型的授权方式
        
        group_id: 组 ID
        trx_type: 内容(trx)类型, 有 "post", "announce",
            "req_block_forward", "req_block_backward",
            "block_synced", "block_produced", "ask_peerid"

        返回值字段:
            {
                TrxType  string
                AuthType string
            }
        """
        return self._get(f"/api/v1/group/{group_id}/trx/auth/{trx_type}")

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

    def update_config(self,
                      group_id,
                      name='group_desc',
                      type='string',
                      value='增加组的简介',
                      action='add',
                      memo='add',
                      image=None):
        """组创建者更新组的某个配置项
        
        group_id: 组的 ID
        name: 配置项的名称, 目前支持 'group_announcement'(组的公告),
            'group_desc'(组的简介),'group_icon'(组的图标), 均是 "string" 类型
        type: 配置项的类型, 可选值为 "int", "bool", "string"
        value: 配置项的值, 必须与 type 相对应
        action: "add" 或 "del", 增加/修改 或 删除
        memo: 附加信息
        image: 一张图片的网址(url)或本地路径(gif 只能是本地路径),
            如果提供该参数, name 必须是 'group_icon'

        返回值字段:
            {
                GroupId string
                Sign    string
                TrxId   string
            }
        """
        if image is not None:
            value = group_icon(image=image)
        data = Munch(group_id=group_id,
                     name=name,
                     type=type,
                     value=value,
                     action=action,
                     memo=memo)
        return self._post(f"/api/v1/group/appconfig", json=data)

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
                GroupId     string
                OwnerPubkey string
                SchemaType  string
                SchemaRule  string
                Action      string
                Sign        string
                TrxId       string
            }
        """
        data = Munch(group_id=group_id,
                     rule=rule,
                     type=type,
                     action=action,
                     memo=memo)
        return self._post(f"/api/v1/group/schema", json=data)