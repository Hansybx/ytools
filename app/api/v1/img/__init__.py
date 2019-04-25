# coding=utf-8
'''
  Created by lyy on 2019-04-19
'''

__author__ = 'lyy'

from flask import Blueprint

# 定义一个蓝图
img = Blueprint('img', __name__)

from app.api.v1.img import pornhub, style_change


@img.route('/')
def say_hello():
    return 'hello,this is image'
