from flask import jsonify

from app.api.v1.img import img
from app.model.res import Res
from app.utils.one_share.one_share import generatePost


@img.route('/one/share', methods=['POST'])
def one_share():
    img_url = generatePost()

    msg = '保存成功'
    status = 200
    info = [
        {
            'img_url': img_url
        }
    ]

    res_json = Res(status, msg, info)

    return jsonify(res_json.__dict__)