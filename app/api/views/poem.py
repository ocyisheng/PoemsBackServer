#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2020/4/27 2:46 PM
# @Author  : Gao
# @File    : poem.py
# @Software: PyCharm

from flask_restful import fields
from ... import db
from .. import ArgumentType, ResourcesView, ResourceView
from ...models import Poem, PoemWriter, PoemStyle, PoemType
from datetime import datetime

proToClass = {
    "writer": PoemWriter,
    "style": PoemStyle,
    "type": PoemType
}
resource_fields = {
    'poemId': fields.Integer(attribute='id'),
    'writerId': fields.Integer(attribute=lambda x: x.writer.id),
    'type': fields.String(attribute=lambda x: x.type.type if x.type else None, default=''),
    'style': fields.String(attribute=lambda x: x.style.style if x.style else None, default=''),
    'title': fields.String,
    'writer': fields.String(attribute=lambda x: x.writer.writer),
    'dynasty': fields.String,
    'content': fields.String,
    'comment': fields.String(default=''),
}


class PoemView(ResourceView):
    def get(self):
        pass

    def post(self, poemId):
        pass

    def put(self):
        # 更新某个id的用户的信息（需要提供用户的所有信息）
        pass

    def patch(self):
        # 更新某个id的用户信息（只需要提供需要改变的信息）
        pass

    def delete(self):
        pass


class PoemViewAddUpdate(ResourceView):

    def __init__(self):
        super().__init__()
        self.parse.add_argument('title', type=ArgumentType.empty_str, required=True, trim=True, nullable=False)
        self.parse.add_argument('content', type=ArgumentType.empty_str, required=True, trim=True, nullable=False)
        self.parse.add_argument('type', type=ArgumentType.empty_str, required=False, trim=True, nullable=False)
        self.parse.add_argument('style', type=ArgumentType.empty_str, required=False, trim=True, nullable=False)

    def post(self):
        args = self.parse.parse_args(strict=True)
        if not Poem.query.filter(Poem.code == args['code']).first():
            args['established_at'] = datetime.strptime(args['established_at'], '%Y-%m-%d')
            f = Poem.dic_to_self(args)
            db.session.add(f)
            db.session.commit()
            return self.resource(message='添加成功')
        return self.resource(message='添加成功')

    def put(self):
        args = self.parse.parse_args()
        code = args['code']
        f = Poem.query.filter(Poem.code == code).first()
        if not f: return self.resource(message='[code={}]不存在'.format(code))
        if 'established_at' in args.keys():
            args['established_at'] = datetime.strptime(args['established_at'], '%Y-%m-%d')
        f.update(args)
        db.session.commit()
        return self.resource(message='更新成功')


class PoemViewGetDelete(ResourceView):
    resourceFields = resource_fields

    def __init__(self):
        super().__init__()
        self.parse.add_argument('code', type=str, required=True, trim=True, nullable=False)

    def get(self):
        args = self.parse.parse_args()
        code = args['code']
        f = Poem.query.filter(Poem.code == code).first()
        if not f: return self.resource(data='', message='[code={}]不存在'.format(code))
        return self.resource(f)

    def delete(self):
        args = self.parse.parse_args()
        code = args['code']
        f = Poem.query.filter(Poem.code == code).first()
        if not f: return self.resource(message='[code={}]不存在'.format(code))
        db.session.delete(f)
        db.session.commit()
        return self.resource(f, message='删除成功')


class PoemsView(ResourcesView):
    resourceFields = resource_fields

    def __init__(self):
        super().__init__()
        self.parse.add_argument('writer', type=str, required=False, trim=True, ignore=True)
        self.parse.add_argument('dynasty', type=str, required=False, trim=True, ignore=True)
        self.parse.add_argument('style', type=str, required=False, trim=True, ignore=True)
        self.parse.add_argument('type', type=str, required=False, trim=True, ignore=True)

    def get(self):
        args = self.parse.parse_args()
        query = Poem.query
        for ak in args.keys():
            av = args[ak]
            if ak == "writer":
                wt = PoemWriter.writerId(av)
                if wt:
                    query = query.filter(Poem.writerId == wt)

            if ak == "style":
                wt = PoemStyle.styleId(av)
                if wt:
                    query = query.filter(Poem.styleId == wt)

            if ak == "type":
                wt = PoemType.typeId(av)
                if wt:
                    query = query.filter(Poem.typeId == wt)

            if av and ak == "dynasty":
                query = query.filter(Poem.dynasty == av)

        query = query.order_by(Poem.createdAt.asc())
        fs = self.paginate(query=query, args=args)
        return self.resource(fs)
