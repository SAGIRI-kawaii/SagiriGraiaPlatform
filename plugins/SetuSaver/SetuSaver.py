import aiohttp
from PIL import Image as IMG
from io import BytesIO
import os

from graia.application.message.elements.internal import MessageChain
from graia.application.message.elements.internal import Plain
from graia.application.message.elements.internal import Image
from graia.application.event.messages import GroupMessage
from graia.application import GraiaMiraiApplication
from graia.application.group import Group
from graia.application.message.parser.kanata import Kanata
from graia.application.message.parser.signature import RegexMatch

from sagiri_core.core import SagiriGraiaPlatformCore


platform = SagiriGraiaPlatformCore.get_platform_instance()
loop = platform.get_loop()
bcc = platform.get_bcc()
app: GraiaMiraiApplication = platform.get_app()

BASE_PATH = "./plugins/SetuSaver/SetuLib/"


@bcc.receiver(GroupMessage)
async def setu_saver(message: MessageChain, group: Group):
    """
    使用方法：
        添加图片：在群中发送 /添加涩图 pid即可
        删除图片：在群中发送 /删除涩图 pid即可
    插件来源：SAGIRI-kawaii
    """
    message_text = message.asDisplay()
    if message_text.startswith("/添加涩图 "):
        img_id = message_text[6:]
        if os.path.exists(BASE_PATH + f"{img_id}.jpg"):
            await app.sendGroupMessage(
                group,
                MessageChain.create([
                    Plain(text=f"图片 {img_id} 已存在于SetuLib中！")
                ])
            )
            return
        if img_id.isdigit():
            await app.sendGroupMessage(
                group,
                MessageChain.create([
                    Plain(text="正在搜索...请稍后...")
                ])
            )
            path = BASE_PATH + f"{img_id}.jpg"
            success = False
            url = f"https://pixiv.cat/{img_id}.jpg"
            async with aiohttp.ClientSession() as session:
                async with session.get(url=url) as resp:
                    status_code = resp.status
                    print(status_code)
                    if status_code != 404:
                        img_content = await resp.read()
                        success = True

            if not success:
                url = f"https://pixiv.cat/{img_id}-1.jpg"
                async with aiohttp.ClientSession() as session:
                    async with session.get(url=url) as resp:
                        status_code = resp.status
                        print(status_code)
                        if status_code != 404:
                            img_content = await resp.read()
                            success = True

            if not success:
                await app.sendGroupMessage(
                    group,
                    MessageChain.create([
                        Plain(text=f"未搜索到图片 {img_id}！请检查输入是否正确！")
                    ])
                )
                return

            image = IMG.open(BytesIO(img_content))
            image = image.convert('RGB')
            image.save(path)

            await app.sendGroupMessage(
                group,
                MessageChain.create([
                    Plain(text=f"图片 {img_id} 添加成功！\n"),
                    Image.fromUnsafeBytes(img_content)
                ])
            )
        else:
            await app.sendGroupMessage(
                group,
                MessageChain.create([
                    Plain(text="非法pid！只接受全数字参数！")
                ])
            )
    elif message_text.startswith("/删除涩图 "):
        img_id = message_text[6:]
        if os.path.exists(f"{BASE_PATH}{img_id}.jpg"):
            os.remove(f"{BASE_PATH}{img_id}.jpg")
            await app.sendGroupMessage(
                group,
                MessageChain.create([
                    Plain(text=f"图片 {img_id} 已从SetuLib中删除！")
                ])
            )
        else:
            await app.sendGroupMessage(
                group,
                MessageChain.create([
                    Plain(text=f"图片 {img_id} 不存在！")
                ])
            )