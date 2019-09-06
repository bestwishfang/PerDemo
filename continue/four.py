from abc import ABCMeta, abstractmethod


# 抽象类
class BasePlay(metaclass=ABCMeta):
    
    # 抽象方法
    @abstractmethod
    def play(self):
        pass



class BaseMessage(object):


    def send(self):
        raise NotImplementedError("send() must be overridden.")
