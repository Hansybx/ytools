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
    image = request.files.get('img')
    save_path = path + '/temp/' + 'face.jpg'
    image.save(save_path)

    result = faceIdentity(save_path)

    end = datetime.datetime.now()

    try:
        status = 200
        msg = '颜值打分成功'
        info = [
            {
                'query_time': get_date_now(),
                'finish_time': (end - start).seconds,
                'result': result['result']['face_list'][0]['beauty']
            }
        ]
    except KeyError:
        status = 500
        msg = '颜值打分失败'
        info = [
            {
                'query_time': get_date_now(),
                'finish_time': (end - start).seconds,
                'result': []
            }
        ]

    res_json = Res(status, msg, info)

    return jsonify(res_json.__dict__)