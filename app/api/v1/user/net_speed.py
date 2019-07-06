from flask import jsonify

from app.api.v1.user import user
from app.model.res import Res
from app.utils.others.net_speed_utils import net_speed_util


@user.route('/net/speed', methods=['POST'])
def net_speed():
    try:
        result = net_speed_util()

        msg = '网速测试成功'
        status = 200
        info = [
            {
                'result': result
            }
        ]
        res_json = Res(status, msg, info)
        return jsonify(res_json.__dict__)
    except Exception as e:
        print(e)