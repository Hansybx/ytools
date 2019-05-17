# coding=utf-8
'''
  Created by lyy on 2019-05-16
'''

__author__ = 'lyy'

from flask import Blueprint

# 定义一个蓝图
song = Blueprint('song', __name__)

from app.api.v1.song import download_song


@song.route('/')
def say_hello():
    return '这里是音乐处理类的接口'
