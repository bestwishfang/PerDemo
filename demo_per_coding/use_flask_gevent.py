# -*- coding: utf-8 -*-
import time
from gevent import monkey

monkey.patch_all()

from flask import Flask

app = Flask(__name__)


@app.route('/')
def index():
    return "Hello Flask"


@app.route('/asyn', methods=['GET'])
def asyn_one():
    print("asyn has a request!")
    time.sleep(10)
    return 'hello asyn'


if __name__ == '__main__':
    # app.run(host='0.0.0.0', port=80, debug=True)

    from gevent import pywsgi
    from werkzeug.debug import DebuggedApplication

    dapp = DebuggedApplication(app, evalex=True)
    ip_port = ('127.0.0.1', 5000)
    server = pywsgi.WSGIServer(ip_port, dapp)
    print("Server Running ...")
    server.serve_forever()
    
