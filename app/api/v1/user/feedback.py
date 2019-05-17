# coding=utf-8
'''
  Created by lyy on 2019-04-06
'''

import json
from threading import Thread

from flask import request, jsonify
from flask_mail import Mail, Message
from flask_script import Manager

from app.api.v1.user import user
from app.model import db
from app.model.feedback import FeedBack
from app.model.res import Res
from app.utils.common_utils import get_date_now
from main import app

__author__ = 'lyy'

manager = Manager(app)
mail = Mail(app)


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

    # 如果反馈成功，异步发送邮件
    if feedback.id > 0:
        send_email(app, feedback)

    res_json = Res(status, msg, info)

    return jsonify(res_json.__dict__)


def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)


# 发送邮件
def send_email(app, feedback):
    msg = Message('开挂(ytools)', sender='420326369@qq.com',
                  recipients=['yueyong1030@outlook.com', '152210702112@stu.just.edu.cn'])
    msg.body = str(
        '反馈id：' + str(feedback.id) + '\n反馈内容：' + str(feedback.content) + '\n反馈用户id：' + str(
            feedback.uid) + '\n反馈来源：' + str(feedback.origin) + '\n联系方式：' + str(feedback.contact) + '\n反馈时间：' + str(
            feedback.created_time))

    thr = Thread(target=send_async_email, args=[app, msg])
    thr.start()
    return 'ok'
