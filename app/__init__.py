#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2019/12/18 8:28 PM
# @Author  : Gao
# @File    : __init__.py.py
# @Software: PyCharm

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from config import Config

## 扩展对象生成
# db
db = SQLAlchemy()
# 数据库迁移
migrate = Migrate()

# 登录
login = LoginManager()
# 强制登陆认证
login.login_view = 'auth.login'
login.login_message = '请登录'


# CurrentConfig.GLOBAL_ENV = Environment(loader=FileSystemLoader("./templates/charts"))
# import json, datetime
# from datetime import date
# from flask.json import JSONEncoder
# class CustomEncoder(JSONEncoder):
#     def default(self, obj):
#         if isinstance(obj, datetime):
#             return obj.strftime('%Y-%m-%d %H:%M:%S')
#         elif isinstance(obj, date):
#             return obj.strftime('%Y-%m-%d')
#         # elif isinstance(obj,Decimal):
#         #     return str(obj)
#
#         return JSONEncoder.default(self, obj)
#         # return super().default(obj)


# 可用于测试，配置单独的Config
def create_app(config_class=Config):
    # app对象
    _app = Flask(__name__)
    # 向app中添加配置
    _app.config.from_object(config_class)
    # _app.json_encoder = CustomEncoder
    # 注册db
    db.init_app(_app)
    # 注册迁移
    migrate.init_app(_app, db)
    # 登录
    login.init_app(_app)

    #
    # 注册蓝图
    from app.routes import register_blueprint
    register_blueprint(_app)

    return _app


app = create_app()




# 跨域支持
def after_request(resp):
    resp.headers['Access-Control-Allow-Origin'] = '*'
    resp.headers['Access-Control-Allow-Headers'] = 'Authorization'
    return resp


app.after_request(after_request)
# 导入路由文件
# 自上而下加载，未包含就不加载！！！
