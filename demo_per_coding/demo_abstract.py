from abc import ABCMeta, abstractmethod


# 抽象类
class BasePlay(metaclass=ABCMeta):

    # 抽象方法
    @abstractmethod
    def play(self):
        pass


# 要求继承类必须覆写 特定方法，否则调用抛异常
class BaseMessage(object):

    def send(self):
        raise NotImplementedError("send() must be overridden.")
