import re
import json
from copy import deepcopy

from api import Api
from config import *

api = Api(PORT, HOST, CACERT)


def _search_trx_seeds(text: str) -> dict[str, list]:
    """Search seeds in a trx content.
    
    text: Trx content
    
    Return dict such as:
    {
        group_id: [seed, search_progress]
    }
    - seed: group seed
    - search_progress: ranking of the last trx searched. The initial value is 0
    """
    pattern = (r'\{[\s\S]*?'
               r'"genesis_block"[\s\S]*?'
               r'"BlockId"[\s\S]*?'
               r'"GroupId"[\s\S]*?'
               r'"ProducerPubKey"[\s\S]*?'
               r'"Hash"[\s\S]*?'
               r'"Signature"[\s\S]*?'
               r'"TimeStamp"[\s\S]*?'
               r'"group_id"[\s\S]*?'
               r'"group_name"[\s\S]*?'
               r'"owner_pubkey"[\s\S]*?'
               r'"consensus_type"[\s\S]*?'
               r'"encryption_type"[\s\S]*?'
               r'"cipher_key"[\s\S]*?'
               r'"app_key"[\s\S]*?'
               r'"signature"[\s\S]*?'
               r'\}')
    seeds = re.findall(pattern, text)
    seeds_dict = {}
    if len(seeds) != 0:
        for i in seeds:
            seed = json.loads(i)
            data = {seed["group_id"]: [seed, 0]}
            seeds_dict.update(data)
        return seeds_dict
    else:
        return {}


def search_network_seeds() -> dict[str, list]:
    """Search the whole network for open seeds.
    
    Write the searched seed to the 'search_seed_timestamp_mark.json' file.
    The return value contains all seeds.
    """
    with open(seeds_searched, encoding='utf-8') as f:
        all_seeds = json.load(f)
        for g in api.get_groups()["groups"]:
            group_id = g["group_id"]
            data = api.get_group_content(group_id)
            # Start searching from marked points and avoid starting from scratch
            if group_id in all_seeds:
                n = deepcopy(all_seeds[group_id][1])
                data = data[n:]
            else:
                with open(f'{rumapp_seeds_folder}/{group_id}.json',
                          encoding='utf-8') as f1:
                    all_seeds.update({group_id: [json.load(f1), 0]})
            for t in data:
                if "content" in t["Content"]:
                    seeds = _search_trx_seeds(t["Content"]["content"])
                    for s in seeds:
                        # Save the new seeds found
                        all_seeds.setdefault(s, seeds[s])
                # Update Search progress for the current group
                all_seeds[group_id][1] += 1
        with open(seeds_searched, 'w', encoding='utf-8') as f2:
            json.dump(all_seeds, f2, indent=2)
        return all_seeds


def join_groups(seeds: dict[str, list] = None) -> tuple[str, bool]:
    """Join new groups by seeds.
    
    Return: invalid group list
    """
    if not seeds:
        seeds = search_network_seeds()
    invalid_groups = []
    for id, s in seeds.items():
        if s[0]["app_key"] in ("group_timeline", "group_post", "group_note"):
            join = api.join_group(s[0])
            if "group_id" in join:
                with open(f'{rumapp_seeds_folder}/{id}.json',
                          'w',
                          encoding='utf-8') as f:
                    json.dump(s[0], f)
            elif join == {'error': 'Group with same GroupId existed'}:
                continue
            else:
                invalid_groups.append(s[0])
        else:
            invalid_groups.append(s[0])
    return invalid_groups


if __name__ == "__main__":
    print(join_groups())