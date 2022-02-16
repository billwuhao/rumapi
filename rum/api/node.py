# -*- coding: utf-8 -*-

from munch import Munch
from rum.api.base import BaseAPI


class Node(BaseAPI):
    """基于节点的方法"""
    def info(self):
        """获取节点信息
        
        获取成功, 返回值字段:
            {
                "node_id": "string",
                "node_publickey": "string",
                "node_status": "string",
                "node_type": "string",
                "node_version": "string",
                "peers": {
                    "additionalProp1": [
                    "string"
                    ],
                    "additionalProp2": [
                    "string"
                    ],
                    "additionalProp3": [
                    "string"
                    ]
                }
            }
        """
        return self._get("/api/v1/node")

    def network(self):
        """获取节点网络信息
        
        获取成功, 返回值字段:
            {
                "addrs": [
                    null
                ],
                "ethaddr": "string",
                "groups": [
                    {
                    "GroupId": "string",
                    "GroupName": "string",
                    "Peers": [
                        "string"
                    ]
                    }
                ],
                "nat_enabled": true,
                "nat_type": "string",
                "node": {
                    "additionalProp1": {}
                },
                "peerid": "string"
            }
        """
        return self._get("/api/v1/network")

    def join_group(self, seed):
        """节点加入一个组
        
        seed: 种子, 字段如下: 
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

        返回值字段:
            {
                "app_key": "string",
                "cipher_key": "string",
                "consensus_type": "string",
                "encryption_type": "string",
                "group_id": "string",
                "group_name": "string",
                "owner_pubkey": "string",
                "signature": "string",
                "user_encryptpubkey": "string",
                "user_pubkey": "string"
            }
        """
        return self._post("/api/v1/group/join", json=seed)

    def create_group(self,
                     group_name,
                     consensus_type="poa",
                     encryption_type="public",
                     app_key="group_timeline"):
        """节点创建一个组
        
        group_name: 组名
        consensus_type: 共识类型, "poa", "pos", "pow", 当前仅支持 "poa"
        encryption_type: 加密类型, "public" 公开, "private" 私有
        app_key: 应用标识, 目前 rum-app 支持 "group_timeline", "group_post", "group_note"

        创建成功, 返回值是一个种子字典
        """
        data = Munch(group_name=group_name,
                     consensus_type=consensus_type,
                     encryption_type=encryption_type,
                     app_key=app_key)
        return self._post("/api/v1/group", json=data)

    def groups(self):
        """获取节点加入的所有组
        
        获取成功, 返回值字段:
            {
                "groups": [
                    {
                    "app_key": "string",
                    "cipher_key": "string",
                    "consensus_type": "string",
                    "encryption_type": "string",
                    "group_id": "string",
                    "group_name": "string",
                    "group_status": "string",
                    "highest_block_id": "string",
                    "highest_height": 0,
                    "last_updated": 0,
                    "owner_pubkey": "string",
                    "user_pubkey": "string"
                    }
                ]
            }
        """
        return self._get("/api/v1/groups")

    def backup(self):
        """备份节点数据
        
        备份成功, 返回值字段:
            {
                "config": "string",
                "keystore": "string",
                "seeds": "string"
            }
        """
        return self._get("/api/v1/backup")

    def add_peers(self, peers):
        """节点增加连接节点, 实现快速连接和同步
        
        peers: 节点 ID 列表

        返回值字段显示成功/未成功添加的节点数:
            {
                "err_count": 0,
                "succ_count": 0
            }
        """
        return self._post("/api/v1/network/peers", json=peers)

    def pinged_peers(self):
        """获取可以 ping 的节点"""
        return self._get("/api/v1/network/peers/ping")

    def psping(self, peer_id):
        """ping 一个节点
        
        peer_id: 节点 ID
        
        返回 ttl 值如 {"ttl": [46, 47, 91, 89, 89, 90, 88, 89, 90, 86]}
        """
        return self._post("/api/v1/psping", json={"peer_id": peer_id})

    def jwt_token(self):
        """生成用于节点授权远程请求的身份验证令牌 jwt_token

        当前, 启动节点自动生成 jwt_token, 已不需要该方法获取
        可以在 "/peerConfig/peer_options.toml" 找到
        """
        return self._post("/app/api/v1/token/apply")

    def refresh_token(self, old_token):
        """节点刷新 jwt_token
        
        old_token: 节点旧的 jwt_token
        返回值: {"token": "string"}
        """
        return self._post("/app/api/v1/token/refresh",
                          headers={"Authorization": f"Bearer {old_token}"})
