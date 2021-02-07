from sagiri_core.core import SagiriGraiaPlatformCore
from graia.application import GraiaMiraiApplication

# 插件信息
__name__ = "请填写插件的名字"
__description__ = "请填写插件的功能描述"
__author__ = "请填写插件的作者"
__usage__ = "请填写插件的使用方法"


platform = SagiriGraiaPlatformCore.get_platform_instance()
loop = platform.get_loop()
bcc = platform.get_bcc()
app: GraiaMiraiApplication = platform.get_app()
