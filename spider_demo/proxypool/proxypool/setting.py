# Redis数据库地址
REDIS_HOST = '127.0.0.1'

# Redis数据库端口
REDIS_PORT = 6379

# Redis数据库密码，如无填None
REDIS_PASSWORD = None

REDIS_KEY = 'proxies'

# 代理分数
MAX_SCORE = 100
MIN_SCORE = 0
INITIAL_SCORE = 10

# 代理池数量界限
# POOL_UPPER_THRESHOLD = 10000
POOL_UPPER_THRESHOLD = 1000

# 有效状态码
VALID_STATUS_CODES = [200, 302]

# 测试API,建议抓哪个网站测试哪个
TEST_URL = 'https://movie.douban.com/top250?start='

# 最大批测试量
# BATCH_TEST_SIZE = 100
BATCH_TEST_SIZE = 10

# 开关
TESTER_ENABLED = True
GETTER_ENABLED = True
API_ENABLED = True

# 测试代理周期
TESTER_CYCLE = 20

# 获取代理周期
GETTER_CYCLE = 300

# API设置
API_HOST = '127.0.0.1'
API_PORT = 5555
