import datetime
import json
import os
from concurrent.futures import ThreadPoolExecutor

from flask import request, jsonify

from app import create_app
from app.api.v1.img import img
from app.model import db
from app.model.face import Face
from app.model.res import Res
from app.utils.ai_face_beauty.ai_face_beauty import faceIdentity
from app.utils.common_utils import get_date_now, upload_file_to_qiniu, get_ran_dom

__author__ = 'lyy'

path = os.getcwd() + '/app/utils/ai_face_beauty'

executor = ThreadPoolExecutor(1)


# 保存人脸信息
def save_face(uid, filepath, face_age, face_gender, face_beauty):
    filename = str('face_' + get_ran_dom() + '.jpg').lower()
    face_url = upload_file_to_qiniu(filename, filepath)
    face = Face(uid, face_url, face_age, face_gender, face_beauty)
    try:
        app = create_app()
        with app.app_context():
            db.session.add(face)
            db.session.commit()
    except Exception as e:
        print(e)


# 测颜值
@img.route('/face/mark', methods=['POST'])
def face_mark():
    start = datetime.datetime.now()
    uid = request.form['uid']
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

    # 如果识别成功，就将人脸信息保存到数据库中(异步)
    if status == 200:
        result = result['result']
        face_age = result['face_list'][0]['age']
        face_gender = result['face_list'][0]['gender']['type']
        face_beauty = result['face_list'][0]['beauty']
        # save_face(uid, save_path, face_age, face_gender, face_beauty)
        executor.submit(save_face, uid, save_path, face_age, face_gender, face_beauty)

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


# 返回一定数量的人脸数据
@img.route('/face/get')
def get_face():
    page = request.args.get("page", default=1, type=int)

    faces = get_face_by_page(page)
    info = {
        'query_time': get_date_now(),
        'result': to_json(faces)
    }
    status = 200
    msg = '获取成功'
    res_json = Res(status, msg, info)
    return jsonify(res_json.__dict__)


# 配合多个对象使用的函数
def to_json(all_vendors):
    v = [ven.dobule_to_dict() for ven in all_vendors]
    return v


# 根据page获取人脸数据
def get_face_by_page(page):
    index = [i for i in range(page * 20 - 19, page * 20)]
    faces = Face.query.filter(Face.id.in_(index)).all()
    return faces


# 即将舍弃
@img.route('/identify/humanface', methods=['POST'])
def human_face():
    start = datetime.datetime.now()
    uid = request.form['uid']
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

    # 如果识别成功，就将人脸信息保存到数据库中(异步)
    if status == 200:
        result = result['result']
        face_age = result['face_list'][0]['age']
        face_gender = result['face_list'][0]['gender']['type']
        face_beauty = result['face_list'][0]['beauty']
        # save_face(uid, save_path, face_age, face_gender, face_beauty)
        executor.submit(save_face, uid, save_path, face_age, face_gender, face_beauty)

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
