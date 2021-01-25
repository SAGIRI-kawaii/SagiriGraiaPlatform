from sagiri_core.core import SagiriGraiaPlatformCore
from graia.application import GraiaMiraiApplication


platform = SagiriGraiaPlatformCore.get_platform_instance()
loop = platform.get_loop()
bcc = platform.get_bcc()
app: GraiaMiraiApplication = platform.get_app()
