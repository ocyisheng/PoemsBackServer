#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2020/4/26 11:56 PM
# @Author  : Gao
# @File    : recommend.py
# @Software: PyCharm
import math


class Recommend:

    def __init__(self, data: dict, filter='id'):
        """
        :param data: {key:[{id:0,field1=xxx},{id=1,field1=xxxx}]}
        :param filter: 过滤相同
        """
        self.__data = data
        self.__filter = filter

    def simliars(self, key, relation, pearson=0.6):
        """
        计算相似度
        :param key: 唯一
        :param relation: 相应字段
        :param pearson: 皮尔逊系数
        :return: []
        """
        res = []
        for k in self.__data.keys():
            if not (k == key):
                xys = self.xy_values(xkey=key, ykey=k, relation=relation)
                # 查找皮尔逊系数正相关超过0.6
                if self.pearson(xys[0], xys[1]) > pearson:
                    simliar = self.euclidean(xys[0], xys[1])
                    res.append((k, simliar))
        res.sort(key=lambda val: val[1], reverse=True)

        return res

    def xy_values(self, xkey, ykey, relation):
        x_dict_values = self.dict_values(xkey, [relation])
        y_dict_values = self.dict_values(ykey, [relation])
        y_values, x_values = [], []
        for x_k in x_dict_values.keys():
            if x_k in y_dict_values.keys():
                x_values.append(x_dict_values[x_k][0])
                y_values.append(y_dict_values[x_k][0])
        return x_values, y_values

    def dict_values(self, key, fields):
        rs = {}
        for value in self.__data[key]:
            values = []
            for field in fields:
                values.append(value[field])
            rs[value[self.__filter]] = values
        return rs

    def pearson(self, xs, ys):
        """
        皮尔逊系数
         -1：完全负相关  1：完全正相关  0：不相关
            0.8-1.0 极强相关
            0.6-0.8 强相关
            0.4-0.6 中等程度相关
            0.2-0.4 弱相关
            0.0-0.2 极弱相关或无相关
        :param xs:  list [float]
        :param ys:  list [float]
        :return: -1.0 ~ 1.0
        """
        if len(xs) == 0 or len(ys) == 0:
            return 0
        # 计算评分和
        sum_x = sum(xs)
        sum_y = sum(ys)
        # 计算评分平方和
        sumx_sq = sum([math.pow(x, 2) for x in xs])
        sumy_sq = sum([math.pow(y, 2) for y in ys])
        # 计算乘积和
        sum_xy = sum([x_y[0] * x_y[1] for x_y in zip(xs, ys)])
        n = len(xs)
        # 计算相关系数
        num = sum_xy - (sum_x * sum_y / n)
        den = math.sqrt((sumx_sq - pow(sum_x, 2) / n) * (sumy_sq - pow(sum_y, 2) / n))
        if den == 0:
            return 0
        r = num / den
        return r

    def euclidean(self, xs, ys, min_dif=0.5):
        """
        欧拉距离 越大相关性越强
        :param xs: list [float]
        :param ys: list [float]
        :return:  0.0 -- 1.0
        """
        # distance = sum([math.pow(x_y[0] - x_y[1], 2) for x_y in zip(xs, ys) if abs(x_y[0] - x_y[1]) <= min_dif])
        distance = sum([math.pow(x_y[0] - x_y[1], 2) for x_y in zip(xs, ys)])
        # return distance
        return 1 / (1 + math.sqrt(distance))

    def common(self):
        pass

    def recommend(self, key, relation, fields, order_by=None, reverse=True):
        """
        根据key推荐相似的数据，根据用户relation字段的相似度推荐
        :param key: 推荐的唯一标示，例如：用户
        :param relation: 推荐的关系字段，用于匹配相似度
        :param fields: 返回的字段
        :param order_by: 排序，默认升序
        :param reverse: 是否反转，默认升序时为True
        :return: 推荐结果 list
        """
        # 相似度最高的用户
        sims = self.simliars(key=key, relation=relation)
        top_sim_key = sims[0][0]

        # 默认order_by字段与relation相同
        if not order_by:
            order_by = relation

        # 若order_by不在fields中，应插入之，以便查询结果排序
        if order_by not in fields:
            fields.append(order_by)

        # 该key所有fields记录
        key_values = self.dict_values(key, fields)
        top_sim_key_values = self.dict_values(top_sim_key, fields)

        # 过滤与相似用户之间相同的部分
        recommends = [top_sim_key_values[k_v] for k_v in top_sim_key_values.keys() if
                      k_v not in key_values.keys()]

        # 查找排序字段的index
        order_by_index = fields.index(order_by)

        # 默认降序排列
        recommends.sort(key=lambda val: val[order_by_index], reverse=reverse)

        # 若order_by与relation不同，返回结果应过滤order_by字段
        if not order_by == relation:
            recommends_remove = []
            for va in recommends:
                vas = []
                for index, v in enumerate(va):
                    if not index == order_by_index:
                        vas.append(v)
                recommends_remove.append(vas)
            return recommends_remove

        return recommends


if __name__ == '__main__':
    import json

    with open('data.json', 'r') as fr:
        datas = json.load(fr)
        rc = Recommend(data=datas)
        rs = rc.recommend(key='90', relation='rating', fields=['id','rating', 'title'])
        print(rs)
        print(datas['90'])
        print(datas['128'])
        print(datas['133'])
# [3578, 5.0, 'Gladiator (2000)'], [3996, 5.0, '"Crouching Tiger'], [4011, 5.0, 'Snatch (2000)'], [1198, 5.0, 'Raiders of the Lost Ark (Indiana Jones and the Raiders of the Lost Ark) (1981)'], [2571, 5.0, '"Matrix'], [1590, 4.0, 'Event Horizon (1997)']
# [3578, 5.0, 'Gladiator (2000)'], [3996, 5.0, '"Crouching Tiger'], [4011, 5.0, 'Snatch (2000)'], [1198, 5.0, 'Raiders of the Lost Ark (Indiana Jones and the Raiders of the Lost Ark) (1981)'], [2571, 5.0, '"Matrix'], [1590, 4.0, 'Event Horizon (1997)'], [3300, 4.0, 'Pitch Black (2000)']
# [3578, 5.0, 'Gladiator (2000)'], [3996, 5.0, '"Crouching Tiger'], [4011, 5.0, 'Snatch (2000)'], [1198, 5.0, 'Raiders of the Lost Ark (Indiana Jones and the Raiders of the Lost Ark) (1981)'], [2571, 5.0, '"Matrix'], [1590, 4.0, 'Event Horizon (1997)']