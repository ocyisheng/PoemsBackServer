#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2020/8/1 10:32 AM
# @Author  : Gao
# @File    : search.py
# @Software: PyCharm

"""



"""

from flask_restful import fields
from .. import  ResourcesView
from ...models import Poem, PoemWriter

type_argument = {
    '1': 'title',
    '2': 'writer',
    '3': 'content',
}

resource_fields = {
    'poemId': fields.Integer(attribute='id', default=0),
    'writerId': fields.Integer(attribute=lambda x: x.writer.id, default=0),
    'writer': fields.String(attribute=lambda x: x.writer.writer),
    'dynasty': fields.String,
    'title': fields.String,
    'content': fields.String,
    'comment': fields.String(default=''),
}


class SearchResultView(ResourcesView):
    resourceFields = resource_fields

    def __init__(self):
        super().__init__()
        self.parse.add_argument('type', type=str, choices=['1', '2', '3'], default='1', required=True, trim=True,
                                ignore=True)
        self.parse.add_argument('kword', type=str, required=True, trim=True, ignore=True)
        self.parse.add_argument('dynasty', type=str, required=False, trim=True, ignore=True)

    def get(self):
        args = self.parse.parse_args()
        like_word = args['kword']
        type_arg = args['type']
        query = Poem.query
        if 'title' == type_argument[type_arg]:
            query = query.filter(Poem.title.like('%{}%'.format(like_word)))

        if 'content' == type_argument[type_arg]:
            query = query.filter(Poem.content.like('%{}%'.format(like_word)))

        if 'writer' == type_argument[type_arg]:
            wquery = PoemWriter.query.filter(PoemWriter.writer.like('%{}%'.format(like_word)))
            query = query.join(wquery).filter(Poem.writerId == PoemWriter.id)

        if 'dynasty' in args.keys() and args['dynasty']:
            query = query.filter(Poem.dynasty == args['dynasty'])

        query = query.order_by(Poem.createdAt.asc())
        fs = self.paginate(query=query, args=args)
        return self.resource(fs)
