# coding=utf-8
'''
  Created by lyy on 2019-04-04
'''

__author__ = 'lyy'


class Res:
    status = 200
    msg = ''
    info = []

    def __init__(self, status, msg, info):
        self.status = status
        self.msg = msg
        self.info = info
