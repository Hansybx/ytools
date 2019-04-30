# coding=utf-8
'''
  Created by lyy on 2019-04-06
'''
from flask_sqlalchemy import SQLAlchemy

__author__ = 'lyy'

db = SQLAlchemy()

from app.model import feedback,log