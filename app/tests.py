#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2019-07-11 10:52
# @Author  : 高春阳
# @File    : tests.py
# @Software: PyCharm

import unittest
from app import db, create_app
from app.models import User, Poem, PoemWriter, PoemStyle, PoemType, Comment


class TestConfig(object):
    # 临时的sqlite 路径，默认是内存中
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
    SQLALCHEMY_TRACK_MODIFICATIONS = True


class UserModelCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print("\nthis setupclass() method only called once.\n")

    @classmethod
    def tearDownClass(cls):
        print("this teardownclass() method only called once too.\n")

    def setUp(self):
        print('setUp')
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        print('tearDown')
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def addDatas(self):
        u1 = User(nickName='susuan', email='susuan@example.com')
        u1.setPassword('cat')

        u2 = User(nickName='green', email='green@example.com')
        u2.setPassword('dog')

        db.session.add(u1)
        db.session.add(u2)

        w = PoemWriter(writer='李白', dynasty='唐', introduction='浪漫主义诗人，最牛逼的诗人')
        db.session.add(w)

        t = PoemType(type='七绝')
        s = PoemStyle(style='山河')
        db.session.add(t)
        db.session.add(s)

        t1 = PoemType(type='五绝')
        s1 = PoemStyle(style='思念')
        db.session.add(t1)
        db.session.add(s1)

        p1 = Poem(title='望庐山瀑布', dynasty='唐', content='日照香炉生紫烟，遥看瀑布挂前川。飞流直下三千尺，疑是银河落九天', writerId=1, typeId=1,
                  styleId=1)
        db.session.add(p1)

        p2 = Poem(title='静夜思', dynasty='唐', content='床前明月光，疑是地上霜。举头望明月，低头思故乡。', writerId=1, typeId=2,
                  styleId=2)
        db.session.add(p2)

        db.session.commit()

        # pw = PoemWriter.query.get(1)
        # pt = PoemType.query.get(1)
        # ps = PoemStyle.query.get(1)
        # pp = Poem.query.get(1)

    def test_user(self):
        u = User(nickName='susuan', email='susuan@example.com')
        u.setPassword('cat')
        self.assertFalse(u.checkPassword('dog'))
        self.assertTrue(u.checkPassword('cat'))

    def test_poem(self):
        w = PoemWriter(writer='李白', dynasty='唐', introduction='浪漫主义诗人，最牛逼的诗人')
        db.session.add(w)
        db.session.commit()

        t = PoemType(type='七绝')
        s = PoemStyle(style='山河')
        db.session.add(t)
        db.session.add(s)
        db.session.commit()

        p = Poem(title='望庐山瀑布', dynasty='唐', content='日照香炉生紫烟，遥看瀑布挂前川。飞流直下三千尺，疑是银河落九天', writerId=1, typeId=1, styleId=1)
        db.session.add(p)
        db.session.commit()

        pw = PoemWriter.query.get(1)

        self.assertEqual(pw.writer, '李白')
        self.assertEqual(pw.dynasty, '唐')

        pt = PoemType.query.get(1)
        ps = PoemStyle.query.get(1)
        pp = Poem.query.get(1)

        #
        self.assertEqual(pw.poems.first().writerId, pp.writerId)
        self.assertEqual(pt.poems.first().typeId, pp.typeId)
        self.assertEqual(ps.poems.first().styleId, pp.styleId)
        self.assertEqual(pp.writer.writer, '李白')
        self.assertEqual(pp.style.style, '山河')
        self.assertEqual(pp.type.type, '七绝')

    def test_like(self):
        self.addDatas()
        u1 = User.query.get(1)
        u2 = User.query.get(2)

        # pw = PoemWriter.query.get(1)
        # pt = PoemType.query.get(1)
        # ps = PoemStyle.query.get(1)
        pp = Poem.query.get(1)
        pp2 = Poem.query.get(2)

        u1.like(pp)
        u1.like(pp2)

        self.assertEqual(u1.likePoems().all(), [pp, pp2])
        self.assertEqual(u2.likePoems().all(), [])

        u1.unLike(pp)
        self.assertFalse(u1.isLike(pp))
        self.assertEqual(u1.likePoems().all(), [pp2])

        u2.like(pp2)

        self.assertEqual(pp2.likers, [u1, u2])



if __name__ == '__main__':
    unittest.main(verbosity=2)
