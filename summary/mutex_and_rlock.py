# import threading
#
#
# class MyThread(threading.Thread):
#
#     def run(self):
#         global n1, n2
#         lock.acquire()  # 加锁
#         n1 += 1
#         print(self.name + ' set n1 to ' + str(n1))
#         lock.acquire()  # 再次加锁
#         n2 += n1
#         print(self.name + ' set n2 to ' + str(n2))
#         lock.release()
#         lock.release()
#
#
# n1, n2 = 0, 0
# lock = threading.Lock()
#
# if __name__ == '__main__':
#     thread_list = []
#     for i in range(5):
#         t = MyThread()
#         t.start()
#         thread_list.append(t)
#     for t in thread_list:
#         t.join()
#     print('final num:%d ,%d' % (n1, n2))


import threading


class MyThread(threading.Thread):

    def run(self):
        global n1, n2
        lock.acquire()  # 加锁
        n1 += 1
        print(self.name + ' set n1 to ' + str(n1))
        lock.acquire()  # 再次加锁
        n2 += n1
        print(self.name + ' set n2 to ' + str(n2))
        lock.release()
        lock.release()


n1, n2 = 0, 0
lock = threading.RLock()

if __name__ == '__main__':
    thread_list = []
    for i in range(5):
        t = MyThread()
        t.start()
        thread_list.append(t)
    for t in thread_list:
        t.join()
    print('final num:%d ,%d' % (n1, n2))
