# SagiriGraiaPlatform
一个支持插件加载的基于Graia的MiraiBot框架(是套壳

## 开始使用
- 执行 `pip install -r requirements.txt` 安装所需依赖
- 将 `configdemo.json` 改名为 `config.json`，并填入bot的qq号，可根据自身状况对 `authKey` 和 `miraiHost` 进行修改
- 将插件文件夹放入plugins文件夹（注意插件文件夹应与插件同名，如文件夹名为test，test文件夹内插件主程序名为test.py）

## 关于插件
你可以通过以下方法来获取GraiaMiraiApplication的实例、bcc以及loop:
```python
from sagiri_core.core import SagiriGraiaPlatformCore
from graia.application import GraiaMiraiApplication


platform = SagiriGraiaPlatformCore.get_platform_instance()
loop = platform.get_loop()
bcc = platform.get_bcc()
app: GraiaMiraiApplication = platform.get_app()
```
示例插件 `MessagePrinter` 可在 `plugins/MessagePrinter` 目录下查看

之后会移植更多插件

## 其他
在 `utils.py` 中提供了将 `MessageChain` 类转换为图片的函数 `messagechain_to_img`，具体使用请看注释