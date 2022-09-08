#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2019/12/18 8:30 PM
# @Author  : Gao
# @File    : routes.py
# @Software: PyCharm

# 路由

# # 注册蓝图
def register_blueprint(app):
	from .api import bp as api_bp
	app.register_blueprint(api_bp)
