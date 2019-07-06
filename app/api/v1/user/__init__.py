# coding=utf-8
'''
  Created by lyy on 2019-04-19
'''
from app.model.res import Res
from app.utils.common_utils import get_date_now

__author__ = 'lyy'

from flask import Blueprint, request, jsonify

# 定义一个蓝图
user = Blueprint('user', __name__)

from app.api.v1.user import feedback, logd, login, net_speed


@user.route('/')
def say_hello():
    return '这里是用户处理类的接口'


@user.route('/ip')
def get_ip():
    ip = request.remote_addr
    try:
        _ip = request.headers["X-Real-IP"]
        if _ip is not None:
            ip = _ip
    except Exception as e:
        print(e)

    status = 200

    info = [
        {
            'ip': ip,
            'created_time': get_date_now()
        }
    ]
    msg = 'IP获取成功'

    res_json = Res(status, msg, info)
    return jsonify(res_json.__dict__)
