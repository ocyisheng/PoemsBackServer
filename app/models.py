#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2019/12/26 2:20 AM
# @Author  : Gao
# @File    : models.py
# @Software: PyCharm

# 表模型

from . import db, login
from datetime import datetime, date
from flask_login import UserMixin
from sqlalchemy.orm import class_mapper
import json
from werkzeug.security import generate_password_hash, check_password_hash

# 辅助表 连接users和funds
likePoemsTable = db.Table('likePoems',
                          db.Column('userId', db.Integer, db.ForeignKey('users.id')),
                          db.Column('poemId', db.Integer, db.ForeignKey('poems.id')),
                          db.Column('createdAt', db.DateTime, default=datetime.now())
                          )


# class DateEncoder(json.JSONEncoder):
#     def default(self, obj):
#         if isinstance(obj, datetime):
#             return obj.strftime('%Y-%m-%d %H:%M:%S')
#         elif isinstance(obj, date):
#             return obj.strftime('%Y-%m-%d')
#         # elif isinstance(obj,Decimal):
#         #     return str(obj)
#         else:
#             return json.JSONEncoder.default(self, obj)


# 通用表字段
class BaseModel(object):
    __tablename__ = 'basesTables'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment='自增主键')
    createdAt = db.Column(db.DateTime, default=datetime.now(), comment='行数据创建时间')
    updatedAt = db.Column(db.DateTime, default=datetime.now(), comment='行数据更新时间')

    def __repr__(self):
        repr_string = self.__class__.__name__ + ',' + self.__tablename__
        return repr_string + self.toJson() + '\n'

    def toDic(self):
        columns = [c.key for c in class_mapper(self.__class__).columns]
        return dict((c, BaseModel._encoder(getattr(self, c))) for c in columns if getattr(self, c))

    def toJson(self):
        return json.dumps(self.toDic(), ensure_ascii=False)

    def update(self, dic):
        for k, v in dic.items():
            if hasattr(self, k):
                self.__setattr__(k, v)
        return self

    @classmethod
    def dicToSelf(cls, dic):
        clsSelf = cls()
        for k, v in dic.items():
            if hasattr(clsSelf, k):
                clsSelf.__setattr__(k, v)
        return clsSelf

    @staticmethod
    def _encoder(obj):
        if isinstance(obj, datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, date):
            return obj.strftime('%Y-%m-%d')
        # elif isinstance(obj,Decimal):
        #     return str(obj)
        return obj


@login.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class PoemWriter(db.Model, BaseModel):
    __tablename__ = "poemWriters"
    writer = db.Column(db.String(8), nullable=False, comment='作者')  # 作者
    dynasty = db.Column(db.String(4), nullable=False, default='诗友', comment='朝代')  # 朝代
    introduction = db.Column(db.String, nullable=True, comment='生平介绍')  # 生平介绍
    userId = db.Column(db.Integer, db.ForeignKey('users.id'), comment='用户id')

    poems = db.relationship('Poem', backref='writer', lazy='dynamic')

    @classmethod
    def writerId(cls, w):
        pw = PoemWriter.query.filter(PoemWriter.writer == w).first()
        if pw: return pw.id


class Poem(db.Model, BaseModel):
    __tablename__ = "poems"
    title = db.Column(db.String, comment="名称", nullable=False)  # 名称
    dynasty = db.Column(db.String(4), nullable=False, default='诗友', comment='朝代')  # 朝代
    writerId = db.Column(db.Integer, db.ForeignKey('poemWriters.id'), comment='作者id')  # 作者
    typeId = db.Column(db.Integer, db.ForeignKey('poemTypes.id'), comment='体裁id')  # 体裁 五律等
    styleId = db.Column(db.Integer, db.ForeignKey('poemStyles.id'), comment='风格id')  # 风格 山水等
    content = db.Column(db.String, nullable=False, comment='内容')  # 内容
    comment = db.Column(db.String, nullable=False, default='', comment='评论')  # 点评

    # 点评
    comments = db.relationship('Comment', backref='poem', lazy='dynamic')


class PoemStyle(db.Model, BaseModel):
    __tablename__ = 'poemStyles'
    style = db.Column(db.String(4), comment='风格')

    poems = db.relationship('Poem', backref='style', lazy='dynamic')

    @classmethod
    def styleId(cls, s):
        ps = PoemStyle.query.filter(PoemStyle.style == s).first()
        if ps: return ps.id


class PoemType(db.Model, BaseModel):
    __tablename__ = 'poemTypes'
    type = db.Column(db.String(8), comment='体裁 词牌等')

    poems = db.relationship('Poem', backref='type', lazy='dynamic')

    @classmethod
    def typeId(cls, t):
        pt = PoemType.query.filter(PoemType.type == t).first()
        if pt: return pt.id


class User(db.Model, BaseModel, UserMixin):
    __tablename__ = 'users'
    nickName = db.Column(db.String(8), comment='昵称')
    password = db.Column(db.String(128), comment='密码哈希')
    email = db.Column(db.String(120), index=True, comment='邮件地址')

    ## 关系连接
    # 喜欢的诗歌
    likedPoems = db.relationship(
        'Poem',  # 关联到右侧funds表
        secondary=likePoemsTable,  # 中间辅助表
        backref=db.backref('likers'),  # 反向关联属性user
        lazy='dynamic'
    )
    # 评论
    comments = db.relationship('Comment', backref='user', lazy='dynamic')

    writer = db.relationship('PoemWriter', backref='user', lazy='dynamic')

    # 关注
    def like(self, poemId):
        poem = Poem.query.get(poemId)
        if not self.isLike(poemId):
            self.likedPoems.append(poem)
            db.session.commit()
        return poem

    # 取消关注
    def unLike(self, poemId):
        poem = Poem.query.get(poemId)
        if self.isLike(poemId):
            self.likedPoems.remove(poem)
            db.session.commit()
        return poem

    # 是否关注
    def isLike(self, poemId):
        return self.likedPoems.filter(likePoemsTable.c.poemId == poemId).count() > 0

    # 喜欢的诗歌
    def likePoems(self):
        return Poem.query.join(likePoemsTable).filter(
            likePoemsTable.c.userId == self.id).order_by(
            likePoemsTable.c.createdAt.desc())

    # 密码验证
    def setPassword(self, password):
        self.password = generate_password_hash(password)

    def checkPassword(self, password):
        return check_password_hash(self.password, password)

    # 成为作者
    def beWriter(self, writer):
        mw = self.writer.first()
        if mw:
            db.session.merge(mw.update(writer.toDic()))
        else:
            writer.userId = self.id
            db.session.add(writer)
        db.session.commit()
        return mw


# class Message(BaseModel):
#     __tablename__ = 'messages'
#     senderId = db.Column(db.Integer, db.ForeignKey('user.id'))
#     recipientId = db.Column(db.Integer, db.ForeignKey('user.id'))
#     body = db.Column(db.String(140), comment='信息内容')


class Comment(db.Model, BaseModel):
    __tablename__ = 'comments'
    content = db.Column(db.String(140), comment='点评内容')

    userId = db.Column(db.Integer, db.ForeignKey('users.id'), comment='点评人的id')
    poemId = db.Column(db.Integer, db.ForeignKey('poems.id'), comment='诗词id')

    likeCount = db.Column(db.Integer, comment='点赞的人数')
