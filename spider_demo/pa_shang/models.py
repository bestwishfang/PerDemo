# 主要负责数据模型的管理


class News(object):
    # 初始化方法定义属性
    def __init__(self, title, url, release_time):
        self.title = title
        self.url = url
        self.release_time = release_time
        
        # 每个数据对象签名
        self.sign = None

