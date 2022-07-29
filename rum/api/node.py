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
        return self._post("/api/v2/group/join", json=seed)

    def create_group(
        self,
        group_name,
        consensus_type="poa",
        encryption_type="public",
        app_key="group_timeline",
    ):
        """节点创建一个组

        group_name: 组名
        consensus_type: 共识类型, "poa", "pos", "pow", 当前仅支持 "poa"
        encryption_type: 加密类型, "public" 公开, "private" 私有
        app_key: 应用标识, 目前 rum-app 支持 "group_timeline", "group_post", "group_note"

        创建成功, 返回值是一个种子字典
        """
        data = Munch(
            group_name=group_name,
            consensus_type=consensus_type,
            encryption_type=encryption_type,
            app_key=app_key,
        )
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

    def add_peers(self, peers):
        """节点增加连接节点, 实现快速连接和同步

        peers: 节点 ID(需要包含 IP 等, 如 "/ip4/110.14.103.110/tcp/1111/16Uiu2H...") 的列表

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

        peer_id: 节点 ID 如 "16Uiu2HAm59mYMPRhrJYw3AFyEuHhcBxbyw85yEk9..."

        返回 ttl 值如 {"ttl": [46, 47, 91, 89, 89, 90, 88, 89, 90, 86]}
        """
        return self._post("/api/v1/psping", json={"peer_id": peer_id})

    def refresh_token(self, old_token=None):
        """节点刷新 jwt_token

        old_token: 节点现在生效的 jwt_token

        返回值: {"token": "string"}
        """
        if old_token is None:
            old_token = self.jwt_token
        return self._post(
            "/app/api/v1/token/refresh",
            headers={"Authorization": f"Bearer {old_token}"},
        )

    def stats(self):
        """获取网络统计摘要"""
        return self._get("/api/v1/network/stats")

    def ack(self, trx_ids):
        """确认(ack) trx, 从队列中移除

        Args:
            trx_ids (list): 队列中 trx 的 ID 组成的列表
        """
        return self._post("/api/v1/trx/ack", json={"trx_ids": trx_ids})

    # def relays(self):
    #     """_summary_"""
    #     return self._get("/api/v1/preview/relay")

    # def req_relay(self, group_id, user_pubkey, relay_type, duration, signature):
    #     """_summary_

    #     Args:
    #         group_id (_type_): _description_
    #         user_pubkey (_type_): _description_
    #         relay_type (_type_): _description_
    #         duration (_type_): _description_
    #         signature (_type_): _description_

    #     Returns:
    #         _type_: _description_
    #     """
    #     data = Munch(
    #         group_id=group_id,
    #         user_pubkey=user_pubkey,
    #         relay_type=relay_type,
    #         duration=duration,
    #         signature=signature,
    #     )
    #     return self._post("/api/v1/preview/relay/req", json=data)

    # def approve_relay(self, req_id):
    #     """_summary_

    #     Args:
    #         relay_id (_type_): _description_
    #     """
    #     return self._get(f"/api/v1/preview/relay/{req_id}/approve")

    # def del_relay(self, relay_id):
    #     """_summary_

    #     Args:
    #         relay_id (_type_): _description_
    #     """
    #     return self._delete(f"/api/v1/preview/relay/{relay_id}")
