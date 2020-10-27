# -*- coding: utf-8 -*-
import threading
from queue import Queue

# def syschronized(func):
#     func.__lock__ == threading.Lock()
#
#     def lock_func(*args, **kwargs):
#         with func.__lock__:
#             return func(*args, **kwargs)
#
#     return lock_func


class Singleton:
    __instance = None
    __lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if cls.__lock.acquire():
            if not cls.__instance:
                cls.__instance = super(Singleton, cls).__new__(cls, *args, **kwargs)
                # cls.__instance = object.__new__(cls, *args, **kwargs)
            cls.__lock.release()
            return cls.__instance


def create_single(q):
    while not q.empty():
        num = q.get()
        single = Singleton()
        print('{}:'.format(num), id(single), type(single), '\n')


if __name__ == '__main__':
    q = Queue()
    for i in range(1, 100):
        q.put(i)

    threading_list = []
    for j in range(4):
        t = threading.Thread(target=create_single, args=(q, ))
        threading_list.append(t)
        t.start()

    for t in threading_list:
        t.join()

    print('*'*100)

    two = Singleton()
    print('two:', id(two), type(two))

    three = object.__new__(Singleton)
    print('three:', id(three), type(three))
