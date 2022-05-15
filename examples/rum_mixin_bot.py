import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from rum import Rum

sys.path.append(os.path.join(os.path.dirname(__file__), "mixin-sdk-python"))
from mixinsdk.clients.user_config import AppConfig
from mixinsdk.clients.blaze_client import BlazeClient
from mixinsdk.clients.http_client import HttpClient_AppAuth
from mixinsdk.types.message import MessageView, pack_text_data, pack_message


rum = Rum(
    # host, port, crtfile, jwt_token=None
    "127.0.0.1",
    "6666",
    r"D:\rum\server.crt",
    # "eyJhbGxxxxxxx....",
)
group_id = "d34f000b-2463-4db4-8c38-96965ef804c5"
eth_addrs_file = os.path.join(os.path.dirname(__file__), "eth_addrs.txt")
pubkeys = {}
with open(eth_addrs_file, encoding="utf-8") as f:
    eth_addrs = set(f.read().split(","))


def _is_ethaddr(input):
    """判断是否是合法 eth 地址

    Args:
        input (str): 用户输入
    """
    if len(input) != 42 or not input.startswith("0x"):
        return False
    try:
        int(input, 16)
    except:
        return False
    return True


def _is_pubkey(input):
    """判断是否是合法 pubkey

    Args:
        input (str): 用户输入
    """
    if input.startswith("CAISIQ") and input.endswith("==") and len(input) == 52:
        return True
    else:
        return False


def update_user_permissions(pubkey, eth_addr):
    """检查付费, 并更新 rum 已付费用户权限"""
    if rum.check_payment(group_id, eth_addr)["data"]["payment"]:
        trx_tpye = [
            "req_block_forward",
            "req_block_backward",
            "block_synced",
            "block_produced",
            "ask_peerid",
        ]
        rum.chainconfig(group_id, "upd_alw_list", trx_tpye, pubkey=pubkey)


class MixinBotClient:
    def __init__(self):
        self.blaze: BlazeClient = None
        self.http: HttpClient_AppAuth = None


def message_handle_error_callback(error, details):
    print("error_callback --- ")
    print(f"error: {error}")
    print(f"details: {details}")


async def message_handle(message):
    global bot
    action = message["action"]

    if action == "ACKNOWLEDGE_MESSAGE_RECEIPT":
        # mixin blaze server received the message
        return

    if action == "LIST_PENDING_MESSAGES":
        print("Mixin blaze server: 👂")
        return

    if action == "ERROR":
        print(message["error"])
        return
        """example message={
            "id": "00000000-0000-0000-0000-000000000000",
            "action": "ERROR",
            "error": {
                "status": 202,
                "code": 400,
                "description": "The request body can't be parsed as valid data.",
            },
        }"""

    if action == "CREATE_MESSAGE":
        error = message.get("error")
        if error:
            print(error)
            return

        data = message["data"]
        msgview = MessageView.from_dict(data)

        if msgview.conversation_id == "":
            # is response status of send message, ignore
            return

        if msgview.type == "message":
            id = msgview.user_id
            print(f"message from: {id}")

            msg = msgview.data_decoded
            if _is_ethaddr(msg):
                eth_addrs.add(msg)
                with open(eth_addrs_file, "w", encoding="utf-8") as f:
                    f.write(",".join(eth_addrs))
                if rum.check_payment(group_id, msg)["data"]["payment"]:
                    reply = "您已付款，请用 Rum API 发起 Announce"
                else:
                    pay_url = rum.pay_paidgroup(group_id, msg)["data"]["url"]
                    reply = f"点击下方链接付款\n{pay_url} \n稍等片刻，再次回复 ETH 地址，可查询是否付款成功"

            elif _is_pubkey(msg):
                user = rum.announced_user(group_id, msg)
                if "error" in user:
                    reply = "未正确发起 Announce"
                elif (
                    user["Result"] == "ANNOUNCED"
                    and user["Memo"] in eth_addrs
                    and user["AnnouncedSignPubkey"] == msg
                ):
                    update_user_permissions(msg, user["Memo"])
                    reply = "👏恭喜获得授权，在 Rum-app 刷新同步完成即可，想要获得 “可写权限”，请回复 “申请可写权限”"
                    pubkeys[id] = msg

            elif msg == "申请可写权限" and id in pubkeys:
                trx_tpye = [
                    "post",
                    "req_block_forward",
                    "req_block_backward",
                    "block_synced",
                    "block_produced",
                    "ask_peerid",
                ]
                rum.chainconfig(group_id, "upd_alw_list", trx_tpye, pubkey=pubkeys[id])
                pubkeys.pop(id)
                reply = "您已获得可写权限"

            else:
                reply = (
                    "请按下面操作获得授权：\n"
                    "1，打开 Rum-app，在 “种子大全” 组内搜索 “高清无码”，找到种子"
                    '（认准 "GroupId": "d34f000b-2463-4db4-8c38-96965ef804c5")\n'
                    "2，加入，在种子网络详情页复制 ETH 地址发给本机器人\n"
                    "3，收到付款链接，点击链接支付\n"
                    "4，付款成功后，通过 Rum API 发起 Announce（user 类型，特别注意：memo 备注 ETH 地址）\n"
                    "5，种子网络详情页复制用户 ID（pubkey）发给本机器人\n"
                    "依次完成上述操作，即可获得 “高清无码” 种子网络内容权限\n"
                    "Rum API: https://rumsystem.github.io/quorum-api"
                    "/#/User/post_api_v1_group_announce"
                )

            await bot.blaze.send_message(
                pack_message(
                    pack_text_data(reply),
                    msgview.conversation_id,
                ),
            )
            await bot.blaze.echo(msgview.message_id)
            return


bot_config = AppConfig.from_payload(
    payload={
        "pin": "xxx",
        "client_id": "xxx",
        "session_id": "xxx",
        "pin_token": "xxx",
        "private_key": "xxx",
    }
)
bot = MixinBotClient()
bot.http = HttpClient_AppAuth(bot_config)
bot.blaze = BlazeClient(
    bot_config,
    on_message=message_handle,
    on_message_error_callback=message_handle_error_callback,
)


bot.blaze.run_forever(2)
