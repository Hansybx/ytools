# coding=utf-8
'''
  Created by lyy on 2019-04-19
'''
from qiniu import Auth

from app.utils.common_utils import get_ran_dom
from flask import jsonify

__author__ = 'lyy'

from flask import Blueprint

# 定义一个蓝图
img = Blueprint('img', __name__)

from app.api.v1.img import ph_logo, stylize, image_classify, ocr, face, wordcloud_song, one_share


@img.route('/')
def say_hello():
    return '这里是图片处理类的接口'


@img.route('/token/get')
def get_qiniu_token():
    from app.secure import QINIU_AK
    from app.secure import QINIU_SK

    access_key = QINIU_AK
    secret_key = QINIU_SK

    auth = Auth(access_key, secret_key)

    # 要上传的空间
    bucket_name = 'ytools'

    # 上传后保存的文件名
    # key = get_ran_dom() + '.png'
    # 生成上传 Token，可以指定过期时间等
    token = auth.upload_token(bucket_name, None, 3600)
    return jsonify(token)
