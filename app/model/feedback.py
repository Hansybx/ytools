# coding=utf-8
'''
  Created by lyy on 2019-04-06
'''
from sqlalchemy import Column, Integer, String

from app.model import db
from app.utils import common_utils

__author__ = 'lyy'


class FeedBack(db.Model):
    # 反馈记录的id
    id = Column(Integer, primary_key=True, autoincrement=True)
    # 反馈人的uid
    uid = Column(String(50), nullable=False)
    # 反馈的内容
    content = Column(String(50), nullable=False)
    # 反馈人的联系方式
    contact = Column(String(50), nullable=False)
    # 反馈的来源
    origin = Column(Integer, nullable=False)
    # 反馈的时间
    created_time = Column(String(50), nullable=False)

    def __init__(self, uid, content, contact, origin):
        self.uid = uid
        self.content = content
        self.contact = contact
        self.origin = origin
        self.created_time = common_utils.get_date_now()
