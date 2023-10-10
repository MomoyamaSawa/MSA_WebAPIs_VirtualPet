from common.singleton import singleton

@singleton
class GlobalConfig:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
