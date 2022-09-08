#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time : 2021/5/2 17:38
# @Author : Gao
# @File : writer.py
from flask_restful import fields
from .. import ArgumentType, ResourcesView, ResourceView, auth, user_id
from ...models import PoemWriter, User

resource_fields = {
    'writerId': fields.Integer(attribute='id', default=0),
    'writer': fields.String,
    'dynasty': fields.String,
    'introduction': fields.String,
}


class BeWriterView(ResourceView):
    resourceFields = resource_fields

    def __init__(self):
        super().__init__()
        self.parse.add_argument('writer', type=ArgumentType.empty_str, required=False, trim=True, nullable=False)
        self.parse.add_argument('introduction', type=ArgumentType.empty_str, required=False, trim=True, nullable=False)

    @auth.login_required
    def get(self):
        u = User.query.get(user_id())
        uw = u.writer.first()
        if uw:
            return self.resource(data=uw.toDic())
        p = PoemWriter(writer=u.nickName, dynasty='诗友', introduction='')
        return self.resource(data=p.toDic())

    @auth.login_required
    def post(self):
        args = self.parse.parse_args()
        u = User.query.get(user_id())
        w = PoemWriter.dicToSelf(args)
        w = u.beWriter(writer=w)
        return self.resource(data=w.toDic())



class PoemWritersView(ResourcesView):
    resourceFields = resource_fields

    def __init__(self):
        super().__init__()
        self.parse.add_argument('dynasty', type=str, required=False, trim=True, ignore=True)

    def get(self):
        args = self.parse.parse_args()
        query = PoemWriter.query
        if 'dynasty' in args.keys() and args['dynasty']:
            query = query.filter(PoemWriter.dynasty == args['dynasty'])
        query = query.order_by(PoemWriter.createdAt.asc())
        fs = self.paginate(query=query, args=args)
        return self.resource(fs)
