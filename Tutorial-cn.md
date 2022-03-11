# RUM 开发教程中文翻译

![Main Test](https://github.com/rumsystem/quorum/actions/workflows/maintest.yml/badge.svg)

原文 [RUM Development Tutorial](https://github.com/rumsystem/quorum/blob/main/Tutorial.md)，翻译会定期保持更新。

内容主要是原文翻译。如有不当或错误之处，敬请批评指正。

<span id="top"></span>

## 目录

- [RUM 开发教程中文翻译](#rum-开发教程中文翻译)
  - [目录](#目录)
- [环境准备](#环境准备)
  - [运行测试](#运行测试)
  - [生成 API 文档](#生成-api-文档)
  - [配置本地测试网](#配置本地测试网)
- [节点](#节点)
  - [获取节点信息](#获取节点信息)
- [组](#组)
  - [创建一个组](#创建一个组)
  - [加入组](#加入组)
  - [获取已加入的所有组信息](#获取已加入的所有组信息)
  - [清除组内数据](#清除组内数据)
  - [离开一个组](#离开一个组)
  - [组创建者删除组 <font color="yellow"><sup>废弃</sup></font>](#组创建者删除组-font-coloryellowsup废弃supfont)
  - [获取组的种子](#获取组的种子)
- [网络和同步](#网络和同步)
  - [获取网络信息](#获取网络信息)
  - [开始同步](#开始同步)
- [内容 API](#内容-api)
  - [发送内容到组](#发送内容到组)
    - [仅发送文本](#仅发送文本)
    - [图文一起发](#图文一起发)
    - [回复](#回复)
    - [点赞或点踩](#点赞或点踩)
  - [更新组内用户配置](#更新组内用户配置)
  - [获取组内所有内容](#获取组内所有内容)
  - [按要求获取内容](#按要求获取内容)
  - [内容相关 Trx 介绍](#内容相关-trx-介绍)
    - [Note Trx](#note-trx)
    - [点赞/点踩 Trx](#点赞点踩-trx)
    - [用户配置 Trx](#用户配置-trx)
- [块](#块)
  - [获取块信息](#获取块信息)
- [Trx](#trx)
  - [关于 Trx](#关于-trx)
  - [获取 Trx 信息](#获取-trx-信息)
- [Producers](#producers)
  - [关于 producers](#关于-producers)
  - [Producer 申请](#producer-申请)
  - [获取提交申请的 Producers](#获取提交申请的-producers)
  - [Owner 批准/移除 Producer](#owner-批准移除-producer)
  - [获取已经批准的 Producers](#获取已经批准的-producers)
- [DeniedList <font color="yellow"><sup>废弃</sup></font>](#deniedlist-font-coloryellowsup废弃supfont)
- [组的配置](#组的配置)
  - [Owner 更新组的配置](#owner-更新组的配置)
  - [获取组的配置列表](#获取组的配置列表)
  - [获取某个配置项的信息](#获取某个配置项的信息)
  - [Owner 更新组的 Schema](#owner-更新组的-schema)
  - [获取组的 Schema](#获取组的-schema)
- [私有组](#私有组)
  - [User 申请](#user-申请)
  - [获取申请成为私有组用户的申请列表](#获取申请成为私有组用户的申请列表)
  - [Owner 批准/移除 User](#owner-批准移除-user)
- [链端配置](#链端配置)
  - [关于链端配置](#关于链端配置)
  - [获取某个 `Trx 类型` 的 `Following 规则`](#获取某个-trx-类型-的-following-规则)
  - [为某个 `Trx 类型` 设置 `Following 规则`](#为某个-trx-类型-设置-following-规则)
  - [更新某个/某些 `Trx 类型` 的黑/白名单](#更新某个某些-trx-类型-的黑白名单)
  - [获取组的黑/白名单](#获取组的黑白名单)
  - [客户端如何使用 API](#客户端如何使用-api)
    - [完全拒绝一个用户](#完全拒绝一个用户)
    - [再次授予一个用户所有权限](#再次授予一个用户所有权限)
    - [怎样设置单一作者模式](#怎样设置单一作者模式)
- [用自己擅长的语言开发](#用自己擅长的语言开发)
- [附录](#附录)
    - [group_id](#group_id)
    - [group_name](#group_name)
    - [trx_id/TrxId](#trx_idtrxid)
    - [block_id/BlockId](#block_idblockid)
    - [node_id](#node_id)
    - [peer_id](#peer_id)
    - [owner_pubkey/user_pubkey](#owner_pubkeyuser_pubkey)
    - [group_status](#group_status)
    - [app_key](#app_key)
    - [consensus_type](#consensus_type)
    - [encryption_type](#encryption_type)
    - [TrxType/trx_type](#trxtypetrx_type)
    - [Authtype/trx_auth_mode](#authtypetrx_auth_mode)

# 环境准备

下载安装 go（版本 1.15.2 以上）

克隆 quorum 项目到本地：https://github.com/rumsystem/quorum.git

cd 进入 quorum 文件夹路径

## 运行测试

- Linux：

```go test cmd/main* -v```

- Windows：

`go test cmd/main.go cmd/main_test.go -v`

## 生成 API 文档

```go run cmd/docs.go```

然后用浏览器打开：```http://localhost:1323/swagger/index.html```

[>>> 回到目录](#top)

## 配置本地测试网

启动 3 个节点用来测试：

- `bootstrap node` 引导节点
- `owner node` 节点一，就叫它 owner 节点（名字可以任意）
- `user node` 节点二，叫它 user 节点（名字可以任意）

按下列步骤开始：

1. 创建 `config/` 文件夹：

```bash
mkdir -p config
```

2. 启动 `bootstrap node`

```bash
go run cmd/main.go -bootstrap -listen /ip4/0.0.0.0/tcp/10666 -logtostderr=true
```

输入密码，启动后找到如下内容：

```bash
I0420 14:58:47.719592     332 keys.go:47] Load keys from config
I0420 14:58:47.781916     332 main.go:64] Host created, ID:<QmR1VFquywCnakSThwWQY6euj9sRBn3586LDUm5vsfCDJR>, Address:<[/ip4/172.28.230.210/tcp/10666 /ip4/127.0.0.1/tcp/10666]>
```

记住`节点ID`（后面也这样称呼），如上述内容中的 `QmR1VFquywCnakSThwWQY6euj9sRBn3586LDUm5vsfCDJR`

3. 加入引导节点参数，启动节点一 `owner node`

```bash
go run cmd/main.go -peername owner -listen /ip4/127.0.0.1/tcp/7002 -apilisten :8002 -peer /ip4/127.0.0.1/tcp/10666/p2p/<QmR1VFquywCnakSThwWQY6euj9sRBn3586LDUm5vsfCDJR> -configdir config -datadir data -keystoredir ownerkeystore  -jsontracer ownertracer.json -debug true
```

4. 同样的方式启动节点二 `user node`，注意节点名，端口号，`-keystoredir` 和 `-jsontracer` 参数不一样

```bash
go run cmd/main.go -peername user -listen /ip4/127.0.0.1/tcp/7003 -apilisten :8003 -peer /ip4/127.0.0.1/tcp/10666/p2p/<QmR1VFquywCnakSThwWQY6euj9sRBn3586LDUm5vsfCDJR> -configdir config -datadir data -keystoredir userkeystore  -jsontracer usertracer.json -debug true
```

- 第一次启动节点，要求输入密码并二次确认，如果不输入密码，会自动创建；
- 密码创建后，下一次启动输入一次密码即可启动节点；
- 环境变量 RUM_KSPASSWD 可以用来输入密码，像下面这样：

```bash
RUM_KSPASSWD=<node_passwor> go run cmd/main.go...
```

[>>> 回到目录](#top)

# 节点

## 获取节点信息

**API**: ```*/api/v1/node```

- 方法: GET
- 参数 : none

**Example**:

```bash
curl -k -X GET -H 'Content-Type: application/json' -d '{}' https://127.0.0.1:8003/api/v1/node
```

调用 API 返回:

```json
{
    "node_id": "16Uiu2HAkytdk8dhP8Z1JWvsM7qYPSLpHxLCfEWkSomqn7Tj6iC2d",
    "node_publickey": "CAISIQJCVubdxsT/FKvnBT9r68W4Nmh0/2it7KY+dA7x25NtYg==",
    "node_status": "NODE_ONLINE",
    "node_type": "peer",
    "node_version": "1.0.0 - 99bbd8e65105c72b5ca57e94ae5be117eaf05f0d",
    "peers": {
        "/quorum/nevis/meshsub/1.1.0": [
            "16Uiu2HAmM4jFjs5EjakvGgJkHS6Lg9jS6miNYPgJ3pMUvXGWXeTc"
        ]
    }
}
```

参数

- node_id `节点ID`
- node_publickey `节点公钥`
- node_status 节点状态 "NODE_ONLINE"（在线）或 "NODE_OFFLINE"（下线）
- node_version 节点的协议版本号
- peers 网络中已连接的节点的 ID

[>>> 回到目录](#top)

# 组

`组`是直译的名称，按照 RUM 的设计，组应该叫 RUM 系统网络的`应用`（App）更恰当，因为每个组都可以添加各种配置（Appconfig，Schema，Chainconfig）以进行定制化开发，使之成为你想要实现的应用。为了方便理解，我们后面也称之为`组`。

## 创建一个组

节点一 `owner node` 创建一个组

**API**: ```*/api/v1/group```

- 方法: POST
- 参数:
    - group_name 组名，可任意，不可修改
    - consensus_type 共识类型，当前仅仅是 "poa"
    - encryption_type 组的加密类型，必须是 "public"（公开）或 "private"（私有）
    - app_key 自定义 key，用于基于 RUM 系统开发应用时，可对应用分类，目前 [rum-app](https://github.com/rumsystem/rum-app) 支持 3 种，"group_timeline", "group_post" 和 "group_note"

**Example**:

```bash
curl -k -X POST -H 'Content-Type: application/json' -d '{"group_name":"my_test_group", "consensus_type":"poa", "encryption_type":"public", "app_key":"test_app"}' https://127.0.0.1:8002/api/v1/group
```

Windows（下面不再列出，自行做相应修改）：

```
curl -k -X POST -H "Content-Type: application/json" -d "{\"group_name\":\"my_test_group\", \"consensus_type\":\"poa\", \"encryption_type\":\"public\", \"app_key\":\"test_app\"}" https://127.0.0.1:8002/api/v1/group
```

参数如：

```json
{
    "group_name": "my_test_group",
    "consensus_type": "poa",
    "encryption_type": "public",
    "app_key": "test_app"
}
```

调用 API 返回一个种子 `seed`:

```json
{
    "genesis_block": {
        "BlockId": "80e3dbd6-24de-46cd-9290-ed2ae93ec3ac",
        "GroupId": "c0020941-e648-40c9-92dc-682645acd17e",
        "ProducerPubKey": "CAISIQLW2nWw+IhoJbTUmoq2ioT5plvvw/QmSeK2uBy090/3hg==",
        "Hash": "LOZa0CLITIpuQqpvXb6LyXV9z+2rSoU4JwBq0BCXttc=",
        "Signature": "MEQCICAXCicQ6f4hRNSoJR89DF3a6AKpe6ZgLXsjXqH9H3jxAiA8dpukcriwEu8amouh2ZEKA2peXr3ctKQwxI3R6+nrfg==",
        "Timestamp": 1632503907836381400
    },
    "group_id": "c0020941-e648-40c9-92dc-682645acd17e",
    "group_name": "my_test_group",
    "owner_pubkey": "CAISIQLW2nWw+IhoJbTUmoq2ioT5plvvw/QmSeK2uBy090/3hg==",
    "owner_encryptpubkey": "age18kngxt6lkxqulldvxu8xs2ey77rrzwjhqpdey527ad4gkn3euu9sj3ah5j",
    "consensus_type": "poa",
    "encryption_type": "public",
    "cipher_key": "8e9bd83f84cf1408484d24f486861947a1db3fbe6eb3c61e31af55a4803aedc1",
    "app_key": "test_app",
    "signature": "304502206897c3c67247cba2e8d5991501b3fd471fcca06f15915efdcd814b9e99c9a48a022100aa3024eb5663da6cbbde150132a4ff52c6c6aeeb49e0c039b4c28e72b071382f"
}
```

部分参数介绍:
* genesis_block： 创世区块，该组的第一个区块
- BlockId： `块 ID`
- ProducerPubKey： Producer 的 `用户公钥`，Producer 可理解为出块者，新建组 Producer 是组的创建者
* group_id： `组 ID`（记住这个 ID，后面很多操作都需要这个参数，并记得将下列 API 中的 组 ID 换成这个）
- owner_pubkey： 创建者的 `用户公钥`
* owner_encryptpubkey： `创建者加密公钥`
* cipher_key： aes 密钥 <sup>[1]</sup>
* signature：  创建者的签名

> **用户公钥**：节点每加入一个组，都会生成一个组内唯一 `用户公钥`，通过这个公钥，可以进行很多权限相关的操作，例如申请 Producer，申请私有组的用户等。在后面的 API 中，会因为身份的不同，将这个公钥称作 owner_pubkey，user_pubkey，Publisher，SenderPubkey，AnnouncedPubkey 等等，只要是同一个组内同一个用户，它都是指同一个 `用户公钥`。例如上述的 ProducerPubKey 和 owner_pubkey 都是指 Owner 的 `用户公钥`。

<sup>[1]</sup> 不管组的加密类型是什么 (`public` or `private`), 除了 "POST" 之外，所有的 Trx 都是通过 `cipher_key` 加密。

其他节点可以通过 创建组返回的种子 加入该组。

[>>> 回到目录](#top)

## 加入组

节点二 `user node` 加入组

**API**: ```*/api/v1/group/join```

- 方法: POST
- 参数: 上述创建组返回的种子 `seed`

**Example**:

```bash
curl -k -X POST -H 'Content-Type: application/json' -d '{"genesis_block":{"BlockId":"36ac6e22-80a1-4d54-abbb-8bd2c55ef8cf","GroupId":"eae3f0db-a034-4c5f-a25f-b1177390ec4d","ProducerPubKey":"CAISIQMJIG4do9g8PBixH432YXVQmD7Ilqp7DzbGxgLJHbRoFA==","Hash":"fDGwAPJbHHG0GpKLQZnRolK9FUO5nSIod/iprwQQn8g=","Signature":"MEYCIQDo5uge+saujb0WR6ZreISDYWpRzY6PQ3f5ly7vtHHgkQIhAKcuwDT2fIpBDx/7lQU6mIBQKJuQeI0Zbw3W7kHfBO28","Timestamp":1631804384241781200},"group_id":"eae3f0db-a034-4c5f-a25f-b1177390ec4d","group_name":"my_test_group","owner_pubkey":"CAISIQMJIG4do9g8PBixH432YXVQmD7Ilqp7DzbGxgLJHbRoFA==","owner_encryptpubkey":"age1lx3zh5sc5cureh484t5tm2036lhrzdnh96rfaft6echs9cqsefss4yn886","consensus_type":"poa","encryption_type":"public","cipher_key":"3994c4224da17ad50504c78458f37249149477c7bc643f3fe78e44033c17874a","signature":"30450220591361918948140c8ad1736cde3831f326470f2d3c5105a0b63867c7b216857c0221008921422c6e1974834d5610d4c6ad1a9dd0394ac464dfc12659cde41d75172d14"}' https://127.0.0.1:8003/api/v1/group/join
```

调用 API 返回:

```json
{
    "group_id": "ac0eea7c-2f3c-4c67-80b3-136e46b924a8",
    "group_name": "my_test_group",
    "owner_pubkey": "CAISIQOeAkTcYYWVTSH80dl2edMA4kI27g9/C6WAnTR01Ae+Pw==",
    "user_pubkey": "CAISIQO7ury6x7aWpwUVn6mj2dZFqme3BAY5xDkYjqW/EbFFcA==",
    "user_encryptpubkey": "age1774tul0j5wy5y39saeg6enyst4gru2dwp7sjwgd4w9ahl6fkusxq3f8dcm",
    "consensus_type": "poa",
    "encryption_type": "public",
    "cipher_key": "076a3cee50f3951744fbe6d973a853171139689fb48554b89f7765c0c6cbf15a",
    "signature": "3045022100a819a627237e0bb0de1e69e3b29119efbf8677173f7e4d3a20830fc366c5bfd702200ad71e34b53da3ac5bcf3f8a46f1964b058ef36c2687d3b8effe4baec2acd2a6"
}
```

部分参数介绍:
- user_pubkey `用户公钥`，节点加入一个组，即产生一个该组内 `用户公钥`
- user_encryptpubkey `用户加密公钥`

[>>> 回到目录](#top)

## 获取已加入的所有组信息

**API**: ```*/api/v1/groups```

- 方法: GET
- 参数 : none

**Example**:

```bash
curl -k -X GET -H 'Content-Type: application/json' -d '{}' https://127.0.0.1:8002/api/v1/groups
```

调用 API 返回:

```json
{
    "groups": [
        {
            "group_id": "90387012-431e-495e-b0a1-8d8060f6a296",
            "group_name": "my_test_group",
            "owner_pubkey": "CAISIQP67zriZHvC+OWv1X8QzFIwm8CKIM+5KRx1FsUSHQoKxg==",
            "user_pubkey": "CAISIQP67zriZHvC+OWv1X8QzFIwm8CKIM+5KRx1FsUSHQoKxg==",
            "consensus_type": "POA",
            "encryption_type": "PUBLIC",
            "cipher_key": "f4ee312ef7331a2897b547da0387d56a7fe3ea5796e0b628f892786d1e7ec15d",
            "app_key": "test_app",
            "last_updated": 1631725187659332400,
            "highest_height": 0,
            "highest_block_id": "a865ae03-d8ce-40fc-abf6-ea6f6132c35a",
            "group_status": "IDLE"
        }
    ]
}
```

部分参数介绍:
* last_updated 组内最新 Trx 上链时间
* highest_height 该组中 “最高” 区块的高度
* highest_block_id 该组中 “最高” 区块 `区块 ID`

[>>> 回到目录](#top)

## 清除组内数据

**API**: ```*/api/v1/group/clear```

- 方法: POST
- 参数: group_id `组 ID`

**Example**:

```bash
curl -k -X POST -H 'Content-Type: application/json' -d '{"group_id":"<13a25432-b791-4d17-a52f-f69266fc3f18>"}' https://127.0.0.1:8002/api/v1/group/clear | jq
```

调用 API 返回:

```json
{
    "group_id": "13a25432-b791-4d17-a52f-f69266fc3f18",
    "signature": "30450221009634af1636bf7374453cd73088ff992d9020777eb617795e3c93ea5d5008f56d022035342a852e87afa87b5e038147dedf10bb847f60808ec78a470b92dfbff91504"
}
```

[>>> 回到目录](#top)

## 离开一个组

**API**: ```*/api/v1/group/leave```

- 方法: POST
- 参数：group_id `组 ID`

**Example**:

```bash
curl -k -X POST -H 'Content-Type: application/json' -d '{"group_id":"<846011a8-1c58-4a35-b70f-83195c3bc2e8>"}' https://127.0.0.1:8002/api/v1/group/leave
```

调用 API 返回:

```json
{
    "group_id": "846011a8-1c58-4a35-b70f-83195c3bc2e8",
    "signature": "304402201818acb8f1358b65aecd0343a48f0fe79c89c3f2852fa809dd6b9315a20740e4022026d0ca3b981ee2a3701930b62d7f5ddcf959a3ba50d926c31f6c143ef91f024a"
}
```

[>>> 回到目录](#top)

## 组创建者删除组 <font color="yellow"><sup>废弃</sup></font>

## 获取组的种子

**API**:  ```*/api/v1/group/{group_id}/seed```

- 方法: Get
- 参数：group_id `组 ID`

**Example**:

```bash
curl -k -X GET -H 'Content-Type: application/json' -d '' https://127.0.0.1:8003/api/v1/group/<c0c8dc7d-4b61-4366-9ac3-fd1c6df0bf55>/seed
```

返回值如上述创建组返回的种子。

[>>> 回到目录](#top)

# 网络和同步

## 获取网络信息

**API**:  ```*/api/v1/network```

- 方法: GET
- 参数: none

**Example**:

```bash
curl -k https://127.0.0.1:8002/api/v1/network
```

调用 API 返回:

```json
{
    "peer_id": "16Uiu2HAmQtEhi1PUHdgXuBJTWyopSbLCXy52o",
    "eth_addr": "0x88221ae4A2118d0E19f6bf3237CFA8D7862571E6",
    "nat_type": "Unknown",
    "nat_enabled": true,
    "addrs": [
        "/ip4/127.0.0.1/tcp/7002"
    ],
    "groups": [
        {
            "GroupId": "446b33ac-7c0b-4167-8e77-f129952137b5",
            "GroupName": "my_test_group",
            "Peers": [
                "16Uiu2HAmJahkyu3zfuuxpdavESqLrjm4o4iMttqg"
            ]
        }
    ],
    "node": {}
}
```

[>>> 回到目录](#top)

## 开始同步

**API**: ```*/api/v1/group/{group_id}/startsync```

- 方法: POST
- 参数: group_id `组 ID`

**Example**:

```bash
curl -k -X POST -H 'Content-Type: application/json' -d '' https://127.0.0.1:8002/api/v1/group/<446b33ac-7c0b-4167-8e77-f129952137b5>/startsync
```

调用 API 返回:
- ```{"GroupId":<GROUP_ID>,"Error":""}``` 组正常开始同步，同时组的状态会变为 SYNCING
- ```{"error":"GROUP_ALREADY_IN_SYNCING"}``` 组当前正在同步中

[>>> 回到目录](#top)

# 内容 API

## 发送内容到组

**API**: ```*/api/v1/group/content```

- 方法: POST
- 参数:
  - `type`: 要发送的对象分类，类型是下面三个之一
    - "Add" 发送内容
    - "Like" 点赞
    - "Dislike" 点踩
  - `object`: 要发送的对象
    - `type`："Note"（与上面的 "Add" 对应），"Like" 或 "Dislike"，如果是 "Note"，则有如下参数：
        - `name`: 内容命名，可选
        - `content`: 要发送的内容文本，如果有下面的 `image` 参数，则是可选的
        - `image`: 要发送的图片，如果有上面的 `content` 参数，则是可选的。该参数是一个列表，每张图片包含下面三个参数，最多 4 张，且总大小小于 200kb
            - `mediaType`: 图片的类型，如 "image/jpeg"
            - `content`: 图片字节 base64 编码后，utf-8 解码为字符串
            - `name`: 图片名
        - `inreplyto`: 回复，可选参数，如果有，发送的内容回复指定的 Trx
            - `trxid`: `Trx ID`
    - 如果 `type` 是 "Like" 或 "Dislike"，则有如下参数：
        - `id`: `Trx ID`，点赞或点踩指定的 Trx
  - `target`: 发送到的目标，目前就是发送到组。有如下参数：
    - `id`: `组 ID`
    - `type`: "Group"

**Example**:

```bash
curl -k -X POST -H 'Content-Type: application/json'  -d '{"type":"Add","object":{"type":"Note","content":"simple note by aa","name":"A simple Node id1"},"target":{"id":"c0c8dc7d-4b61-4366-9ac3-fd1c6df0bf55","type":"Group"}}'  https://127.0.0.1:8002/api/v1/group/content
```

参数如：

```json
{
    "type": "Add",
    "object": {
        "type": "Note",
        "content": "simple note by aa",
        "name": "A simple Node id1"
    },
    "target": {
        "id": "c0c8dc7d-4b61-4366-9ac3-fd1c6df0bf55",
        "type": "Group"
    }
}
```

调用 API 返回:

```json
{
    "trx_id": "c60ed78e-df15-4408-9b5b-f87158cf0bda"
}
```

[>>> 回到目录](#top)

### 仅发送文本

参数如：

```json
{
    "type": "Add",
    "object": {
        "type": "Note",
        "content": "Good Morning!\nHave a nice day."
    },
    "target": {
        "id": "c60ed78e-df15-4408-9b5b-f87158cf0bda",
        "type": "Group"
    }
}
```

[rum-app](https://github.com/rumsystem/rum-app) 论坛模板用 `object.name` 作为标题，因此该字段不能是空字符串 `""`，如：

```json
{
    "type": "Add",
    "object": {
        "type": "Note",
        "content": "Good Morning!\nHave a nice day.",
        "name": "my first forum!"
    },
    "target": {
        "id": "c60ed78e-df15-4408-9b5b-f87158cf0bda",
        "type": "Group"
    }
}
```

### 图文一起发

参数如：

```json
{
    "type": "Add",
    "object": {
        "type": "Note",
        "content": "Good Morning!\nHave a nice day.",
        "name": "",
        "image": [
            {
                "mediaType": "image/png",
                "content": "this is pic content by base64.b64encode(pic-content-bytes).decode(\"utf-8\")",
                "name": "pic-name init by uuid like f\"{uuid.uuid4()}-{datetime.now().isoformat()}\""
            }
        ]
    },
    "target": {
        "id": "d87b93a3-a537-473c-8445-609157f8dab0",
        "type": "Group"
    }
}
```

### 回复

参数如：

```json
{
    "type": "Add",
    "object": {
        "type": "Note",
        "content": "can’t agree more! thx.",
        "inreplyto": {
            "trxid": "08c6ee4d-0310-47cf-988e-3879321ef274"
        }
    },
    "target": {
        "id": "d87b93a3-a537-473c-8445-609157f8dab0",
        "type": "Group"
    }
}
```

### 点赞或点踩

参数如：

```json
{
    "type": "Like",
    "object": {
        "id": "578e65d0-9b61-4937-8e7c-f00e2b262753"
    },
    "target": {
        "id": "c0c8dc7d-4b61-4366-9ac3-fd1c6df0bf55",
        "type": "Group"
    }
}
```

[>>> 回到目录](#top)

## 更新组内用户配置

任何一个组都有自己的用户配置可以更新。

**API**: ```*/api/v1/group/profile```

- 方法: POST
- 参数:
  - `type`："Update"
  - `person`: 配置相关，有以下参数：
    - `name`: 用户名
    - `image`: 头像，可选，不提供使用系统默认头像。有以下参数：
      - `mediaType`: 图片的类型，如 "image/jpeg"
      - `content`: 图片字节 base64 编码后，utf-8 解码为字符串
    - `wallet`: 钱包，可选参数。以 mixin 账号为例，有以下参数：
      - `id`: mixin 账号 uuid
      - `type`: "mixin",
      - `name`: "mixin messenger"
  - `target`：同上述发送内容到组
    - `id`
    - `type`

调用 API 返回:

```json
{
    "trx_id": "c60ed78e-df15-4408-9b5b-f87158cf0bda"
}
```

**Example**:

```bash
curl -k -X POST -H 'Content-Type: application/json'  -d '<Params>'  https://127.0.0.1:8002/api/v1/group/profile
```

**Params** 如:

```json
{
    "type": "Update",
    "person": {
        "name": "nickname",
        "image": {
            "mediaType": "image/png",
            "content": "there will be bytes content of images"
        },
        "wallet": [
            {
                "id": "bae95683-eabb-211f-9588-12dadffd0323",
                "type": "mixin",
                "name": "mixin messenger"
            }
        ]
    },
    "target": {
        "id": "c0c8dc7d-4b61-4366-9ac3-fd1c6df0bf55",
        "type": "Group"
    }
}
```

[>>> 回到目录](#top)


## 获取组内所有内容

每条内容以 Trx 来 “标记”，可分为 Note（向组内发送的内容）, Person profile（用户在组内的配置信息）Like/Dislike（点赞/点踩）

**API**: ```*/api/v1/group/{group_id}/content```

这个 api 将会废弃，目前保留仅供调试用。

- 方法: GET
- 参数：group_id `组 ID`

**Example**:

```bash
curl -k -X GET -H 'Content-Type: application/json' -d '' https://127.0.0.1:8003/api/v1/group/446b33ac-7c0b-4167-8e77-f129952137b5/content
```

## 按要求获取内容

**API**: ```*/app/api/v1/group/{group_id}/content?starttrx={trx_id}&num={n}```

**TIPS:** 这个 API 比其它常见 API 多了一个 `/app`

- 方法: POST
- 参数:
  - group_id：组 ID
  - reverse：true 或 false，不提供默认 false，如果是 true，反向获取，从最新的开始
  - starttrx 或 includestarttrx：起始 `Trx ID`, 一个不包含，一个包含
  - num: 要获取内容条数，不提供该参数默认获取 20 条
  - senders: 内容发布者的 `用户公钥` 列表，有该参数则只获取列表内发布者发布的内容

**Example**:

```bash
curl -v -X POST -H 'Content-Type: application/json' -d '{"senders":[ "CAISIQP8dKlMcBXzqKrnQSDLiSGWH+bRsUCmzX42D9F41CPzag=="]}' "http://localhost:8002/app/api/v1/group/5a3224cc-40b0-4491-bfc7-9b76b85b5dd8/content?starttrx=95f74d77-b15a-4cf5-a964-1c367c1b1909&num=200"
```

senders 参数如：
```json
{
    "senders": [
        "CAISIQP8dKlMcBXzqKrnQSDLiSGWH+bRsUCmzX42D9F41CPzag=="
    ]
}
```

调用 API 返回的是 Trx 的列表，如：

```json
[
    {
        "TrxId": "f9d0e9ca-53a9-4e1c-bed1-65c624ea4185",
        "Publisher": "CAISIQP8dKlMcBXzqKrnQSDLiSGWH+bRsUCmzX42D9F41CPzag==",
        "Content": {
            "type": "Note",
            "content": "simple note by aa",
            "name": "A simple Node id1"
        },
        "TypeUrl": "quorum.pb.Object",
        "TimeStamp": 1646961512914503200
    }
]
```

部分参数介绍：
- Publisher：发布者的 `用户公钥`

## 内容相关 Trx 介绍

### Note Trx

- 内容的类型: "Note"
- "TypeUrl": "quorum.pb.Object"

```json
{
    "TrxId": "da2aaf30-39a8-4fe4-a0a0-44ceb71ac013",
    "Publisher": "CAISIQOlA37+ghb05D5ZAKExjsto/H7eeCmkagcZ+BY/pjSOKw==",
    "Content": {
        "type": "Note",
        "content": "simple note by aa",
        "name": "A simple Node id1"
    },
    "TypeUrl": "quorum.pb.Object",
    "TimeStamp": 1629748212762123400
}
```

### 点赞/点踩 Trx

- 内容类型: "Like" 或 "Dislike"
- "TypeUrl": "quorum.pb.Object"

```json
{
    "TrxId": "65de2397-2f35-4a07-9af2-35a920b79882",
    "Publisher": "CAISIQMbTGdEDACml0BOcBXpWM6FOLDgH7u9VapHJ+wDMZSObw==",
    "Content": {
        "id": "02c23edc-be7d-4a32-bbae-fb8e179e9c5b",
        "type": "Like"
    },
    "TypeUrl": "quorum.pb.Object",
    "TimeStamp": 1639980884426949600
}
```

### 用户配置 Trx

- "TypeUrl": "quorum.pb.Person"

```json
{
    "TrxId": "7d5e4f23-42c5-4466-9ae3-ce701dfff2ec",
    "Publisher": "CAISIQNK024r4gdSjIK3HoQlPbmIhDNqElIoL/6nQiYFv3rTtw==",
    "Content": {
        "name": "Lucy",
        "image": {
            "mediaType": "image/png",
            "content": "there will be bytes content of images"
        },
        "wallet": [
            {
                "id": "bae95683-eabb-212f-9588-12dadffd0323",
                "type": "mixin",
                "name": "mixin messenger"
            }
        ]
    },
    "TypeUrl": "quorum.pb.Person",
    "TimeStamp": 1637574058426424900
}
```

[>>> 回到目录](#top)

# 块

## 获取块信息

**API**: ```*/api/v1/block/{group_id}/{block_id}```

- 方法: GET
- 参数:
  - group_id `组 ID`
  - block_id `块 ID`

**Example**:

```bash
curl -k -X GET -H 'Content-Type: application/json' -d '' https://127.0.0.1:8003/api/v1/block/<GROUP_ID>/<BLOCK_ID>
```

调用 API 返回:

```json
{
    "BlockId": "aa75447f-b621-4424-a723-9d4bf1d9fff9",
    "GroupId": "a4b634c2-ceb7-4e60-9584-a221aa7b6855",
    "PrevBlockId": "78bffd23-2dba-408b-b88e-ed3f5f005411",
    "PreviousHash": "ZXh7C2Fnp4J8ny96Udo2Nr3Z50zu+KdA4BcEiw7cF4s=",
    "Trxs": [
        {
            "TrxId": "820d6b65-99b8-4b96-afb1-0b639a76e1f3",
            "GroupId": "a4b634c2-ceb7-4e60-9584-a221aa7b6855",
            "Data": "CiR0eXBlLmdvb2dsZWFwaXMuY29tL3F1b3J1bS5wYi5PYmplY3QSKxIETm90ZTIRc2ltcGxlIG5vdGUgYnkgYWFCEEEgc2ltcGxlIE5vZGUgaWQ=",
            "TimeStamp": 1631817240704625000,
            "Version": "ver 0.01",
            "Expired": 1631817540704625200,
            "SenderPubkey": "CAISIQJHvBByFpoeT6SBvE+w3FTs5zRTq19hi7GP0fTVkj00hw==",
            "SenderSign": "MEUCIBwTg4UzSub5IUl4NVEZmMmkG8Kx2XMZCHIThoLdAtBoAiEAoCM5f/vYbUVIqdgS40vVueb954duzIjrzMDzHmE8h6s="
        }
    ],
    "ProducerPubKey": "CAISIQJHvBByFpoeT6SBvE+w3FTs5zRTq19hi7GP0fTVkj00hw==",
    "Hash": "RnChfYe3rBsO5swKoSDV5K8spV+NL5kaJ3aH1w/73lU=",
    "Signature": "MEYCIQC9Rnj381tjLmo8XwW0kpOCQb5o62QN78L4a6QsXIA37gIhALVClUs9UB32f7wQTUmoVg58uLr6r3apGkNyKh1uek4i",
    "Timestamp": 1631817245705639200
}
```

部分参数介绍：
- PrevBlockId：上一个块的 ID
- Trxs：Trx 列表，一个块可包含多个 Trx
- SenderPubkey：发送者的 `用户公钥`

[>>> 回到目录](#top)

# Trx

## 关于 Trx

Trx 生命周期，加密和出块过程

**Trx 种类**

所有链上操作均以 Trx “标记” 记录，Trx 的类型有：

- "POST"
- "SCHEMA"
- "PRODUCER"
- "ANNOUNCE"
- "REQ_BLOCK_FORWARD"
- "REQ_BLOCK_BACKWARD"
- "REQ_BLOCK_RESP"
- "BLOCK_SYNCED"
- "BLOCK_PRODUCED"
- "USER"
- "ASK_PEERID"
- "ASK_PEERID_RESP"
- "CHAIN_CONFIG"
- "APP_CONFIG"

**Trx 加密类型**

- "POST" 类型的 Trx
  - "private" 组： 每个发送节点都要根据自己手中的组内成员名单（`用户公钥` 名单），对 POST 的内容进行非对称加密，然后发送，收到 trx 的节点使用自己的公钥对 trx 进行解密
  - "public" 组： 每个发送节点都用 `seed` 中的 `cipher_key` 对称加密密钥对收发的 trx 数据进行对称加密

- 其他类型 Trx 与 "public" 组加密类型相同

**出块流程/共识策略**

一个 Trx 被 push 到链上后，根据组的不同共识类型，将被采取不同形式对待。

共识类型有 "poa", "pos" 或 "pow", 当前是 "poa"

**Trx 状态判断**

同其他链相似，Trx 的发送没有重试机制，客户端应自己保存并判断一个 Trx 的状态，具体过程如下

1. 发送一个 trx 时，获取 trx_id

2. 将这个 trx 标记为 “发送中”

3. 设置一个超时，目前建议是 30 秒

4. 在组内的内容中不断查询，直到相同 trx_id 出现，即可认为 trx 发送成功（被包含在块中）

5. 如果超时被触发，没有查到结果，即认为发送 trx 失败，客户端可以自行处理重发

[>>> 回到目录](#top)

## 获取 Trx 信息

**API**: ```*/api/v1/trx/{group_id}/{trx_id}```

- 方法: GET
- 参数:
  - group_id `组 ID`
  - trx_id `Trx ID`

**Example**:

```bash
curl -k -X GET -H 'Content-Type: application/json' -d '' https://127.0.0.1:8003/api/v1/trx/<GROUP_ID>/<TRX_ID>
```

调用 API 返回：

```json
{
    "TrxId": "c63d7c8e-d56d-432c-aae3-7d0d9dc34c31",
    "GroupId": "3bb7a3be-d145-44af-94cf-e64b992ff8f0",
    "Data": "rx5hmlGgIgnQSm5tT75KY96UaIauDALPvPLjRRe2qiwJhc8VI3wwpsm2M3Y4bYCXGhpjWVDc3D5pHr+cnhuUqWZWQUZJ8FkGYG+bHnz0t4z2//6xo+3+GrCogphT+vJHPCld3womShSLEo4G3VTBbBzaPOnSg1T31OuI8wRsKoslI1owKiWC4r5VwhXHmLq8RW+HFpIy7PqZXxr+8Hsojawrs0B9CbJ3wf7TWubUlw5JhpAXGbbBBw6nLyGM7MnL0+Q3nUi1mX9dgGWOEwwxvO66SYhB",
    "TimeStamp": "1639570707554262200",
    "Version": "1.0.0",
    "Expired": 1639571007554262200,
    "SenderPubkey": "CAISIQKwLxW1uBoZHMbss9QTdVLb8lfBhvMQ3ucnm9afGnVmpQ==",
    "SenderSign": "MEQCIGKc0MyiusNFWZEc+ZMXzk/eev7Sdouii4zAeSIGCqnMAiAz+LMXWck1NIJLB8U7mGmetzYGuTYPKxifH7sF1cMwZg=="
}
```

[>>> 回到目录](#top)

# Producers

## 关于 producers

Producer 作为组内 “生产者”，可以代替 Owner 出块，组内有其他 Producer 之后，Owenr 可以不用保持随时在线，在 Owner 下线的时间内，Producer 将代替 Owner 执行收集 Trx 并出块的任务

Owner 是组内第一个 Producer，有其它 Producer 时，Producer 与 Owner 可同时在线出块

## Producer 申请

**API**: ```*/api/v1/group/announce```

- 方法: POST
- 参数:
  - group_id：`组 ID`
  - action："add" 申请 或 "remove" 取消申请（或在已是 Producer 时申请退出 Producer）
  - type："producer" 或 "user"，如果是 "user" 见后面 [User 申请](#user-申请)
  - memo：Memo

**Example**:

```bash
curl -k -X POST -H 'Content-Type: application/json' -d '{"group_id":"5ed3f9fe-81e2-450d-9146-7a329aac2b62", "action":"add", "type":"producer", "memo":"producer p1, realiable and cheap, online 24hr"}' https://127.0.0.1:8005/api/v1/group/announce | jq
```

参数如:

```json
{
    "group_id": "5ed3f9fe-81e2-450d-9146-7a329aac2b62",
    "action": "add",
    "type": "producer",
    "memo": "producer p1, realiable and cheap, online 24hr"
}
```

调用 API 返回:

```json
{
    "group_id": "5ed3f9fe-81e2-450d-9146-7a329aac2b62",
    "sign_pubkey": "CAISIQOxCH2yVZPR8t6gVvZapxcIPBwMh9jB80pDLNeuA5s8hQ==",
    "encrypt_pubkey": "",
    "type": "AS_PRODUCER",
    "action": "ADD",
    "sign": "3046022100a853ca31f6f6719be213231b6428cecf64de5b1042dd8af1e140499507c85c40022100abd6828478f56da213ec10d361be8709333ff44cd0fa037409af9c0b67e6d0f5",
    "trx_id": "2e86c7fb-908e-4528-8f87-d3548e0137ab"
}
```

部分参数介绍：
- sign_pubkey：申请者的组内 `用户公钥`
- type：申请类型
- sign：申请者的签名

[>>> 回到目录](#top)

## 获取提交申请的 Producers

**API**: ```*/api/v1/group/{group_id}/announced/producers```

- 方法: GET
- 参数:
  - group_id：`组 ID`

**Example**:

```bash
curl -k -X GET -H 'Content-Type: application/json' -d '' https://127.0.0.1:8002/api/v1/group/5ed3f9fe-81e2-450d-9146-7a329aac2b62/announced/producers
```

调用 API 返回:

```json
[
    {
        "AnnouncedPubkey": "CAISIQOxCH2yVZPR8t6gVvZapxcIPBwMh9jB80pDLNeuA5s8hQ==",
        "AnnouncerSign": "3046022100a853ca31f6f6719be213231b6428cecf64de5b1042dd8af1e140499507c85c40022100abd6828478f56da213ec10d361be8709333ff44cd0fa037409af9c0b67e6d0f5",
        "memo": "",
        "Result": "ANNOUCNED",
        "Action": "Add",
        "TimeStamp": 1634756064250457600
    }
]
```

部分参数介绍：
- AnnouncedPubkey：申请者的 `用户公钥`
- AnnouncerSign：申请者的签名
- Result："ANNOUCNED" 已申请 或 "APPROVED" 已经被批准
- Action："Add" 申请成为 或 "REMOVE" 已取消申请（或在已是 Producers 时申请退出）

[>>> 回到目录](#top)

## Owner 批准/移除 Producer

**API**: ```*/api/v1/group/producer```

- 方法: POST
- 参数:
  - producer_pubkey：申请者（或已经是 Producer）的 `用户公钥`
  - group_id：组 ID
  - action："add" 批准成为（"ANNOUCNED" 且是 "ADD") 或 "remove" 移除已经批准的 Producer

**Example**:

```bash
curl -k -X POST -H 'Content-Type: application/json' -d '{"producer_pubkey":"CAISIQOxCH2yVZPR8t6gVvZapxcIPBwMh9jB80pDLNeuA5s8hQ==","group_id":"5ed3f9fe-81e2-450d-9146-7a329aac2b62", "action":"add"}' https://127.0.0.1:8002/api/v1/group/producer | jq
```

参数如:

```json
{
    "producer_pubkey": "CAISIQOxCH2yVZPR8t6gVvZapxcIPBwMh9jB80pDLNeuA5s8hQ==",
    "group_id": "5ed3f9fe-81e2-450d-9146-7a329aac2b62",
    "action": "add"
}
```

调用 API 返回:

```json
{
    "group_id": "5ed3f9fe-81e2-450d-9146-7a329aac2b62",
    "producer_pubkey": "CAISIQOxCH2yVZPR8t6gVvZapxcIPBwMh9jB80pDLNeuA5s8hQ==",
    "owner_pubkey": "CAISIQNVGW0jrrKvo9/40lAyz/uICsyBbk465PmDKdWfcCM4JA==",
    "sign": "304402202cbca750600cd0aeb3a1076e4aa20e9d1110fe706a553df90d0cd69289628eed022042188b48fa75d0197d9f5ce03499d3b95ffcdfb0ace707cf3eda9f12473db0ea",
    "trx_id": "6bff5556-4dc9-4cb6-a595-2181aaebdc26",
    "memo": "",
    "action": "ADD"
}
```

[>>> 回到目录](#top)

## 获取已经批准的 Producers

**API**: ```*/api/v1/group/{group_id}/producers```

- 方法: GET
- 参数:
  - group_id：组 ID

**Example**:

```bash
curl -k -X GET -H 'Content-Type: application/json' -d '' https://127.0.0.1:8005/api/v1/group/5ed3f9fe-81e2-450d-9146-7a329aac2b62/producers | jq
```

调用 API 返回:

```json
[
    {
        "ProducerPubkey": "CAISIQNVGW0jrrKvo9/40lAyz/uICsyBbk465PmDKdWfcCM4JA==",
        "OwnerPubkey": "CAISIQNVGW0jrrKvo9/40lAyz/uICsyBbk465PmDKdWfcCM4JA==",
        "OwnerSign": "3046022100e29a892a9e66f9a736a7d9672db7bd9e2431b8bcff6d407723303a14bc53c66e022100ecf61ce2ff95109fb6504094104afca7074a7c96ac79733cab98cef0e5f85baf",
        "TimeStamp": 1634755122424178000,
        "BlockProduced": 3
    },
    {
        "ProducerPubkey": "CAISIQOxCH2yVZPR8t6gVvZapxcIPBwMh9jB80pDLNeuA5s8hQ==",
        "OwnerPubkey": "CAISIQNVGW0jrrKvo9/40lAyz/uICsyBbk465PmDKdWfcCM4JA==",
        "OwnerSign": "304402202cbca750600cd0aeb3a1076e4aa20e9d1110fe706a553df90d0cd69289628eed022042188b48fa75d0197d9f5ce03499d3b95ffcdfb0ace707cf3eda9f12473db0ea",
        "TimeStamp": 1634756661280204800,
        "BlockProduced": 0
    }
]
```

部分参数介绍：
- BlockProduced：该 Producer 当前出块数

[>>> 回到目录](#top)

# DeniedList <font color="yellow"><sup>废弃</sup></font>

# 组的配置

## Owner 更新组的配置

**API**:  ```*/api/v1/group/appconfig```

- 方法: POST
- 参数:
  - group_id: 组 ID
  - name: 配置项的名称, 目前 [rum-app](https://github.com/rumsystem/rum-app) 支持 'group_announcement'(组的公告),'group_desc'(组的简介),'group_icon'(组的图标), 均是 "string" 类型
  - type: 配置项的类型, 可选值为 "int", "bool", "string"
  - value: 配置项的值, 必须与 type 相对应
  - action: "add" 或 "del", 增加/修改 或 删除
  - memo: Memo

**Example**:

```bash
curl -k -X POST -H 'Content-Type: application/json' -d '{"action":"add", "group_id":"c8795b55-90bf-4b58-aaa0-86d11fe4e16a", "name":"test", "type":"string", "value":"afafa", "memo":"add test_bool to group"}' https://127.0.0.1:8002/api/v1/group/config | jq
```

参数如:

```json
{
    "action": "add",
    "group_id": "c8795b55-90bf-4b58-aaa0-86d11fe4e16a",
    "name": "test",
    "type": "string",
    "value": "afafa",
    "memo": "add test to group"
}
```

调用 API 返回:

```json
{
    "group_id": "c8795b55-90bf-4b58-aaa0-86d11fe4e16a",
    "sign": "3045022100e1375e48cfbd51cb78afc413fcca084deae9eb7f8454c54832feb9ae00fada7702203ee6fe2292ea3a87d687ae3369012b7518010e555b913125b8a7bf54f211502a",
    "trx_id": "9e54c173-c1dd-429d-91fa-a6b43c14da77"
}
```

[>>> 回到目录](#top)

## 获取组的配置列表

**API**:  ```*/api/v1/group/{group_id}/config/keylist```

- 方法: GET
- 参数:
  - group_id：组 ID

**Example**:

```bash
curl -k -X GET -H 'Content-Type: application/json' -d '{}' https://127.0.0.1:8002/api/v1/group/c8795b55-90bf-4b58-aaa0-86d11fe4e16a/config/keylist
```

调用 API 返回:

```json
[
    {
        "Name": "test",
        "Type": "STRING"
    }
]
```

参数介绍:
- name 配置项的名称 
- type 配置项的类型

[>>> 回到目录](#top)

## 获取某个配置项的信息

**API**:  ```*/api/v1/group/{group_id}/config/{KEY_NAME}```

- 方法: GET
- 参数:
  - group_id：组 ID
  - key_name：配置项名称

**Example**:

```bash
curl -k -X GET -H 'Content-Type: application/json' -d '{}' https://127.0.0.1:8002/api/v1/group/c8795b55-90bf-4b58-aaa0-86d11fe4e16a/config/test | jq
```

调用 API 返回:

```json
{
    "Name": "test",
    "Type": "STRING",
    "Value": "afafa",
    "OwnerPubkey": "CAISIQJOfMIyaYuVpzdeXq5p+ku/8pSB6XEmUJfHIJ3A0wCkIg==",
    "OwnerSign": "304502210091dcc8d8e167c128ef59af1b6e2b2efece499043cc149014303b932485cde3240220427f81f2d7482df0d9a4ab2c019528b33776c73daf21ba98921ee6ff4417b1bc",
    "Memo": "add test to group",
    "TimeStamp": 1639518490895535600
}
```

[>>> 回到目录](#top)

## Owner 更新组的 Schema

**API**:  ```*/api/v1/group/schema```

- 方法: POST
- 参数:
  - group_id：组 ID
  - rule：Schema 规则
  - type：Schema 的类型
  - aciton："add" 或 "remove", 添加或删除
  - memo：Memo

**Example**:

```bash
curl -k -X POST -H 'Content-Type: application/json' -d '{"rule":"new_schema","type":"schema_type", "group_id":"13a25432-b791-4d17-a52f-f69266fc3f18", "action":"add", "memo":"memo"}' https://127.0.0.1:8002/api/v1/group/schema
```

参数如：

```json
{
    "rule": "new_schema",
    "type": "schema_type",
    "group_id": "13a25432-b791-4d17-a52f-f69266fc3f18",
    "action": "add",
    "memo": "memo"
}
```

[>>> 回到目录](#top)

## 获取组的 Schema

**API**:  ```*/api/v1/group/{group_id}/schema```

- 方法: GET
- 参数:
  - group_id：组 ID

**Example**:

```bash
curl -k -X GET -H 'Content-Type: application/json' -d '{}' https://127.0.0.1:8002/api/v1/group/13a25432-b791-4d17-a52f-f69266fc3f18/app/schema | jq
```

调用 API 返回:

```json
[
    {
        "Type": "schema_type",
        "Rule": "new_schema",
        "TimeStamp": 1636047963013888300
    }
]
```

[>>> 回到目录](#top)

# 私有组

"private" 类型的组。任何节点加入私有组，如果没被 Owner 批准成为该组的用户，则无法获取到 Content，即能拿到 trxs 但 trx 的 Content 字段为空，以此保证组的内容隐私。

## User 申请

**API**: ```*/api/v1/group/announce```

- 方法: POST
- 参数:
  - group_id：组 ID
  - action："add" 申请成为 或 "remove" 取消申请（或在已经是 User 时申请退出，退出是指退出私有组用户，而不是退出组，随时可以退出组）
  - type："producer" 或 "user"，如果是 "producer" 见前面 [Producer 申请](#producer-申请)
  - memo：Memo

**Example**:

```bash
curl -k -X POST -H 'Content-Type: application/json' -d '{"group_id":"5ed3f9fe-81e2-450d-9146-7a329aac2b62", "action":"add", "type":"user", "memo":"invitation code:a423b3"}' https://127.0.0.1:8003/api/v1/group/announce | jq
```

参数如:

```json
{
    "group_id": "5ed3f9fe-81e2-450d-9146-7a329aac2b62",
    "action": "add",
    "type": "user",
    "memo": "invitation code:a423b3"
}
```

调用 API 返回:

```json
{
    "group_id": "5ed3f9fe-81e2-450d-9146-7a329aac2b62",
    "sign_pubkey": "CAISIQJwgOXjCltm1ijvB26u3DDroKqdw1xjYF/w1fBRVdScYQ==",
    "encrypt_pubkey": "age1fx3ju9a2f3kpdh76375dect95wmvk084p8wxczeqdw8q2m0jtfks2k8pm9",
    "type": "AS_USER",
    "action": "ADD",
    "sign": "304402206a68e3393f4382c9978a19751496e730de94136a15ab77e30bab2f184bcb5646022041a9898bb5ff563a6efeea29b30bac4bebf0d3464eb326fd84322d98919b3715",
    "trx_id": "8a4ae55d-d576-490a-9b9a-80a21c761cef"
}
```

部分参数介绍：
- sign_pubkey：申请者的 `用户公钥`
- encrypt_pubkey：加密公钥

[>>> 回到目录](#top)

## 获取申请成为私有组用户的申请列表

**API**: ```*/api/v1/group/{group_id}/announced/users```

- 方法: GET
- 参数:
  - group_id：组 ID

**Example**:

```bash
curl -k -X GET -H 'Content-Type: application/json' -d '' https://127.0.0.1:8002/api/v1/group/5ed3f9fe-81e2-450d-9146-7a329aac2b62/announced/users
```

调用 API 返回:

```json
[
    {
        "AnnouncedSignPubkey": "CAISIQIWQX/5Nmy2/YoBbdO9jn4tDgn22prqOWMYusBR6axenw==",
        "AnnouncedEncryptPubkey": "age1a68u5gafkt3yfsz7pr45j5ku3tyyk4xh9ydp3xwpaphksz54kgns99me0g",
        "AnnouncerSign": "30450221009974a5e0f3ea114de8469a806894410d12b5dc5d6d7ee21e49b5482cb062f1740220168185ad84777675ba29773942596f2db0fa5dd810185d2b8113ac0eaf4d7603",
        "Result": "ANNOUNCED"
    }
]
```

部分参数介绍:
- AnnouncedPubkey：申请者的 `用户公钥`
- AnnouncedEncryptPubkey：用于申请的加密公钥
- Result："ANNOUNCED" 已申请（已取消申请）或 "APPROVED" 已被批准

[>>> 回到目录](#top)

## Owner 批准/移除 User

**API**: ```*/api/v1/group/user```

- 方法: POST
- 参数:
  - user_pubkey：申请者（或已经是 User）的 `用户公钥`
  - group_id：组 ID
  - action："add" 批准成为（不能是已取消申请者）或 "remove" 移除已经批准的 User

**Example**:

```bash
curl -k -X POST -H 'Content-Type: application/json' -d '{"user_pubkey":"CAISIQOxCH2yVZPR8t6gVvZapxcIPBwMh9jB80pDLNeuA5s8hQ==","group_id":"5ed3f9fe-81e2-450d-9146-7a329aac2b62", "action":"add"}' https://127.0.0.1:8002/api/v1/group/user | jq
```

参数如:

```json
{
    "user_pubkey": "CAISIQOxCH2yVZPR8t6gVvZapxcIPBwMh9jB80pDLNeuA5s8hQ==",
    "group_id": "5ed3f9fe-81e2-450d-9146-7a329aac2b62",
    "action": "add"
}
```

调用 API 返回:

```json
{
    "group_id": "5ed3f9fe-81e2-450d-9146-7a329aac2b62",
    "user_pubkey": "CAISIQOxCH2yVZPR8t6gVvZapxcIPBwMh9jB80pDLNeuA5s8hQ==",
    "owner_pubkey": "CAISIQNVGW0jrrKvo9/40lAyz/uICsyBbk465PmDKdWfcCM4JA==",
    "sign": "304402202cbca750600cd0aeb3a1076e4aa20e9d1110fe706a553df90d0cd69289628eed022042188b48fa75d0197d9f5ce03499d3b95ffcdfb0ace707cf3eda9f12473db0ea",
    "trx_id": "6bff5556-4dc9-4cb6-a595-2181aaebdc26",
    "memo": "",
    "action": "ADD"
}
```

[>>> 回到目录](#top)

# 链端配置

## 关于链端配置

Owner 可以给组内用户授予某个或某些 `Trx 类型` 的操作权限。

以下 `Trx 类型` 是可配置的：

```sh
"POST"
"ANNOUNCE"
"REQ_BLOCK_FORWARD"
"REQ_BLOCK_BACKWARD"
"BLOCK_SYNCED"
"BLOCK_PRODUCED"
"ASK_PEERID"
```

每个 `Trx 类型` 有它自己的黑/白名单和 `Following 规则`， 对于用户，其拥有的权限遵循以下规则:

1. 如果一个用户的 `用户公钥` 在某个 `Trx 类型` 的白名单里，则该用户拥有发送这个 `Trx 类型` 的 Trx 的权限；
2. 如果一个用户的 `用户公钥` 在某个 `Trx 类型` 的黑名单里，则该组的 Owner/Producer 将拒绝该用户发送的所有该 `Trx 类型` 的 Trx；
3. 如果一个用户的 `用户公钥` 不在某个 `Trx 类型` 的白/名单里, 遵循以下规则:
    - a. 如果该 `Trx 类型` 的 `Following 规则` 设置为 `"FOLLOW_ALW_LIST"`, 则只有 `用户公钥` 加入该类型白名单的用户才拥有权限；
    - b. 如果该 `Trx 类型` 的 `Following 规则` 设置为 `"FOLLOW_DNY_LIST"`, 则只有 `用户公钥` 加入该类型黑名单的用户才失去权限；

如果一个用户被拒绝，他仍然可以发送 trx 并获取 trx_id，但 Owner/Producer 将拒绝该 trx，这意味着 trx 不会打包到块中并广播给组。因此，客户端应用程序应该检查组身份验证规则，以便将错误消息返回给用户。

[>>> 回到目录](#top)

## 获取某个 `Trx 类型` 的 `Following 规则`

**API**: ```*/api/v1/group/<group_id>/trx/auth/<trx_type>```

- 方法: GET
- 参数:
  - group_id：组 ID
  - trx_type：`Trx 类型`

**Example**:

```sh
curl -k -X GET -H 'Content-Type: application/json' -d '' https://127.0.0.1:8003/api/v1/group/b3e1800a-af6e-4c67-af89-4ddcf831b6f7/trx/auth/post | jq
```

调用 API 返回：

```json
{
    "TrxType": "POST",
    "AuthType": "FOLLOW_ALW_LIST"
}
```

参数:

- `TrxType` : `Trx 类型`
- `Authtype` : `Following 规则`，`FOLLOW_ALW_LIST` 或 `FOLLOW_DNY_LIST`

[>>> 回到目录](#top)

## 为某个 `Trx 类型` 设置 `Following 规则`

**API**: v1/group/chainconfig

- 方法: POST
- 参数:
  - `group_id`：组 ID
  - `type`：配置类型，必须是 "set_trx_auth_mode"
  - `config`：配置项目，字符串类型，包含以下参数：
    - `trx_type`：`Trx 类型`，字符串类型
    - `trx_auth_mode`：身份验证方式，必须是 "follow_alw_list" 或 "follow_dny_list"
  - `memo`：Memo

**Example**:

```sh
curl -k -X POST -H 'Content-Type: application/json' -d '{"group_id":"b3e1800a-af6e-4c67-af89-4ddcf831b6f7", "type":"set_trx_auth_mode", "config":"{\"trx_type\":\"POST\", \"trx_auth_mode\":\"follow_dny_list\"}", "Memo":"Memo"}' https://127.0.0.1:8003/api/v1/group/chainconfig | jq
```

参数如：

```json
{
    "group_id": "b3e1800a-af6e-4c67-af89-4ddcf831b6f7",
    "type": "set_trx_auth_mode",
    "config": "{\"trx_type\":\"POST\", \"trx_auth_mode\":\"follow_dny_list\"}",
    "Memo": "Memo"
}
```

调用 API 返回：

```json
{
    "group_id": "b3e1800a-af6e-4c67-af89-4ddcf831b6f7",
    "owner_pubkey": "CAISIQPLW/J9xgdMWoJxFttChoGOOld8TpChnGFFyPADGL+0JA==",
    "sign": "30440220089276796ceeef3a2c413bd89249475c2ecd8be4f2cb0ee3d19903fc45a7386b02206561bfdfb0338a9d022619dd8064e9a3496c1ea768f344e3c3850f8a907cdc73",
    "trx_id": "90e9818a-2e23-4248-93e3-d4ba1b100f4f"
}
```

[>>> 回到目录](#top)

## 更新某个/某些 `Trx 类型` 的黑/白名单

**API**: v1/group/chainconfig 

- 方法: POST
- 参数:
  - `group_id`：组 ID
  - `type`：配置类型，必须是 "upd_alw_list" 或 "upd_dny_list"
  - `config`：配置项目，字符串类型，包含以下参数：
    - `action`："add" 或 "remove"，添加 或 移除
    - `pubkey`：要添加或移除的用户的 `用户公钥`
    - `trx_type`：`Trx 类型`，单个或多个组成的数组
    - `memo`：Memo

**Example**:

```sh
curl -k -X POST -H 'Content-Type: application/json' -d '{"group_id":"b3e1800a-af6e-4c67-af89-4ddcf831b6f7", "type":"upd_alw_list", "config":"{\"action\":\"add\",  \"pubkey\":\"CAISIQNGAO67UTFSuWzySHKdy4IjBI/Q5XDMELPUSxHpBwQDcQ==\", \"trx_type\":[\"post\", \"announce\", \"req_block_forward\", \"req_block_backward\", \"ask_peerid\"]}", "Memo":"Memo"}' https://127.0.0.1:8003/api/v1/group/chainconfig | jq
```

参数如：

```json
{
    "group_id": "b3e1800a-af6e-4c67-af89-4ddcf831b6f7",
    "type": "upd_alw_list",
    "config": "{\"action\":\"add\",  \"pubkey\":\"CAISIQNGAO67UTFSuWzySHKdy4IjBI/Q5XDMELPUSxHpBwQDcQ==\", \"trx_type\":[\"post\", \"announce\", \"req_block_forward\", \"req_block_backward\", \"ask_peerid\"]}",
    "Memo": "Memo"
}
```

调用 API 返回：

```json
{
    "group_id": "b3e1800a-af6e-4c67-af89-4ddcf831b6f7",
    "owner_pubkey": "CAISIQPLW/J9xgdMWoJxFttChoGOOld8TpChnGFFyPADGL+0JA==",
    "sign": "30440220089276796ceeef3a2c413bd89249475c2ecd8be4f2cb0ee3d19903fc45a7386b02206561bfdfb0338a9d022619dd8064e9a3496c1ea768f344e3c3850f8a907cdc73",
    "trx_id": "90e9818a-2e23-4248-93e3-d4ba1b100f4f"
}
```

[>>> 回到目录](#top)

## 获取组的黑/白名单

**API**: v1/group/<group_id>/trx/allowlist

**API**: v1/group/<group_id>/trx/denylist

- 方法: Get
- 参数:
  - group_id：组 ID

**Example**:

获取白名单

```sh
curl -k -X GET -H 'Content-Type: application/json' -d '' https://127.0.0.1:8003/api/v1/group/b3e1800a-af6e-4c67-af89-4ddcf831b6f7/trx/allowlist
```

调用 API 返回：

```json
[
    {
        "Pubkey": "CAISIQNGAO67UTFSuWzySHKdy4IjBI/Q5XDMELPUSxHpBwQDcQ==",
        "TrxType": [
            "POST",
            "ANNOUNCE",
            "REQ_BLOCK_FORWARD",
            "REQ_BLOCK_BACKWARD",
            "ASK_PEERID"
        ],
        "GroupOwnerPubkey": "CAISIQPLW/J9xgdMWoJxFttChoGOOld8TpChnGFFyPADGL+0JA==",
        "GroupOwnerSign": "304502210084bc833278dc98be6f279540b571ad5402f5c2d1e978c4c2298cddb079ca312002205f9374b9d27c628815aecff4ffe11329b17b8be12687223a072afa58e9f15f2c",
        "TimeStamp": 1642609852758917000,
        "Memo": "Memo"
    }
]
```

部分参数介绍:

- Pubkey: 白名单中用户的 `用户公钥`
- TrxType: 该用户拥有哪些 `Trx 类型` 的权限（如果是黑名单，就是失去了哪些 `Trx 类型` 的权限）
- GroupOwnerPubkey：Owner 的 `用户公钥`

[>>> 回到目录](#top)

## 客户端如何使用 API

新建一个组，所有 `Trx 类型` 的 `Following 规则` 默认都是 `"FOLLOW_DNY_LIST"`, 如果不改变规则，则只要成为该组的用户，即拥有所有 `Trx 类型` 的权限。

### 完全拒绝一个用户

不需要改变 `Following 规则`，将下列 `Trx 类型` 及 `用户公钥` 加入黑名单：
- "POST"
- "ANNOUNCE"
- "REQ_BLOCK_FORWARD"
- "REQ_BLOCK_BACKWARD"
- "ASK_PEERID"

**Example**:

```sh
curl -k -X POST -H 'Content-Type: application/json' -d '{"group_id":"b3e1800a-af6e-4c67-af89-4ddcf831b6f7", "type":"upd_dny_list", "config":"{\"action\":\"add\",  \"pubkey\":\"CAISIQNGAO67UTFSuWzySHKdy4IjBI/Q5XDMELPUSxHpBwQDcQ==\", \"trx_type\":[\"post\", \"announce\", \"req_block_forward\", \"req_block_backward\", \"ask_peerid\"]}", "Memo":"Memo"}' https://127.0.0.1:8003/api/v1/group/chainconfig | jq
```

### 再次授予一个用户所有权限

将下列 `Trx 类型` 及 `用户公钥` 从黑名单中移除：
- "POST"
- "ANNOUNCE"
- "REQ_BLOCK_FORWARD"
- "REQ_BLOCK_BACKWARD"
- "ASK_PEERID"

**Example**:

```sh
curl -k -X POST -H 'Content-Type: application/json' -d '{"group_id":"b3e1800a-af6e-4c67-af89-4ddcf831b6f7", "type":"upd_dny_list", "config":"{\"action\":\"add\",  \"pubkey\":\"CAISIQNGAO67UTFSuWzySHKdy4IjBI/Q5XDMELPUSxHpBwQDcQ==\", \"trx_type\":[]}", "Memo":"Memo"}' https://127.0.0.1:8003/api/v1/group/chainconfig | jq
```

### 怎样设置单一作者模式

1. 更改 `"POST"` 的 `Following 规则` 为 `FOLLOW_ALW_LIST`

**Example**:

```sh
curl -k -X POST -H 'Content-Type: application/json' -d '{"group_id":"b3e1800a-af6e-4c67-af89-4ddcf831b6f7", "type":"set_trx_auth_mode", "config":"{\"trx_type\":\"POST\", \"trx_auth_mode\":\"follow_alw_list\"}", "Memo":"Memo"}' https://127.0.0.1:8003/api/v1/group/chainconfig | jq 
```

2. 将作者的 `用户公钥` 及 `"POST"` 添加到白名单

**Example**:

```sh
curl -k -X POST -H 'Content-Type: application/json' -d '{"group_id":"b3e1800a-af6e-4c67-af89-4ddcf831b6f7", "type":"upd_alw_list", "config":"{\"action\":\"add\",  \"pubkey\":\"CAISIQNGAO67UTFSuWzySHKdy4IjBI/Q5XDMELPUSxHpBwQDcQ==\", \"trx_type\":[\"post\"]}", "Memo":"Memo"}' https://127.0.0.1:8003/api/v1/group/chainconfig | jq
```

然后，现在仅作为作者的用户才有权限发内容。

同一个用户，同一个 `Trx 类型`，可以既在黑名单又在白名单中，这是有原因和有计划的。**白名单的优先级最高**，因此，在某个（些）`Trx 类型` 白名单中的用户，不管 `Following 规则` 是什么，也不管他（们）是否在这个（些）类型的黑名单中，总是拥有这个（些）类型的权限。 避免混淆，小心配置。

[>>> 回到目录](#top)

# 用自己擅长的语言开发

如果看到这里，欢迎你加入到 RUM 网络应用开发中来。然后，你可以：

1. 直接下载 [rum-app](https://docs.prsdev.club/#/rum-app/test)，或者自行编译 [quorum](https://github.com/rumsystem/quorum)
2. 运行 rum-app 或 启动你编译的 quorum 加入到 RUM 系统网络中来。你可以使用我们的公开节点 `/ip4/94.23.17.189/tcp/10666/p2p/16Uiu2HAmGTcDnhj3KVQUwVx8SGLyKBXQwfAxNayJdEwfsnUYKK4u` 或其他在线节点作为引导节点（`bootstrap`）启动 quorum
3. 采用你擅长的语言连接你启动的节点，进行开发。以 Python 为例：

```python
"""
PORT: int，本地启动的 Rum 节点的 端口号，该端口号启动时自动生成（rum-app）或自定义（quorum）
HOST: str，本地 IP，通常是 127.0.0.1
CACERT: str，本地启动的 Rum 节点的证书文件（server.crt）的绝对路径
"""

import requests

url = f"https://{HOST}:{PORT}"
session = requests.Session()
session.verify = CACERT
session.headers.update({
    "USER-AGENT": "RUMAPI",
    "Content-Type": "application/json"})

session.get(f"{url}/api/v1/node")
```

[>>> 回到目录](#top)

# 附录

### group_id

一个组的唯一身份标识，创建组即获得。

### group_name

组的名称，建组时自定义，不可修改。

### trx_id/TrxId

Trx 的唯一身份标识。

### block_id/BlockId

块的唯一身份标识，一个块可包含多个 Trx。

### node_id

自己的节点的唯一身份标识，创建节点即获得。

### peer_id

节点 ID，包含 node_id 以及其他网络中的节点的 ID。

特别注意，使用 API `"/api/v1/network/peers"` 时，节点 ID 应该包含公网 IP 等信息，例如：`"/ip4/110.14.103.110/tcp/1111/16Uiu2H..."`

### owner_pubkey/user_pubkey

`用户公钥`，是用户在组内的唯一身份标识，也用来进行签名。

### group_status

组的状态，有 3 种：
- SYNCING，正在同步
- SYNC_FAILED，同步失败
- IDLE，空闲

### app_key

可以看作组的类型，用来创建不同类型的组，长度在 5~20 字符之间。

### consensus_type

共识类型，有 "poa"，"pos" 或 "pow", 目前是 "poa"

### encryption_type

加密类型，必须是 "public" 或 "private"。

### TrxType/trx_type

`Trx 类型`，有：
- "POST"
- "SCHEMA"
- "PRODUCER"
- "ANNOUNCE"
- "REQ_BLOCK_FORWARD"
- "REQ_BLOCK_BACKWARD"
- "REQ_BLOCK_RESP"
- "BLOCK_SYNCED"
- "BLOCK_PRODUCED"
- "USER"
- "ASK_PEERID"
- "ASK_PEERID_RESP"
- "CHAIN_CONFIG"
- "APP_CONFIG"

### Authtype/trx_auth_mode

身份验证方式或称 `Following 规则`，有：
- "FOLLOW_ALW_LIST"
- "FOLLOW_DNY_LIST"

[>>> 回到目录](#top)

