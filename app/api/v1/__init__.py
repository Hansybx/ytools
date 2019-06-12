# coding=utf-8
'''
  Created by lyy on 2019-04-04
'''

__author__ = 'lyy'

from flask import Blueprint

# 定义一个蓝图
v1 = Blueprint('v1', __name__)

from app.api.v1.img import img
from app.api.v1.user import user
from app.api.v1.text import text
from app.api.v1.song import song
from app.api.v1.others import others
