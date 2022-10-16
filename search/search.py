#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time : 2022/9/26 11:50
# @Author : Gao
# @File : search.py


import json
import math
from typing import List, Tuple
from collections import defaultdict
from functools import lru_cache
import re
from util.util import file_path
import jieba

file = file_path('resources/poems', 'china-poems.json')
file_index_china_poems = file_path('resources/poems', 'index-china-poems.json')
docs = []
with open(file, encoding="utf8") as rf:
    datas = rf.readlines()
    for data in datas:
        # 将歌词的文本列表转换成一个字符串
        doc = json.loads(data)
        content = doc["content"]
        content = re.sub('[，。！？]', ' ', content)
        content = re.sub('\[.*\]', '', content)
        content = re.sub('[《》]', '', content)
        # 分词
        list_content = list(jieba.cut_for_search(content))
        # print(list_content)
        m_doc = {}
        m_doc["title"] = doc['title']
        # m_doc["dynasty"] = doc['dynasty']
        # m_doc["writer"] = doc['writer']
        m_doc["content"] = list_content

        docs.append(m_doc)

with open(file_index_china_poems, 'w', encoding='utf8') as wf:
    json.dump(docs, wf, ensure_ascii=False)
# 注意: 这里我改了index的数据结构
with open(file_index_china_poems, encoding="utf8") as rf:
    docs = json.load(rf)

index = defaultdict(set)
for doc_index, doc in enumerate(docs):
    for word in doc["content"]:
        index[word].add(doc_index)


# print(index)


def tf(word: str, doc_index: List[str], docs: List[dict]) -> float:
    return docs[doc_index]["content"].count(word) / len(docs[doc_index]["content"])


@lru_cache()
# 因为参数需要哈希缓存，所以docs, index不放在参数中传递了
def idf(word: str) -> float:
    # 多少文档包含word
    doc_included = len(index.get(word, []))
    return math.log(doc_included / len(docs))


def tf_idf(word: str, doc_index: List[str], docs: List[List[str]], index: List[dict]) -> float:
    return tf(word, doc_index, docs) * idf(word)


def search(keywords: str, docs: List[dict], index: dict) -> List[Tuple]:
    doc_indexs = list()
    for keyword in keywords:
        doc_indexs.extend(index.get(keyword, []))

    if not doc_indexs:
        return []

    # 所有包含关键字的doc_index去重
    doc_indexs = set(doc_indexs)

    scores = []
    for doc_index in doc_indexs:
        keywords_scores = []

        for keyword in keywords:
            score = tf_idf(keyword, doc_index, docs, index)
            keywords_scores.append(score)

        scores.append((doc_index, sum(keywords_scores)))

    return sorted(scores, key=lambda x: x[1], reverse=True)


ret = search(["中天", ], docs, index)
print(ret)

with open(file, encoding='utf-8') as r:
    poems = r.readlines()
    for r in ret:
        ind = r[0]
        print(poems[ind])
if __name__ == '__main__':
    print('all search')
