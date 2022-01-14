import requests
import json


class Api:
    """
    Frequently used Rum Api. 

    Rum Api docs: https://github.com/rumsystem/quorum/blob/main/Tutorial.md
    """
    def __init__(self, PORT: int, HOST: str, CACERT: str):
        """
        PORT: Local node port number
        HOST: Local loopback address (127.0.0.1)
        CACERT: Absolute path of security certificate "server.crt"
        """

        self.BASEURL = f"https://{HOST}:{PORT}/api/v1"
        self.session = requests.Session()
        self.session.verify = CACERT
        self.session.headers.update({
            "USER-AGENT": "Rum Api",
            "Content-Type": "application/json",
        })

    def _get(self, url):
        """url: See below"""
        return self.session.get(url).json()

    def _post(self, url, **kwargs):
        """url, **kwargs: See below"""
        return self.session.post(url, **kwargs).json()

    def get_node(self):
        """Get node info.

        Return value such as:
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
        """
        return self._get(f"{self.BASEURL}/node")

    def get_network(self):
        """Get network info.

        Return value such as:
        {
            "groups": [
                {
                    "GroupId": "997ce496-661b-457b-8c6a-f57f6d9862d0",
                    "GroupName": "pb_group_1",
                    "Peers": [
                        "16Uiu2HAkuXLC2hZTRbWToCNztyWB39KDi8g66ou3YrSzeTbsWsFG"
                    ]
                }
            ],
            "node": {
                "addrs": [
                    "/ip4/192.168.20.17/tcp/7002",
                    "/ip4/127.0.0.1/tcp/7002",
                    "/ip4/107.159.4.35/tcp/65185"
                ],
                "ethaddr": "0x4daD72e78c3537a8852ca7b3d1742Dd42c30441A",
                "nat_enabled": true,
                "nat_type": "Public",
                "peerid": "16Uiu2HAm8XVpfQrJYaeL7XtrHC3FvfKt2QW7P8R3MBenYyHxu8Kk"
            }
        }
        """
        return self._get(f"{self.BASEURL}/network")

    def get_groups(self):
        """Get list all groups.

        Return value such as:
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
        """
        return self._get(f"{self.BASEURL}/groups")

    def get_group_content(self, group_id: str, trx_type: str = "note"):
        """Get group content.

        Args:
          group_id: Group ID.
          trx_type: "note","all","dlike" and "person",default "note".
        Rutern:
          - trx_type is "note", return Note Trx. Elements that return value such as:
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
          - trx_type is "person", return Person Profile Trx. Elements that return value such as:
            {
                "TrxId": "7d5e4f23-42c5-4466-9ae3-ce701dfff2ec",
                "Publisher": "CAISIQNK024r4gdSjIK3HoQlPbmIhDNqElIoL/6nQiYFv3rTtw==",
                "Content": {
                    "name": "Lucy",
                    "image": {
                        "mediaType": "image/png",
                        "content": "there will be base64 string content of images"
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
          - trx_type is "dlike", return Like/Dislike Trx. Elements that return value such as:
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
          - trx_type is "all", return to all above.
          """

        trxs = self._get(f"{self.BASEURL}/group/{group_id}/content")
        if trxs is None or 'error' in trxs:
            return []
        else:
            notes = []
            dlikes = []
            persons = []
            for trx in trxs:
                if "type" in trx["Content"]:
                    if trx["Content"]["type"] == "Note":
                        notes.append(trx)
                    elif trx["Content"]["type"] in ("Like", "Dislike"):
                        dlikes.append(trx)
                if trx["TypeUrl"] == "quorum.pb.Person":
                    persons.append(trx)
            if trx_type == "all":
                return trxs
            elif trx_type == "note":
                return notes
            elif trx_type == "dlike":
                return dlikes
            elif trx_type == "person":
                return persons

    def get_block(self, group_id: str, block_id: str):
        """Get block info.

        block_id: BlockId.

        Return value such as:
        {
            "BlockId": "aa75447f-b621-4424-a723-9d4bf1d9fff9",
            "GroupId": "a4b634c2-ceb7-4e60-9584-a221aa7b6855",
            "PrevBlockId": "78bffd23-2dba-408b-b88e-ed3f5f005411",
            "PreviousHash": "ZXh7C2Fnp4J8ny96Udo2Nr3Z50zu+KdA4BcEiw7cF4s=",
            "Trxs": [
                {
                    "TrxId": "820d6b65-99b8-4b96-afb1-0b639a76e1f3",
                    "GroupId": "a4b634c2-ceb7-4e60-9584-a221aa7b6855",
                    "Data": "CiR0eXBlLmdvb2dsZWFwaXMuY29tL...",
                    "TimeStamp": 1631817240704625000,
                    "Version": "ver 0.01",
                    "Expired": 1631817540704625200,
                    "SenderPubkey": "CAISIQJHvBByFpoeT6SBvE+w3FTs5zRTq19hi7GP0fTVkj00hw==",
                    "SenderSign": "MEUCIBwTg4UzSub5IUl4NVEZ..."
                }
            ],
            "ProducerPubKey": "CAISIQJHvBByFpoeT6SBvE+w3FTs5zRTq19hi7GP0fTVkj00hw==",
            "Hash": "RnChfYe3rBsO5swKoSDV5K8spV+NL5kaJ3aH1w/73lU=",
            "Signature": "MEYCIQC9Rnj381tjLmo8XwW0kpOCQb5o62QN78L4...",
            "Timestamp": 1631817245705639200
        }

        Return {'error': '...'}, group or block_id not exist
        """
        return self._get(f"{self.BASEURL}/block/{group_id}/{block_id}")

    def get_trx(self, group_id: str, trx_id: str):
        """Get trx info.

        trx_id: TrxId.

        Return value such as:
        {
            "TrxId": "c63d7c8e-d56d-432c-aae3-7d0d9dc34c31",
            "GroupId": "3bb7a3be-d145-44af-94cf-e64b992ff8f0",
            "Data": "rx5hmlGgIgnQSm5tT75KY96UaIauDAL...",
            "TimeStamp": "1639570707554262200",
            "Version": "1.0.0",
            "Expired": 1639571007554262200,
            "SenderPubkey": "CAISIQKwLxW1uBoZHMbss9QTdVLb8lfBhvMQ3ucnm9afGnVmpQ==",
            "SenderSign": "MEQCIGKc0MyiusNFWZEc+ZMXzk..."
        }

        Return {'error': '...'}, group or trx_id not exist
        """
        return self._get(f"{self.BASEURL}/trx/{group_id}/{trx_id}")

    def post_content(self, data: dict) -> dict[str, str]:
        """Post content to group.

        data: such as:
        {
            "type": "Add",
            "object": {
                "id": "578e65d0-9b61-4937-8e7c-f00e2b262753",
                "type": "Note",
                "content": "Good Morning!\nHave a nice day.",
                "name": "",
                "image": [
                    {
                        "mediaType": "image/png",
                        "content": "this is pic content by base64.b64encode(pic-content-bytes).decode(\"utf-8\")",
                        "name": "pic-name init by uuid like f\"{uuid.uuid4()}-{datetime.now().isoformat()}\""
                    }
                ],
                "inreplyto": {"trxid": "08c6ee4d-0310-47cf-988e-3879321ef274"}
            },
            "target": {
                "id": "d87b93a3-a537-473c-8445-609157f8dab0",
                "type": "Group"
            }
        }

        - "type": "Add", "Like" or "Dislike", if "type" is "Add", "object" has no "id" ,otherwise "object" has only "id"
        - "object.id" is trx_id, Like or Dislike on the specified Trx
        - "target.id" is group_id
        - BBS use "object.name" as title which should not be ""
        - When "object.content" is not null, "object.image" is optional
        - When "object.image" is not null, "object.content" is optional. 1~4 images, total size less than 200 mb
        - If "object.inreplyto" exists, the content will reply to the specified Trx

        Return trx_id such as {'trx_id': 'cedd7583-698b-4e6c-9a1d-3807b61947a7'}
        """
        return self._post(f"{self.BASEURL}/group/content", json=data)

    def create_group(self,
                     data: dict[str, str],
                     save: bool = False,
                     seeds_path: str = '') -> dict:
        """Owner node create a group.

        data: such as:
        {
            "group_name": "my_test_group",
            "consensus_type": "poa",
            "encryption_type": "public",
            "app_key": "group_timeline"
        }

        - "group_name": Group name
        - "consensus_type": Group consensus type, must be "poa", requested. "poa" or "pos" or "pow", "poa" only for now
        - "encryption_type": Group encryption type, must be "public", requested. encryption type of group, "public" or "private"
        - "app_key": Currently only "group_timeline"(Weibo), "group_post"(BBS) and "group_note"(Note)

        save: If save is True, seeds_path must not be ''
        seeds_path: The absolute path of the rum-app seeds folder

        Return value is a seed.
        """
        seed = self._post(f"{self.BASEURL}/group", json=data)
        if save:
            with open(seeds_path + seed["group_id"] + ".json",
                      'w',
                      encoding="utf-8") as f:
                json.dump(seed, f)
        return seed

    def join_group(self, seed: dict[str, str]) -> dict[str, str]:
        """User node join a group.

        seed is just like:
        {
            "genesis_block": {
                "BlockId": "7c32c425-a41b-4a0b-96ba-48e2e8816375",
                "GroupId": "3bb7a3be-d145-44af-94cf-e64b992ff8f0",
                "ProducerPubKey": "CAISIQKm+gTifqG6ga1FUb9NzXDetFIi9AosQSx/RBFH3RbGFQ==",
                "Hash": "+y7oVa69YPEOZcbZuUUOLt/i+vv5yychSHz4Xy7T7z8=",
                "Signature": "MEYCIQDlshiApdymHMDK65Qv9VqGevyspb3WW9cLcbHF0r7QagIhAM...",
                "TimeStamp": "1634699220007617449"
            },
            "group_id": "3bb7a3be-d145-44af-94cf-e64b992ff8f0",
            "group_name": "去中心微博",
            "owner_pubkey": "CAISIQKm+gTifqG6ga1FUb9NzXDetFIi9AosQSx/RBFH3RbGFQ==",
            "owner_encryptpubkey": "age1njthmyqheex4gmnl473et8lskj45ydnvt4qz73ngm9m9m42sk4fqrzdcja",
            "consensus_type": "poa",
            "encryption_type": "public",
            "cipher_key": "9d9e13ce3b77f6ae1da4e5ef15d94ff22e77e509dc4e3bdd70fa7435f3a9992b",
            "app_key": "group_timeline",
            "signature": "3045022100cb18857635cadb520a88d6f7a6e4f2713352..."
        }

        Return value such as:
        {
            "group_id": "ac0eea7c-2f3c-4c67-80b3-136e46b924a8",
            "group_name": "my_test_group",
            "owner_pubkey": "CAISIQOeAkTcYYWVTSH80dl2edMA4kI27g9/C6WAnTR01Ae+Pw==",
            "user_pubkey": "CAISIQO7ury6x7aWpwUVn6mj2dZFqme3BAY5xDkYjqW/EbFFcA==",
            "user_encryptpubkey": "age1774tul0j5wy5y39saeg6enyst4gru2dwp7sjwgd4w9ahl6fkusxq3f8dcm",
            "consensus_type": "poa",
            "encryption_type": "public",
            "cipher_key": "076a3cee50f3951744fbe6d973a853171139689fb48554b89f7765c0c6cbf15a",
            "signature": "3045022100a819a627237e0bb0de1e69e3b29119efbf8677..."
        }

        Return {'error': 'Group with same GroupId existed'}, already joined
        """
        return self._post(f"{self.BASEURL}/group/join", json=seed)

    def leave_group(self, group_id: dict[str, str]) -> dict[str, str]:
        """User node leave a group.

        group_id is just like:
        {
            "group_id": "846011a8-1c58-4a35-b70f-83195c3bc2e8"
        }

        Return value such as:
        {
            "group_id": "846011a8-1c58-4a35-b70f-83195c3bc2e8",
            "signature": "304402201818acb8f1358b65aecd0343a48f0fe79c89c3..."
        }
        "signature": Signature by group owner

        Return {'error': 'Group c79749ff-2a8c... not exist'}, group not exist
        """
        return self._post(f"{self.BASEURL}/group/leave", json=group_id)

    def sync(self, group_id: str) -> dict[str, str]:
        """Start sync for a group.

        Return {"GroupId":<GROUP_ID>,"Error":""}, start sync, 
        return {"error":"GROUP_ALREADY_IN_SYNCING"}, syncing.
        """
        return self._post(f"{self.BASEURL}/group/{group_id}/startsync")

    def update_user_profile(self, data: dict):
        """Update user profile of a group.

        data is just like:
        {
            "type": "Update",
            "person": {
                "name": "nickname",
                "image": {
                    "mediaType": "image/png",
                    "content": "There will be base64 string content of images"
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

        "Person" must have "name" or "image" fields.

        Return value such as {'trx_id': '3cfc8ea9-1720-4ae5-aea4-7df613174bf8'}
        """
        return self._post(f"{self.BASEURL}/group/profile", json=data)