#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2020/4/27 2:46 PM
# @Author  : Gao
# @File    : auth.py
# @Software: PyCharm
from ... import db
from .. import ResourceView, auth, auth_token, id_from_token, user_id
from app.models import User
from .. import ArgumentType


def uerNameExist(value):
    if isinstance(value, str):
        if value == '':
            raise ValueError("value is not a '' string")
        if User.query.filter(User.nickName == value).first():
            raise ValueError("{} 已经存在，更换新的名称".format(value))
        return value
    raise ValueError("only validate str instance")


class UserRegisterView(ResourceView):

    def __init__(self):
        super().__init__()
        self.parse.add_argument('name', type=uerNameExist, required=True, nullable=False, trim=True)
        self.parse.add_argument('password', type=ArgumentType.empty_str, required=True, nullable=False, trim=True)

    def post(self):
        args = self.parse.parse_args()
        u = User(nickName=args['name'])
        u.setPassword(password=args['password'])
        db.session.add(u)
        db.session.commit()
        return self.resource(message='注册成功')


class UserResetPasswordView(ResourceView):

    def __init__(self):
        super().__init__()
        self.parse.add_argument('password', type=ArgumentType.empty_str, required=True, nullable=False, trim=True)
        self.parse.add_argument('passwordNew', type=ArgumentType.empty_str, required=True, nullable=False, trim=True)

    @auth.login_required
    def post(self):
        args = self.parse.parse_args()
        u = User.query.get(user_id())
        if not u.checkPassword(password=args['password']): return self.resource(message='旧密码错误', status=0)
        u.setPassword(password=args['passwordNew'])
        db.session.commit()
        return self.resource(message='重置成功')


class UserFundPasswordView(ResourceView):
    pass


class UserLoginView(ResourceView):
    def __init__(self):
        super().__init__()
        self.parse.add_argument('name', type=ArgumentType.empty_str, required=True, nullable=False, trim=True)
        self.parse.add_argument('password', type=ArgumentType.empty_str, required=True, nullable=False, trim=True)

    def post(self):
        args = self.parse.parse_args()
        u = User.query.filter(User.nickName == args['name']).first()
        if not u: return self.resource(message='用户名不存在', status=1)
        if u.checkPassword(args['password']):
            token = auth_token(auth_id=u.id)
            return self.resource(data={'token': token})
        return self.resource(message='密码错误', status=1)


class UserLogoutView(ResourceView):
    # 这里需要做储存比较
    @auth.login_required
    def post(self):
        return self.resource(message='退出成功')


class UserRefreshTokenView(ResourceView):

    def __init__(self):
        super().__init__()
        self.parse.add_argument('token', type=ArgumentType.empty_str, required=True, nullable=False, trim=True)

    @auth.login_required
    def post(self):
        args = self.parse.parse_args()
        token = args['token']
        u_id = id_from_token(token)
        return self.resource(data={'token': auth_token(auth_id=u_id)})
