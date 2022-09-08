#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time : 2021/5/3 11:31
# @Author : Gao
# @File : user.py

from flask_restful import fields
from .. import ArgumentType, ResourcesView, ResourceView, auth, user_id
from ...models import Poem, User, PoemWriter

resource_fields = {
    'poemId': fields.Integer(attribute=lambda x: x.id),
    'title': fields.String,
    'writer': fields.String(attribute=lambda x: x.writer.writer),
    'dynasty': fields.String,
    'type': fields.String(attribute=lambda x: None if not x.type else x.type.type, default=''),
    'style': fields.String(attribute=lambda x: None if not x.style else x.style.style, default=''),
    'content': fields.String,
}


class UserLikePoemsView(ResourcesView):
    resourceFields = resource_fields

    def __init__(self):
        super().__init__()
        self.parse.add_argument('userId', type=int, required=False, trim=True, ignore=True)

    @auth.login_required
    def get(self):
        args = self.parse.parse_args()
        userId = user_id()
        if 'userId' in args.keys() and args['userId']:
            userId = args['userId']
        u = User.query.get(userId)
        ps = self.paginate(query=u.likePoems(), args=args)
        return self.resource(ps)


class UserLikePoemView(ResourceView):
    resourceFields = resource_fields
    def __init__(self):
        super().__init__()
        self.parse.add_argument('poemId', type=int, required=True, trim=True, ignore=False)

    @auth.login_required
    def get(self):
        args = self.parse.parse_args()
        u = User.query.get(user_id())
        p = u.like(args['poemId'])
        return self.resource(p)


class UserUnLikePoemView(ResourceView):
    resourceFields = resource_fields
    def __init__(self):
        super().__init__()
        self.parse.add_argument('poemId', type=int, required=True, trim=True, ignore=False)

    @auth.login_required
    def get(self):
        args = self.parse.parse_args()
        u = User.query.get(user_id())
        p = u.unLike(args['poemId'])
        return self.resource(p)


class UserView(ResourceView):
    resourceFields = resource_fields

    def __init__(self):
        super().__init__()
        self.parse.add_argument('code', type=ArgumentType.empty_str, required=True, trim=True, nullable=False)

    def get(self):
        args = self.parse.parse_args()
        code = args['code']
        f = Poem.query.filter(Poem.code == code).first()
        if not f: return self.resource(data='', message='[code={}]不存在'.format(code))
        return self.resource(f)

