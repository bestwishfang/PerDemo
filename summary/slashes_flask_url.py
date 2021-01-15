from flask import Flask

app = Flask(__name__)


# @app.route('/dest/', strict_slashes=True)
# def dest_page_with_slash():
#     print('dest_page_with_slash')
#     return '/dest/'


@app.route('/dest', strict_slashes=True)
def dest_page_no_slash():
    print('dest_page_no_slash')
    return '/dest'


if __name__ == '__main__':
    app.run()

"""
https://blog.csdn.net/weixin_30319097/article/details/95580023

strict_slashes=None # 对URL最后的 / 符号是否严格要求
例如：
@app.route('/index',strict_slashes=False) #访问 http://www.xx.com/index/ 或 http://www.xx.com/index均可
@app.route('/index',strict_slashes=True) #仅访问 http://www.xx.com/index 
"""
