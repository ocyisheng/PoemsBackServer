#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2019/12/9 8:28 PM
# @Author  : Gao
# @File    : util.py
# @Software: PyCharm

import os
# import json


def get_local_ip():
    import socket
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(('8.8.8.8', 80))
    ip = s.getsockname()[0]
    s.close()
    return ip


def project_path():
    """
    # 注意这个脚本应放在工程根目录下的一级目录下才有作用
    # 如 ../myProject/util/util.py

    :return: 默认返回工程根目录
    """
    return os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))


def file_path(dirs, file):
    """

    可以正确的创建相对于工程根目录的目录，以及获取路径
    注意不会创建file，但会返回包含file的路径
    :param dirs: 相对目录，若不存在就创建
    :param file: 文件名称
    :return: 文件的路径，但不会创建该文件
    """
    p_path = project_path()
    for path in dirs.split('/'):
        p_path = os.path.join(p_path, path)
    if not os.path.exists(p_path):
        os.makedirs(p_path)
    return os.path.join(p_path, file)
#
#
# def read_json(path):
#     with open(path, 'r', encoding='utf-8') as f:
#         return json.load(f)
#
#
# def write_json(path, o):
#     with open(path, 'w', encoding='utf-8') as f:
#         json.dump(o, f)


if __name__ == '__main__':
    print(file_path('/resources/db/', 'poems.db'))
