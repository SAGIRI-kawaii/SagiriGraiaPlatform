import asyncio
import importlib
import importlib.util
import os
from asyncio.events import AbstractEventLoop

from graia.application import GraiaMiraiApplication
from graia.application import Session
from graia.broadcast import Broadcast

from .exceptions import *


class SagiriGraiaPlatformCore:
    __instance = None
    __first_init: bool = False
    __app: GraiaMiraiApplication = None
    __loop: AbstractEventLoop = None
    __bcc = None
    __config: dict = None
    __plugins_set: set = set()
    __plugins: list = []
    __launched: bool = False
    plugins_path: str = "./plugins/"
    plugins_folder_name: str = "plugins"
    necessary_parameters = ["miraiHost", "authKey", "BotQQ"]

    def __new__(cls, config: dict):
        if not cls.__instance:
            cls.__instance = object.__new__(cls)
        return cls.__instance

    def __init__(self, config: dict):
        if not self.__first_init:
            print("Initialize")
            if any(parameter not in config for parameter in self.necessary_parameters):
                raise ValueError(f"Missing necessary parameters! (miraiHost, authKey, BotQQ)")
            print(config)
            self.__loop = asyncio.get_event_loop()
            self.__bcc = Broadcast(loop=self.__loop)
            self.__app = GraiaMiraiApplication(
                broadcast=self.__bcc,
                connect_info=Session(
                    host=config["miraiHost"],
                    authKey=config["authKey"],
                    account=config["BotQQ"],
                    websocket=True
                )
            )
            self.__app.debug = False
            self.__config = config
            SagiriGraiaPlatformCore.__first_init = True
            print("Initialize end")
        else:
            raise SagiriGraiaPlatformCoreAlreadyInitialized()

    @classmethod
    def get_platform_instance(cls):
        if cls.__instance:
            return cls.__instance
        else:
            raise SagiriGraiaPlatformCoreNotInitialized()

    def get_bcc(self) -> Broadcast:
        if self.__bcc:
            return self.__bcc
        else:
            raise SagiriGraiaPlatformCoreNotInitialized()

    def get_loop(self) -> AbstractEventLoop:
        if self.__loop:
            return self.__loop
        else:
            raise SagiriGraiaPlatformCoreNotInitialized()

    def get_app(self) -> GraiaMiraiApplication:
        if self.__app:
            return self.__app
        else:
            raise SagiriGraiaPlatformCoreNotInitialized()

    def plugins_load(self):
        print("start load plugins\n")
        for root, dirs, files in os.walk(self.plugins_path):
            for d in dirs:
                if not os.path.exists(self.plugins_path + d):
                    # print(f"plugin {d} load failed: {d}.py not exist! Please check whether the folder name is "
                    #       f"consistent with the module name!")
                    pass
                elif d in self.__plugins_set:
                    pass
                else:
                    try:
                        print(f"loading plugin: {d}")
                        module = importlib.import_module(f"{self.plugins_folder_name}.{d}.{d}", d)
                        name = getattr(module, '__name__', None)
                        description = getattr(module, '__description__', None)
                        author = getattr(module, '__author__', None)
                        usage = getattr(module, '__usage__', None)
                        module_info = {
                            "name": name,
                            "description": description,
                            "author": author,
                            "usage": usage
                        }
                        self.__plugins.append(module_info)
                        self.__plugins_set.add(d)
                    except Exception as e:
                        print(f"\033[1;31mloading error: {e}\033[0m")
        print("\nloading plugins finished")

    def get_config(self):
        return self.__config

    def get_plugins(self):
        return self.__plugins

    def launch(self):
        if not self.__launched:
            self.__app.launch_blocking()
            self.__launched = True
        else:
            raise GraiaMiraiApplicationAlreadyLaunched()
