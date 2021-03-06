import datetime

from flask import request, jsonify

from app.api.v1.song import song
from app.model.res import Res
from app.utils.common_utils import get_date_now, serialize
from app.utils.download_song.netease_music import get_song_by_text


@song.route('/netease/download', methods=['POST'])
def download_netease_song():
    text = request.form['text']

    start = datetime.datetime.now()

    song = get_song_by_text(text)

    end = datetime.datetime.now()

    if song is not None:
        # if song.id > 0:
        status = 200
        msg = '音乐获取成功'
        info = [
            {
                'text': text,
                'song': serialize(song),
                'created_time': get_date_now(),
                'finish_time': (end - start).seconds
            }
        ]

        res_json = Res(status, msg, info)

        return jsonify(res_json.__dict__)

    else:
        status = 404
        msg = '未找到资源，请联系管理员'
        info = [
            {
                'text': text,
                'song': '',
                'created_time': get_date_now(),
                'finish_time': (end - start).seconds
            }
        ]

        res_json = Res(status, msg, info)

        return jsonify(res_json.__dict__)
