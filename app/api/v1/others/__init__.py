# coding=utf-8
'''
  Created by lyy on 2019-06-10
'''

__author__ = 'lyy'

from flask import Blueprint

# 定义一个蓝图
others = Blueprint('others', __name__)


@others.route('/')
def say_hello():
    return '这里是其他类的接口'
