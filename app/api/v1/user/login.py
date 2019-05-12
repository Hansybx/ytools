# coding=utf-8
'''
  Created by lyy on 2019-05-12
'''
import json

import requests
from flask import request, jsonify

from app.api.v1.user import user
from app.model import db
from app.model.log import Log
from app.model.res import Res
from app.model.user import User
from app.utils import common_utils
from app.utils.common_utils import get_date_now

__author__ = 'lyy'


# 将用户的访问信息存储到数据库中
@user.route('/login', methods=['POST'])
def user_login():
    data = request.data
    json_text = json.loads(data)

    uid = json_text['openid']
    avatar_url = json_text['avatarUrl']
    city = json_text['city']
    country = json_text['country']
    province = json_text['province']
    gender = json_text['gender']
    language = json_text['language']
    nickname = json_text['nickName']

    ip = request.remote_addr
    try:
        _ip = request.headers["X-Real-IP"]
        if _ip is not None:
            ip = _ip
    except Exception as e:
        print(e)

    add_log(uid, ip)

    if user_exist(uid):
        record_id = update(uid)
        record_msg = '更新成功'
    else:
        user = User(uid, nickname, avatar_url, country, province, city, gender, language)
        record_id = insert(user)
        record_msg = '记录成功'

    status = 200

    info = [
        {
            'id': record_id,
            'created_time': get_date_now()
        }
    ]

    res_json = Res(status, record_msg, info)
    return jsonify(res_json.__dict__)


def add_log(uid, ip):
    ip_info = get_ip_info(ip)['data']
    country = ip_info['country']
    region = ip_info['region']
    city = ip_info['city']
    isp = ip_info['isp']

    log = Log(uid, ip, country, region, city, isp)
    db.session.add(log)
    db.session.commit()


# 判断用户是否存在
def user_exist(uid):
    user = User.query.filter(User.uid == uid).first()
    if user is None or user.uid.strip == '':
        return False
    else:
        return True


# 插入用户数据
def insert(user):
    db.session.add(user)
    db.session.commit()
    return user.id


# 更新数据
def update(uid):
    user = User.query.filter(User.uid == uid).first()
    if user is not None:
        user.updated_time = common_utils.get_date_now()
        db.session.commit()
        return user.id
    else:
        return 0


# 获取这个ip地址的详细信息
def get_ip_info(ip):
    url = 'http://ip.taobao.com/service/getIpInfo.php?ip=' + ip
    r = requests.get(url)
    return r.json()
