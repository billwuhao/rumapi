import requests
from rum.api import Group, Node
from rum.paidgroup import *

class Rum:
    def __init__(self, host, port, jwt_token=None):
        """
        host: IP 地址, 本地一般是 http://127.0.0.1, 远程连接 http/https://IP
        port: 端口号
        jwt_token: 用于远程登录身份验证的令牌
        """
        self.group = Group(self)
        self.node = Node(self)

        self._session = requests.Session()
        self._session.keep_alive = False
        requests.adapters.DEFAULT_RETRIES = 5

        self._session.headers.update(
            {
                "USER-AGENT": "rum.api",
                "Content-Type": "application/json",
                "accept": "application/json",
            }
        )
        self.jwt_token = jwt_token

        if self.jwt_token is not None:
            self._session.headers.update({"Authorization": f"Bearer {self.jwt_token}"})

        self.baseurl = f"{host}:{port}"

        # 方法列表
        self.nodeinfo = self.node.info
        self.network = self.node.network
        self.join_group = self.node.join_group
        self.create_group = self.node.create_group
        self.groups = self.node.groups
        self.add_peers = self.node.add_peers
        self.pinged_peers = self.node.pinged_peers
        self.psping = self.node.psping
        self.refresh_token = self.node.refresh_token
        self.content = self.group.content
        self.seed = self.group.seed
        self.clear = self.group.clear
        self.leave = self.group.leave
        self.startsync = self.group.startsync
        self.block = self.group.block
        self.trx = self.group.trx
        self.like = self.group.like
        self.dislike = self.group.dislike
        self.send = self.group.send
        self.announce = self.group.announce
        self.announced_producers = self.group.announced_producers
        self.announced_users = self.group.announced_users
        self.announced_user = self.group.announced_user
        self.producers = self.group.producers
        self.update_user = self.group.update_user
        self.update_producer = self.group.update_producer
        self.update_profile = self.group.update_profile
        self.chainconfig = self.group.chainconfig
        self.denylist = self.group.denylist
        self.allowlist = self.group.allowlist
        self.auth_mode = self.group.auth_mode
        self.configs = self.group.configs
        self.config = self.group.config
        self.update_config = self.group.update_config
        self.stats = self.node.stats
        self.pubqueue = self.group.pubqueue
        self.ack = self.node.ack
        self.paidgroup_dapp = paidgroup_dapp
        self.paidgroup_info = paidgroup_info
        self.check_payment = check_payment
        self.announce_paidgroup = announce_paidgroup
        self.pay_paidgroup = pay_paidgroup
        self.send_file = self.group.send_file
        self.load_files = self.group.load_files
        # self.relays = self.node.relays
        # self.req_relay = self.node.req_relay
        # self.approve_relay = self.node.approve_relay
        # self.del_relay = self.node.del_relay

    def _request(self, method, url, **kwargs):
        resp = self._session.request(method=method, url=self.baseurl + url, **kwargs)
        return resp.json()

    def get(self, url):
        return self._request("get", url)

    def post(self, url, **kwargs):
        return self._request("post", url, **kwargs)

    def delete(self, url):
        return self._request("delete", url)
