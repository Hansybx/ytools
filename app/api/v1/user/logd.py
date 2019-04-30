# coding=utf-8
'''
  Created by lyy on 2019-04-30
'''
import requests

from app.model.log import Log
from app.model.res import Res

__author__ = 'lyy'

from app.model import db

from app.utils.common_utils import get_date_now
from app.api.v1.user import user
from flask import request, jsonify


# 将用户的访问信息存储到数据库中
@user.route('/log/create', methods=['POST'])
def logd():
    uid = request.form['uid']
    ip = request.remote_addr

    ip_info = get_ip_info(ip)['data']
    country = ip_info['country']
    region = ip_info['region']
    city = ip_info['city']
    isp = ip_info['isp']

    log = Log(uid, ip, country, region, city, isp)
    db.session.add(log)
    db.session.commit()

    status = 200
    msg = '记录成功'
    info = [
        {
            'id': log.id,
            'created_time': get_date_now()
        }
    ]

    res_json = Res(status, msg, info)

    return jsonify(res_json.__dict__)


# 获取这个ip地址的详细信息
def get_ip_info(ip):
    url = 'http://ip.taobao.com/service/getIpInfo.php?ip=' + ip
    r = requests.get(url)
    return r.json()
