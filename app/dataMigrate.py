# #!/usr/bin/python3
# # -*- coding: utf-8 -*-
# # @Time : 2021/5/2 11:25
# # @Author : Gao
# # @File : dataMigrate.py
#
# from util.util import file_path
# from app import db, app
# from app.models import Poem, PoemWriter, PoemStyle, PoemType
# import json
#
# db.create_all(app=app)
# app.app_context().push()
#
# pPath = file_path('/resources/poems', 'china-poems.json')
# wPath = file_path('/resources/poems', 'china-poems-shiren.json')
# dkPath = file_path('/resources/poems', 'data-keys.json')
#
# errorPath = file_path('/resources/poems', 'error-keys.json')
# def typeStyle():
#     with open(dkPath, 'r', encoding='utf-8') as dataKeyFile:
#         dataKeys = json.load(dataKeyFile)
#         types = dataKeys['type']
#         styles = dataKeys['style']
#         dynastys = dataKeys['dynasty']
#
#         for t in types:
#             p = PoemType(type=t)
#             db.session.add(p)
#         db.session.commit()
#
#         for s in styles:
#             p = PoemStyle(style=s)
#             db.session.add(p)
#
#         db.session.commit()
#
#
# def writers():
#     with open(wPath, 'r', encoding='utf-8') as wf:
#         index = 1
#         for l in wf.readlines():
#             lDic = json.loads(l)
#
#             pt = PoemWriter.dicToSelf(lDic)
#             db.session.add(pt)
#             if index % 50 == 0:
#                 db.session.commit()
#             index += 1
#         db.session.commit()
# def error():
#     with open(errorPath, 'r', encoding='utf-8') as wf:
#
#         ls = json.load(wf)
#         for l in ls:
#             if not PoemWriter.query.filter(PoemWriter.writer==l['writer'],PoemWriter.dynasty==l['dynasty']).first():
#                 pt = PoemWriter.dicToSelf(l)
#                 db.session.add(pt)
#                 db.session.commit()
#
#             writerId = PoemWriter.query.filter(PoemWriter.writer == l['writer'],PoemWriter.dynasty==l['dynasty']).first().id
#             p = Poem.dicToSelf(l)
#             p.writerId = writerId
#
#             if 'type' in l.keys():
#                 t = PoemType.query.filter(PoemType.type == l['type']).first()
#                 if t:
#                     p.typeId = t.id
#
#             if 'style' in l.keys():
#                 s = PoemStyle.query.filter(PoemStyle.style == l['style']).first()
#                 if s:
#                     p.styleId = s.id
#             db.session.add(p)
#         db.session.commit()
#
# def poems():
#     with open(pPath, 'r', encoding='utf-8') as wf:
#
#         errorPoems = []
#         index = 1
#         for l in wf.readlines():
#             try:
#                 lDic = json.loads(l)
#             except:
#                 print(l)
#             if 'comment' in lDic.keys():
#                 if isinstance(lDic['comment'], list):
#                     lDic['comment'] = lDic['comment'][0]
#             pt = Poem.dicToSelf(lDic)
#             if 'dynasty' in lDic.keys():
#
#                 pw = PoemWriter.query.filter(PoemWriter.writer == lDic['writer'],
#                                              PoemWriter.dynasty == lDic['dynasty']).first()
#                 if pw:
#                     pt.writerId = pw.id
#                     if 'type' in lDic.keys():
#                         t = PoemType.query.filter(PoemType.type == lDic['type']).first()
#                         if t:
#                             pt.typeId = t.id
#                         else:
#                             errorPoems.append(lDic)
#                     if 'style' in lDic.keys():
#                         s = PoemStyle.query.filter(PoemStyle.style == lDic['style']).first()
#                         if s:
#                             pt.styleId = s.id
#                         else:
#                             errorPoems.append(lDic)
#
#                     db.session.add(pt)
#
#                     if index % 50 == 0:
#                         db.session.commit()
#                         print(index)
#                 else:
#                     errorPoems.append(lDic)
#             else:
#                 errorPoems.append(lDic)
#             index += 1
#         db.session.commit()
#         print(errorPoems)
#         with open(errorPath,'w') as ew:
#             json.dump(errorPoems,ew,ensure_ascii=False)
#
#
# if __name__ == '__main__':
#     print('dataMigration')
#     # error()
#     # typeStyle()
#     # writers()
#     # poems()
#
#     pw = PoemWriter(id=11402,dynasty='南北朝',writer='庾信',introduction='庾信(513-581)字子山，南阳新野（今河南）人。他是南北朝最后一位优秀诗人，他的诗直接影响着唐代的诗风，在一定程度上，也可说是唐诗的先驱。有《庾子山集》。')
#     db.session.add(pw)
#     db.session.commit()