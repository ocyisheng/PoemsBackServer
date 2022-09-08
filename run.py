#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2019/12/26 1:08 AM
# @Author  : Gao
# @File    : run.py
# @Software: PyCharm

from app import app

from util.util import get_local_ip

if __name__ == '__main__':
    from werkzeug.middleware.proxy_fix import ProxyFix

    app.wsgi_app = ProxyFix(app.wsgi_app)
    # app.run(debug=True, port=5010)
    app.run(host=get_local_ip(), port=5010, debug=True, load_dotenv=False)
