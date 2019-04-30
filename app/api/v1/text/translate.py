# coding=utf-8
'''
  Created by lyy on 2019-04-30
'''

from flask import request, jsonify

from app.api.v1.text import text
from app.model.res import Res
from app.utils.common_utils import get_date_now
from app.utils.translate.translate_utils import translate_from_baidu

__author__ = 'lyy'


# 翻译接口
@text.route('/translate', methods=['POST'])
def translate():
    query = request.form['query']
    language = request.form['language']

    result = translate_from_baidu(query, language)

    status = 200
    msg = '图片生成成功'
    info = [
        {
            'query': query,
            'language': language,
            'result': result["trans_result"],
            'query_time': get_date_now()
        }
    ]

    res_json = Res(status, msg, info)

    return jsonify(res_json.__dict__)
