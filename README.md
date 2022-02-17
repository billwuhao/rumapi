# Rum API

```python
from rum import Rum

rum = Rum(host, port, crtfile, jwt_token=None)

# 方法列表
rum.nodeinfo #获得节点信息
rum.network #获得节点网络信息
rum.join_group #加入一个组
rum.create_group #创建一个组
rum.groups #获取所有组信息
rum.backup #备份节点数据
rum.add_peers #增加连接节点
rum.pinged_peers #获取可 ping 节点
rum.psping #ping 一个节点
rum.refresh_token #刷新 jwt_token
rum.content #获取某个组内容
rum.seed #获取已加入某个组种子
rum.clear #清除一个组内容
rum.leave #离开一个组
rum.startsync #开始同步一个组
rum.block #获取某个块信息
rum.trx #获取某条内容（trx）
rum.like #点赞
rum.dislike #点踩
rum.send #发送内容
rum.announce #申请 producer 或私有组用户
rum.announced_producers #获取申请 producer 列表
rum.announced_users #获取申请 user 列表
rum.producers #获取已批准 producers
rum.update_user #添加或删除私有组用户
rum.update_producer #添加或删除 producer
rum.update_profile #更新某个组用户配置
rum.deniedlist #获取某个组黑名单
rum.update_deniedlist #将用户添加或移除黑名单
rum.configs #获取组配置列表
rum.config #获取组某个配置
rum.update_config #更新组配置
rum.schema #获取组概要
rum.update_schema #更新概要
```