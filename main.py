from sagiri_core.core import SagiriGraiaPlatformCore
import utils

config = utils.load_config()
platform = SagiriGraiaPlatformCore(config=config)
platform.plugins_load()

app = platform.get_app()

for plugin in platform.get_plugins():
    print(plugin)

platform.launch()
