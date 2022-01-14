import string
import random

from api import Api
from config import *

api = Api(PORT, HOST, CACERT)


def auto_sync():
    """Automatically refresh all groups."""
    for g in api.get_groups()["groups"]:
        api.sync(g["group_id"])


def auto_user_config():
    """Automatically generate random names and avatars"""
    for i in api.get_groups()['groups']:
        name = ''.join(random.sample(string.ascii_letters, 5))
        data = {
            "type": "Update",
            "person": {
                "name": name
            },
            "target": {
                "id": i['group_id'],
                "type": "Group"
            }
        }
        api.update_user_profile(data)


if __name__ == "__main__":
    auto_sync()
    auto_user_config()