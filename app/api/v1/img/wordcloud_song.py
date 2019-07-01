import datetime

from app.api.v1.img import img
from flask import request, jsonify

from app.model.res import Res
from app.utils.common_utils import get_date_now
from app.utils.wordcloud_song.netease_music import draw_wordCloud


@img.route('/wordcloud/netease', methods=['POST'])
def wordcloud_netease():
    start = datetime.datetime.now()

    text = request.form['text']
    img_url = draw_wordCloud(text)

    end = datetime.datetime.now()
    status = 200
    msg = '图片生成成功'
    info = [
        {
            'img_url': img_url,
            'created_time': get_date_now(),
            'finish_time': (end - start).seconds
        }
    ]

    res_json = Res(status, msg, info)

    return jsonify(res_json.__dict__)
