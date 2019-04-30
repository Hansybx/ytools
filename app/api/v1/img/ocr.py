# coding=utf-8
'''
  Created by lyy on 2019-04-30
'''
import datetime
import os

from flask import request, jsonify

from app.api.v1.img import img
from app.model.res import Res
from app.utils.common_utils import get_date_now
from app.utils.ocr.ocr_utils import ocr_by_baidu

__author__ = 'lyy'

path = os.getcwd() + '/app/utils/ocr'


# OCR 文字识别
@img.route('/ocr', methods=['POST'])
def ocr():
    start = datetime.datetime.now()
    img = request.files.get('img')
    save_path = path + '/temp/' + 'ocr.jpg'
    img.save(save_path)

    result = ocr_by_baidu(save_path)

    end = datetime.datetime.now()

    status = 200
    msg = '文字识别成功'
    info = [
        {
            'query_time': get_date_now(),
            'finish_time': (end - start).seconds,
            'result': result
        }
    ]

    res_json = Res(status, msg, info)

    return jsonify(res_json.__dict__)
