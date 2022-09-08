#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time : 2021/5/2 11:30
# @Author : Gao
# @File : __init__.py.py

from flask import Blueprint

bp = Blueprint('home', __name__)

from . import routes