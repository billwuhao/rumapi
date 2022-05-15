import requests


def paidgroup_dapp():
    """获取支持付费 dapp 的信息

    返回值字段:
    {'data': {'name': 'Paid Group',
        'version': '0.0.1',
        'developer': 'Quorum Team',
        'owner': '0x3a0075D4C979839E31D1AbccAcDF3FcAe981fe33',
        'invokeFee': '5.0000',
        'asset': {'index': 20,
            'id': '965e5c6e-434c-3fa9-b780-c50f43cd955c',
            'name': 'Chui Niu Bi',
            'icon': 'https://mixin-images.zeromesh.net/0sQY63dDM...',
            'rumAddress': '0x2A4cb8346e7abb258a91763E8eB762385d105ea0',
            'symbol': 'CNB',
            'symbolDisplay': 'CNB',
            'rumSymbol': 'RCNB'},
        'shareRatio': '80'},
    'error': None,
    'success': True
    }
    """
    resp = requests.get("https://prs-bp2.press.one/api/dapps/PaidGroupMvm")
    return resp.json()


def paidgroup_info(group_id):
    """获取付费组详情

    Args:
        group_id (str): 组 ID

    返回值字段:
    {'data': {'dapp': {...},
        'group': {'mixinReceiver': '0x00014e6ffccaceab44219fee7f2edcc81c440001',
            'price': '1.0000',
            'asset': {'index': 20,
                'id': '965e5c6e-434c-3fa9-b780-c50f43cd955c',
                'name': 'Chui Niu Bi',
                'icon': 'https://mixin-images.zeromesh.net/0sQY63dDM...',
                'rumAddress': '0x2A4cb8346e7abb258a91763E8eB762385d105ea0',
                'symbol': 'CNB',
                'symbolDisplay': 'CNB',
                'rumSymbol': 'RCNB'},
            'duration': 99999999}
        },
    'error': None,
    'success': True
    }
    """
    resp = requests.get(f"https://prs-bp2.press.one/api/mvm/paidgroup/{group_id}")
    return resp.json()


def check_payment(group_id, eth_addr):
    """检查用户付款情况

    Args:
        group_id (str): 组 ID
        eth_addr (str): eth 地址

    返回值字段:
    {'data': {...
        'payment': {'groupId': 'a8f5fe8c-a8a0-4520-bbf2-d69c70604b82',
            'price': '7.0000',
            'asset': {'index': 20,
                'id': '965e5c6e-434c-3fa9-b780-c50f43cd955c',
                'name': 'Chui Niu Bi',
                'icon': 'https://mixin-images.zeromesh.net/0s...',
                'rumAddress': '0x2A4cb8346e7abb258a91763E8eB762385d105ea0',
                'symbol': 'CNB',
                'symbolDisplay': 'CNB',
                'rumSymbol': 'RCNB'},
            'expiredAt': 1749335523}
        },
    'error': None,
    'success': True
    }
    """
    resp = requests.get(
        f"https://prs-bp2.press.one/api/mvm/paidgroup/{group_id}/{eth_addr}"
    )
    return resp.json()


def announce_paidgroup(group_id, eth_addr, amount, duration):
    """设置付费组, 发起申请扫码付费后设置完成

    Args:
        group_id (str): 组 ID
        eth_addr (str): eth 地址
        amount (int): 设置用户进组需要支付金额
        duration (int): 持续时间(秒)

    返回值字段:
    {'data': {'qrcode': <二维码>
        'url': 'mixin://codes/e9a20098-76bb-4c34-ae54-caf0fbee7839'},
    'error': None,
    'success': True}
    """
    data = {
        "group": group_id,
        "owner": eth_addr,
        "amount": str(amount),
        "duration": duration,
    }
    resp = requests.post(
        f"https://prs-bp2.press.one/api/mvm/paidgroup/announce", json=data
    )
    return resp.json()


def pay_paidgroup(group_id, eth_addr):
    """用户发起付款, 扫码成功付款后可查到付款情况

    Args:
        group_id (str): 组 ID
        eth_addr (str): eth 地址

    付费组在 RUM 是如何实现？用户加入 group, 利用该 api 发起付费，
    将用户 eth 地址附在 memo, 在 RUM 发起 announce, owner 查询付费情况授权

    返回值字段:
    {'data': {'qrcode': <二维码>
        'url': 'mixin://codes/e9a20098-76bb-4c34-ae54-caf0fbee7839'},
    'error': None,
    'success': True}
    """
    data = {"user": eth_addr, "group": group_id}
    resp = requests.post(f"https://prs-bp2.press.one/api/mvm/paidgroup/pay", json=data)
    return resp.json()
