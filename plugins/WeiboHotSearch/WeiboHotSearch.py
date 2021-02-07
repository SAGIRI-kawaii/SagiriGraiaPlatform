import aiohttp
import random

from graia.application.message.elements.internal import MessageChain
from graia.application.message.elements.internal import Plain
from graia.application.event.messages import GroupMessage

from utils import messagechain_to_img
from sagiri_core.core import SagiriGraiaPlatformCore
from graia.application import GraiaMiraiApplication
from graia.application.message.parser.kanata import Kanata
from graia.application.message.parser.signature import FullMatch
from graia.application.group import Group


# 插件信息
__name__ = "WeiboHotSearch"
__description__ = "获取当前微博热搜"
__author__ = "SAGIRI-kawaii"
__usage__ = "在群内发送 微博 即可"


platform = SagiriGraiaPlatformCore.get_platform_instance()
bcc = platform.get_bcc()
app: GraiaMiraiApplication = platform.get_app()


@bcc.receiver(GroupMessage, dispatchers=[Kanata([FullMatch('微博')])])
async def group_message_listener(app: GraiaMiraiApplication, group: Group):
    await app.sendGroupMessage(
        group,
        await get_weibo_hot()
    )


async def get_weibo_hot(display: str = "img") -> MessageChain:
    url = "http://api.weibo.cn/2/guest/search/hot/word"
    async with aiohttp.ClientSession() as session:
        async with session.get(url=url) as resp:
            data = await resp.json()
    data = data["data"]
    text_list = [f"随机数:{random.randint(0,10000)}", "\n微博实时热榜:"]
    index = 0
    for i in data:
        index += 1
        text_list.append("\n%d. %s" % (index, i["word"].strip()))
    text = "".join(text_list).replace("#", "")
    msg = MessageChain.create([
        Plain(text=text)
    ])
    if display == "img":
        return await messagechain_to_img(msg)
    elif display == "text":
        return msg
    else:
        raise ValueError("Invalid display value!")
