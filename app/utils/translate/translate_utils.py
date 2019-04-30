# coding=utf-8
'''
  Created by lyy on 2019-04-30
'''
import hashlib
import random

import requests

from app.secure import BAIDU_TRANSLATE_APP_ID, BAIDU_TRANSLATE_SK

__author__ = 'lyy'


# 翻译的工具方法
def translate_from_baidu(query, language):
    appid = BAIDU_TRANSLATE_APP_ID
    secretKey = BAIDU_TRANSLATE_SK
    salt = str(random.randint(32768, 65536))

    sign = appid + query + salt + secretKey
    m1 = hashlib.md5()
    m1.update(sign.encode("utf8"))
    sign = m1.hexdigest()

    post_url = 'https://fanyi-api.baidu.com/api/trans/vip/translate'
    data = {
        'q': query,
        'from': 'auto',
        'to': language,
        'appid': appid,
        'salt': salt,
        'sign': sign
    }

    r = requests.post(post_url, data)
    return r.json()


if __name__ == '__main__':
    res = translate_from_baidu('苹果', 'en')
    print(res)
