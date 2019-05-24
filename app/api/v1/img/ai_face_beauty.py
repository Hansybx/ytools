import datetime
import os

from flask import request, jsonify

from app.api.v1.img import img
from app.model.res import Res
from app.utils.ai_face_beauty.ai_face_beauty import faceIdentity
from app.utils.common_utils import get_date_now

__author__ = 'lyy'

path = os.getcwd() + '/app/utils/ai_face_beauty'


@img.route('/identify/humanface', methods=['POST'])
def human_face():
    start = datetime.datetime.now()
    img = request.files.get('img')
    save_path = path + '/temp/' + 'face.jpg'
    img.save(save_path)

    result = faceIdentity(save_path)

    if result['error_code'] == 222304 or result['error_code'] == 222204:
        status = 500
        err_msg = '图片过大'
    elif result['error_code'] == 222202:
        status = 500
        err_msg = '没有发现人脸'
    elif result['error_code'] is not 0:
        status = 500
        err_msg = '服务器异常'
    else:
        status = 200
        err_msg = '颜值打分成功'

    msg = err_msg

    end = datetime.datetime.now()

    info = [
        {
            'query_time': get_date_now(),
            'finish_time': (end - start).seconds,
            'result': result
        }
    ]

    res_json = Res(status, msg, info)

    return jsonify(res_json.__dict__)
