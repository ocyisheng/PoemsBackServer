#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time : 2021/5/18 10:37
# @Author : Gao
# @File : comment.py

from flask_restful import fields
from ... import db
from .. import ArgumentType, ResourcesView, ResourceView, user_id, auth
from ...models import Poem, PoemWriter, PoemStyle, PoemType, Comment

commentFields = {
    'commenter': fields.String(attribute=lambda x: x.user.nickName),
    'commenterId': fields.String(attribute=lambda x: x.userId),
    'commentId': fields.Integer(attribute=lambda x: x.id),
    'content': fields.String,
    'likeCount': fields.Integer,

}


class CommentView(ResourceView):

    def __init__(self):
        super().__init__()
        self.parse.add_argument('poemId', type=str, required=True, trim=True, nullable=False)
        self.parse.add_argument('content', type=str, required=True, trim=True, nullable=False)

    @auth.login_required
    def post(self):
        args = self.parse.parse_args()
        poemId = args['poemId']
        if Poem.query.get(args['poemId']):
            ct = Comment(content=args['content'], userId=user_id(), poemId=poemId)
            db.session.add(ct)
            db.session.commit()
            return self.resource()
        return self.resource(message='您评论的诗歌不存在', status=1)


class CommentsView(ResourcesView):
    resourceFields = commentFields

    def __init__(self):
        super().__init__()
        self.parse.add_argument('poemId', type=int, required=True, trim=True, nullable=False)

    def get(self):
        args = self.parse.parse_args()
        poemId = args['poemId']
        poem = Poem.query.get(poemId)
        if poem:
            comments = self.paginate(poem.comments.order_by(Comment.createdAt.asc()), self.parse.parse_args())
            return self.resource(comments)
        return self.resource(message='该诗歌不存在', status=1)
