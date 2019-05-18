# coding=utf-8
'''
  Created by lyy on 2019-05-17
'''

from sqlalchemy import Column, Integer, String

from app.model import db
from app.utils import common_utils

__author__ = 'lyy'


class Song(db.Model):
    # 表的名字:
    __tablename__ = 'songs'

    # 日志记录的id
    id = Column(Integer, primary_key=True, autoincrement=True)
    # 日志人的uid
    sid = Column(String(100), nullable=False)
    # 日志的ip
    sname = Column(String(100), nullable=False)
    sauthor = Column(String(100), nullable=False)
    spic = Column(String(1000), nullable=False)
    origin_url = Column(String(1000), nullable=False)
    download_url = Column(String(1000), nullable=False)
    created_time = Column(String(100), nullable=False)

    def __init__(self, sid, sname, sauthor, spic, origin_url, download_url):
        self.sid = sid
        self.sname = sname
        self.sauthor = sauthor
        self.spic = spic
        self.origin_url = origin_url
        self.download_url = download_url
        self.created_time = common_utils.get_date_now()
