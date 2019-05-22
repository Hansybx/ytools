import base64

from aip import AipFace

from app.secure import BAIDU_APP_ID, BAIDU_API_KEY, BAIDU_SECRET_KEY
from app.utils.common_utils import get_file_content

APP_ID = BAIDU_APP_ID
API_KEY = BAIDU_API_KEY
SECRET_KEY = BAIDU_SECRET_KEY

client = AipFace(APP_ID, API_KEY, SECRET_KEY)


def faceIdentity(img):
    image = get_file_content(img)
    image = base64.b64encode(image)
    image64 = str(image, 'utf-8')
    imageType = "BASE64"

    """ 可选参数 """
    options = {}
    options["face_field"] = "age,gender,beauty"
    options["max_face_num"] = 10
    options["face_type"] = "LIVE"
    """ 带参数调用人脸检测 """
    res = client.detect(image64, imageType, options)
    return res


if __name__ == '__main__':
    pass
