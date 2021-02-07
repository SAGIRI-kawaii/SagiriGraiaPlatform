from sagiri_core.core import SagiriGraiaPlatformCore
from graia.application import GraiaMiraiApplication
from graia.application.message.elements.internal import MessageChain
from graia.application.group import *
from graia.application.friend import *
from graia.application.event.messages import GroupMessage
from graia.application.event.messages import FriendMessage
from graia.application.event.messages import TempMessage

# 插件信息
__name__ = "MessagePrinter"
__description__ = "打印收到的消息"
__author__ = "SAGIRI-kawaii"
__usage__ = ""


platform = SagiriGraiaPlatformCore.get_platform_instance()
bcc = platform.get_bcc()
app: GraiaMiraiApplication = platform.get_app()


@bcc.receiver(GroupMessage)
async def group_message_listener(
    message: MessageChain,
    sender: Member,
    group: Group
):
    print(f"接收到来自群组 <{group.name} ({group.id})> 中成员 <{sender.name} ({sender.id})> 的消息：{message.asDisplay()}")


@bcc.receiver(FriendMessage)
async def friend_message_listener(
    message: MessageChain,
    sender: Friend
):
    print(f"接收到来自好友 <{sender.nickname} ({sender.id})> 的消息：{message.asDisplay()}")


@bcc.receiver(TempMessage)
async def temp_message_listener(
    message: MessageChain,
    sender: Member
):
    print(f"接收到来自 <{sender.name} ({sender.id})> 的临时消息：{message.asDisplay()}")
