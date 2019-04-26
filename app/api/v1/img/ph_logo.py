# coding=utf-8
'''
  Created by lyy on 2019-04-04
'''

__author__ = 'lyy'

from app.utils.common_utils import get_date_now
from flask import request, jsonify

from app.model.res import Res
from app.utils.ph_logo.create_ph_logo import write_text_on_photo
from app.api.v1.img import img


@img.route('/phlogo/hello')
def say_phlogo():
    return 'this is phlogo'


@img.route('/phlogo/create', methods=['POST'])
def make_logo():
    text1 = request.form['text1']
    text2 = request.form['text2']

    img_url = write_text_on_photo(text1, text2)

    status = 200
    msg = '图片生成成功'
    info = [
        {
            'text1': text1,
            'text2': text2,
            'img_url': img_url,
            'created_time': get_date_now()
        }
    ]

    res_json = Res(status, msg, info)

    return jsonify(res_json.__dict__)
