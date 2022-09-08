#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2019/12/26 2:21 AM
# @Author  : Gao
# @File    : forms.py
# @Software: PyCharm

# 表单
from flask_wtf import FlaskForm
from app.validate import RequestParamsValidate


class SYFlaskForm(FlaskForm, RequestParamsValidate):

    def validate_fail(self):
        """
        :return:
        """
        messages = ''
        for k, v in self.errors.items():
            messages += '{}:{}\n'.format(k, v)

        return super().validate_request_fail(messages=messages)

    def validate_success(self, data):

        """

        :param data:
        :return:
        """
        return super().validate_request_success(data=data)
