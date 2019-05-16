# coding=utf-8
'''
  Created by lyy on 2019-05-16
'''
import datetime

from flask import request, jsonify

from app.api.v1.song import song
from app.model.res import Res
from app.utils.common_utils import get_date_now
from app.utils.download_song.song_utils import download_song_by_text

__author__ = 'lyy'


@song.route('/hello')
def say_song():
    return 'this is song'


@song.route('/qq/download', methods=['POST'])
def download_qq_song():
    text = request.form['text']

    start = datetime.datetime.now()

    origin_url, download_url = download_song_by_text(text)

    end = datetime.datetime.now()

    status = 200
    msg = '音乐获取成功'
    info = [
        {
            'text': text,
            'origin_url': origin_url,
            'download_url': download_url,
            'created_time': get_date_now(),
            'finish_time': (end - start).seconds
        }
    ]

    res_json = Res(status, msg, info)

    return jsonify(res_json.__dict__)
