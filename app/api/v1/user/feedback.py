# coding=utf-8
'''
  Created by lyy on 2019-04-06
'''

__author__ = 'lyy'

import json

from app.model import db
from app.model.feedback import FeedBack
from app.model.res import Res
from app.utils.common_utils import get_date_now
from app.api.v1.user import user
from flask import request, jsonify


@user.route('/feedback/create', methods=['POST'])
def feedback():
    data = request.data
    json_text = json.loads(data)

    # 反馈人的uid
    uid = json_text['uid']
    # 反馈的内容
    content = json_text['content']
    # 反馈人的联系方式
    contact = json_text['contact']
    # 反馈的来源
    origin = json_text['origin']

    feedback = FeedBack(uid, content, contact, origin)

    db.session.add(feedback)
    db.session.commit()

    status = 200
    msg = '反馈成功'
    info = [
        {
            'id': feedback.id,
            'created_time': get_date_now()
        }
    ]

    res_json = Res(status, msg, info)

    return jsonify(res_json.__dict__)
