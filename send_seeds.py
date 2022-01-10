import json

from api import Api
from config import *

api = Api(PORT, HOST, CACERT)

def _get_groubs_info() -> list[str]:
    """Get groups information.
    
    Save each group seed and its information as a list. 
    Sort by number of users, or mark synchronization status
    """
    data = []
    for g in api.get_groups()["groups"]:
        person_info = api.get_group_content(g["group_id"],"all")
        num = len(set(i["Publisher"] for i in person_info))
        if num != 0:
            status = f'{num}人'
        else:
            status = '正在同步中...'
        with open(f'{rumapp_seeds_folder}/{g["group_id"]}.json', encoding='utf-8') as f:
            seed = json.load(f)
            data.append((seed, num, status))
    return [f'- {str(i[0])} {i[2]}' for i in sorted(data,key=lambda x:x[1],reverse=True)]


def send_seeds(groub_id:str):
    """Send seed to specified group."""
    data = {
            "type": "Add",
            "object": {
                "type": "Note",
                "content": "\n\n".join(_get_groubs_info()).replace("'",'"'),
                "name": "种子大全：按活跃人数排行"
            },
            "target": {
                "id": groub_id,
                "type": "Group"
            }
        }
    api.post_content(data)


if __name__ == "__main__":
    send_seeds("54978593-a913-4ad4-aa57-5f85067e1e8b")