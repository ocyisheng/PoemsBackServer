#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2020/4/28 12:29 PM
# @Author  : Gao
# @File    : routes.py
# @Software: PyCharm

from flask_restful import Api
from . import bp

api = Api(bp, prefix='/api')

# 以下注册url
from app.api.views import auth, poem, writer, comment, user,search

#
api.add_resource(poem.PoemsView, '/poems')
api.add_resource(poem.PoemViewGetDelete, '/poem')
api.add_resource(poem.PoemViewAddUpdate, '/poem/add')
#
api.add_resource(writer.PoemWritersView, '/writers')
api.add_resource(writer.BeWriterView,'/writer')

api.add_resource(comment.CommentView, '/comment')
api.add_resource(comment.CommentsView, '/comments')

api.add_resource(auth.UserRegisterView, '/auth/register')
api.add_resource(auth.UserLoginView, '/auth/login')
api.add_resource(auth.UserResetPasswordView, '/auth/reset')
api.add_resource(auth.UserLogoutView, '/auth/logout')
api.add_resource(auth.UserRefreshTokenView, '/auth/rftoken')


api.add_resource(user.UserLikePoemsView, '/user/likes')
api.add_resource(user.UserLikePoemView, '/user/like')
api.add_resource(user.UserUnLikePoemView, '/user/unlike')


api.add_resource(search.SearchResultView,'/search')
