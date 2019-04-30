# coding=utf-8
'''
  Created by lyy on 2019-04-30
'''
from aip import AipOcr

from app.secure import BAIDU_APP_ID, BAIDU_API_KEY, BAIDU_SECRET_KEY
from app.utils.common_utils import get_file_content

__author__ = 'lyy'

APP_ID = BAIDU_APP_ID
API_KEY = BAIDU_API_KEY
SECRET_KEY = BAIDU_SECRET_KEY

client = AipOcr(APP_ID, API_KEY, SECRET_KEY)


def ocr_by_baidu(img):
    image = get_file_content(img)

    """ 调用通用文字识别, 图片参数为本地图片 """
    res = client.basicGeneral(image)
    return res


if __name__ == '__main__':
    res = ocr_by_baidu('temp/ocr.jpg')
    print(res)
