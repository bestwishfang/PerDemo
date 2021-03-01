# 使用第三方库来创建useragent
from fake_useragent import UserAgent


ua = UserAgent()
print(ua.chrome)
print('='*100)
for i in range(10):
    print(ua.random)