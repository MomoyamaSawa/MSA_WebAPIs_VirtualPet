from common.singleton import singleton
import json,sys

@singleton
class GlobalConfig:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

# 这个配置的初始化要在很多操作之前，比如数据库的初始化就要用到全局配置，所以像这样配置饿汉模式
if not hasattr(sys, 'isInitializedGlobalConfig'):
    # 在第一次导入时执行的代码
    with open("config.json") as file:
        file_content = file.read()
        configData = json.loads(file_content)
        config = GlobalConfig(**configData)
    sys.isInitializedGlobalConfig = True
