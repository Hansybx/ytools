# coding=utf-8
'''
  Created by lyy on 2019-05-25
'''

from sqlalchemy import Column, Integer, String

from app.model import db
from app.utils import common_utils

__author__ = 'lyy'


class Face(db.Model):
    # 记录id
    id = Column(Integer, primary_key=True, autoincrement=True)
    # 用户id
    uid = Column(String(64), nullable=False)
    # face图片的url
    face_url = Column(String(1024), nullable=False)
    # face图片的识别结果
    face_age = Column(String(32), nullable=False)
    face_gender = Column(String(32), nullable=False)
    face_beauty = Column(String(32), nullable=False)

    # 记录时间
    created_time = Column(String(64), nullable=False)

    def __init__(self, uid, face_url, face_age, face_gender, face_beauty):
        self.uid = uid
        self.face_url = face_url
        self.face_age = face_age
        self.face_gender = face_gender
        self.face_beauty = face_beauty
        self.created_time = common_utils.get_date_now()
