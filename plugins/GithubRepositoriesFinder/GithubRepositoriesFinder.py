import aiohttp

from graia.application import GraiaMiraiApplication
from graia.application.message.chain import MessageChain
from graia.application.message.elements.internal import Plain, At
from graia.application.event.messages import Group
from graia.application.event.messages import Member

from sagiri_core.core import SagiriGraiaPlatformCore


# 插件信息
__name__ = "GithubRepositoriesFinder"
__description__ = "根据地址寻找仓库并返回详细信息"
__author__ = "umauc"
__usage__ = "在群中发送github 用户名/仓库名 获取信息"


platform = SagiriGraiaPlatformCore.get_platform_instance()
loop = platform.get_loop()
bcc = platform.get_bcc()
app: GraiaMiraiApplication = platform.get_app()


@bcc.receiver("GroupMessage")
async def githubot(app: GraiaMiraiApplication, member: Member, messageChain: MessageChain, group: Group):
    """
    使用方法：发送github 用户名/仓库名 获取信息
    插件来源：https://github.com/umauc/githubot
    """
    if messageChain.asDisplay().startswith("github "):
        keyword = messageChain.asDisplay()[7:]
        try:
            url = f'https://api.github.com/search/repositories?q={keyword}'
            headers = {
                'accept': 'application/vnd.github.v3+json'
            }
            async with aiohttp.ClientSession() as session:
                async with session.get(url=url, headers=headers) as resp:
                    search = await resp.json()
            if search.get('total_count') != 0:
                repo_data = search.get('items')[0]
                full_name = repo_data.get('full_name')
                owner = repo_data.get('owner').get('login')
                description = repo_data.get('description')
                watch = repo_data.get('watchers')
                star = repo_data.get('stargazers_count')
                fork = repo_data.get('forks_count')
                language = repo_data.get('language')
                open_issues = repo_data.get('open_issues')
                try:
                    license = repo_data.get('license').get('spdx_id')
                except Exception:
                    license = 'None'
                last_pushed = repo_data.get('pushed_at')
                jump = repo_data.get('html_url')
                mc = MessageChain.create([
                    At(target=member.id),
                    Plain(text=f'\n{full_name}:\nOwner:{owner}\nDescription:{description}\nWatch/Star/Fork:{watch}/{star}/{fork}\nLanguage:{language}\nLicense:{license}\nLast pushed:{last_pushed}\nJump:{jump}')
                ]).asSendable()
                await app.sendGroupMessage(group, mc)
        except Exception:
            await app.sendGroupMessage(
                group,
                MessageChain.create([
                    At(target=member.id),
                    Plain(text='无此存储库')
                ])
            )