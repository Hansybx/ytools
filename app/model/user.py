# coding=utf-8
'''
  Created by lyy on 2019-05-12
'''
from sqlalchemy import Column, Integer, String

from app.model import db
from app.utils import common_utils

__author__ = 'lyy'


class User(db.Model):
    # 表的名字:
    __tablename__ = 'users'

    # 日志记录的id
    id = Column(Integer, primary_key=True, autoincrement=True)
    # 日志人的uid
    uid = Column(String(50), nullable=False)
    # 日志的ip
    nickname = Column(String(50), nullable=False)
    avatar_url = Column(String(1000), nullable=False)
    country = Column(String(50), nullable=False)
    province = Column(String(50), nullable=False)
    city = Column(String(50), nullable=False)
    gender = Column(String(50), nullable=False)
    language = Column(String(50), nullable=False)
    created_time = Column(String(100), nullable=False)
    updated_time = Column(String(100), nullable=False)

    def __init__(self, uid, nickname, avatar_url, country, province, city, gender, language):
        self.uid = uid
        self.nickname = nickname
        self.avatar_url = avatar_url
        self.country = country
        self.province = province
        self.city = city
        self.gender = gender
        self.language = language
        self.created_time = common_utils.get_date_now()
        self.updated_time = common_utils.get_date_now()
