# -*- coding: utf-8 -*-

import requests
from rum.api import Group, Node


class Rum:
    def __init__(self, host, port, crtfile, jwt_token=None):
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

    def _request(self, method, url, **kwargs):
        resp = self._session.request(method=method,
                                     url=self.baseurl + url,
                                     **kwargs)
        return resp.json()

    def get(self, url):
        return self._request("get", url)

    def post(self, url, **kwargs):
        return self._request("post", url, **kwargs)