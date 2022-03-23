import requests
from rum.api import Group, Node


class Rum:
    def __init__(self, host, port, crtfile, jwt_token=None):
        """
        host: IP 地址, 本地一般是 127.0.0.1, 服务器是公网 IP
        port: 端口号
        crtfile: 证书文件 server.crt 绝对路径
        jwt_token: 用于远程登录身份验证的令牌
        """
        self.group = Group(self)
        self.node = Node(self)

        self._session = requests.Session()
        self._session.verify = crtfile
        self._session.keep_alive = False
        requests.adapters.DEFAULT_RETRIES = 5

        self._session.headers.update({
            "USER-AGENT": "rum.api",
            "Content-Type": "application/json",
            "accept": "application/json"
        })
        if jwt_token is not None:
            self._session.headers.update(
                {"Authorization": f"Bearer {jwt_token}"})

        self.baseurl = f"https://{host}:{port}"

        # 方法列表
        self.nodeinfo = self.node.info
        self.network = self.node.network
        self.join_group = self.node.join_group
        self.create_group = self.node.create_group
        self.groups = self.node.groups
        self.backup = self.node.backup
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
        self.schema = self.group.schema
        self.update_schema = self.group.update_schema

    def _request(self, method, url, **kwargs):
        resp = self._session.request(method=method,
                                     url=self.baseurl + url,
                                     **kwargs)
        return resp.json()

    def get(self, url):
        return self._request("get", url)

    def post(self, url, **kwargs):
        return self._request("post", url, **kwargs)