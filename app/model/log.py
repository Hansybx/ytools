# coding=utf-8
'''
  Created by lyy on 2019-04-30
'''
from sqlalchemy import Column, Integer, String

from app.model import db
from app.utils import common_utils

__author__ = 'lyy'


class Log(db.Model):
    # 表的名字:
    __tablename__ = 'log'

    # 日志记录的id
    id = Column(Integer, primary_key=True, autoincrement=True)
    # 日志人的uid
    uid = Column(String(50), nullable=False)
    # 日志的ip
    ip = Column(String(50), nullable=False)
    country = Column(String(50), nullable=False)
    region = Column(String(50), nullable=False)
    city = Column(String(50), nullable=False)
    isp = Column(String(50), nullable=False)
    created_time = Column(String(50), nullable=False)

    def __init__(self, uid, ip, country, region, city, isp):
        self.uid = uid
        self.ip = ip
        self.country = country
        self.region = region
        self.city = city
        self.isp = isp
        self.created_time = common_utils.get_date_now()
