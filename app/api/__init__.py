#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2020/4/27 2:45 PM
# @Author  : Gao
# @File    : __init__.py.py
# @Software: PyCharm


import flask_restful
from flask_restful import abort, marshal, reqparse, fields
from flask_restful import Resource as Res
from flask_httpauth import HTTPTokenAuth
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous import SignatureExpired, BadSignature
from flask import request

secret_key = "pbsLike"
salt = "gao"

auth = HTTPTokenAuth()


@auth.verify_token
def verify_token(token) -> bool:
    s = Serializer(secret_key=secret_key)
    try:
        data = s.loads(token, salt=salt)
    except (SignatureExpired, BadSignature):
        return False
    if 'id' in data:
        return True
    return False


@auth.error_handler
def unauthorized():
    return response(data='', message='token过期， 请重新登录', status=1)


def auth_token(auth_id, exp=360000):
    s = Serializer(secret_key=secret_key, expires_in=exp)
    t = s.dumps({'id': auth_id}, salt=salt)
    return t.decode()


def user_id() -> int:
    return id_from_token(token_form_request())


def token_form_request():
    return request.headers.get('Authorization').split('Bearer')[-1].strip()


def id_from_token(token) -> int:
    s = Serializer(secret_key=secret_key)
    data = s.loads(token, salt=salt)
    return data['id']

def response(data, message, status):
    return {
        'status': status,
        'message': message,
        'data': data
    }

def my_abort(http_status_code, **kwargs):
    if http_status_code == 400:
        # 重定义400返回参数
        abort(400, **response(data='', message=kwargs.get('message'), status=1))
    abort(http_status_code)


flask_restful.abort = my_abort


class ArgumentType:
    @staticmethod
    def empty_str(value):
        if isinstance(value, str):
            if value == '':
                raise ValueError("value is not a '' string")
            return value
        raise ValueError("only validate str instance")


class Resource(Res):
    resourceFields = {}

    def __init__(self):
        self.parse = reqparse.RequestParser()

    def resource(self, data='', message='成功', status=0):
        res = data if self.resourceFields == {} else marshal(data=data, fields=self.resourceFields)
        return response(res, message, status)

    #
    # def get(self):
    # 	abort(http_status_code=400, message='选择正确的请求方式')
    # #
    # def post(self):
    # 	abort(http_status_code=400, message='选择正确的请求方式')

    # def put(self):
    # 	# 更新某个id的用户的信息（需要提供用户的所有信息）
    # 	abort(http_status_code=400, message='选择正确的请求方式')
    #
    # def patch(self):
    # 	# 更新某个id的用户信息（只需要提供需要改变的信息）
    # 	abort(http_status_code=400, message='选择正确的请求方式')
    #
    # def delete(self):
    # 	abort(http_status_code=400, message='选择正确的请求方式')


class ResourceView(Resource):
    pass


class ResourcesView(Resource):
    resourceFields = {}

    paginateFields = {
        'total': fields.Integer(attribute=lambda x: x.total),
        'pages': fields.Integer(attribute=lambda x: x.pages),
        'page': fields.Integer(attribute=lambda x: x.page),
        'next_num': fields.Integer(attribute=lambda x: x.next_num),
        'prev_num': fields.Integer(attribute=lambda x: x.prev_num),
        'has_next': fields.Boolean(attribute=lambda x: x.has_next),
        'has_prev': fields.Boolean(attribute=lambda x: x.has_prev),
        'items': None
    }

    def __init__(self):
        # 这里必须添加super
        super().__init__()
        self.parse.add_argument('page', type=int, ignore=True, default=1)
        self.parse.add_argument('pages', type=int, ignore=True, default=10)

    @staticmethod
    def paginate(query, args):
        page = args['page']
        per_page = args['pages']
        return query.paginate(page=page, per_page=per_page, error_out=False)

    def resource(self, data='', message='成功', status=0):
        self.paginateFields['items'] = fields.Nested(self.resourceFields)
        self.resourceFields = self.paginateFields
        return super().resource(data=data, message=message, status=status)


# class ApiDoc(object):
#     argHold = ['name', 'default', 'required', 'ignore', 'type', 'choices', 'help', 'nullable']
#     _resources = set()
#
#     @classmethod
#     def register(cls, resource: Resource.__class__):
#         cls._resources.add(resource)
#
#     @classmethod
#     def apiDocs(cls):
#         for res in cls._resources:
#             resView = res()
#             for g in resView.parse.args:
#                 ng = {}
#                 for ah in cls.argHold:
#                     v = g.__dict__[ah]
#                     # print(v)
#                     if ah == 'type' and  isinstance(v, str.__class__):
#                         print(v.__class__)
#                         print(ah)
#                     ng[ah] = v
#                 print(ng)
#
#             #
#         # print(argumets)
#
#
# apiDoc = ApiDoc()

from flask import Blueprint

bp = Blueprint('api', __name__)
from . import routes
