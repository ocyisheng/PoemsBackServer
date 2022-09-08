#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2020/4/13 7:23 PM
# @Author  : Gao
# @File    : validate.py
# @Software: PyCharm
from flask import jsonify


class Code(dict):

    def code(self, code):
        return self[code]


def Resource(data, code, messages):
    return jsonify({
        'code': code,
        'messages': messages,
        'data': data,
    })


class ParamsValidate:

    @staticmethod
    def _validate(data, code, messages):
        return jsonify({
            'code': code,
            'messages': messages,
            'data': data,
        })

    def validate_success(self, data):
        return self._validate(data=data, code=0, messages='success')

    def validate_fail(self, code, messages):
        return self._validate(data='no', code=code, messages=messages)


class RequestParamsValidate(ParamsValidate, Code):
    def validate_request_fail(self, messages):
        return super().validate_fail(code=1, messages=messages)

    def validate_request_success(self, data):
        return super().validate_success(data=data)

    def code(self, code):
        # 1 系
        code_doc = {1, '请求参数错误'}
        return code_doc[code]


class RespondParamsValidate(ParamsValidate, Code):
    def json_validate_respond_fail(self, messages):
        return super().validate_fail(code=2, messages=messages)

    def json_validate_respond_success(self, data):
        return super().validate_success(data=data)

    def code(self, code):
        # 2系
        code_doc = {2, '响应数据错误'}
        return code_doc[code]
