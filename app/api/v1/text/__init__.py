# coding=utf-8
'''
  Created by lyy on 2019-04-30
'''

__author__ = 'lyy'

from flask import Blueprint

# 定义一个蓝图
text = Blueprint('text', __name__)

from app.api.v1.text import translate
