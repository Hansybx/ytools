# coding=utf-8
'''
  Created by lyy on 2019-05-16
'''
import json
import re

import requests

from app.model import db
from app.model.song import Song
from app.utils.common_utils import upload_file_to_qiniu

__author__ = 'lyy'

headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
           'Accept-Encoding': 'gzip, deflate, sdch, br',
           'Accept-Language': 'zh-CN,zh;q=0.8',
           'Connection': 'keep-alive',
           'Host': 'pan.baidu.com',
           'Upgrade-Insecure-Requests': '1',
           'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'}


# 获取字符串中的url
def find_all_url(sentence):
    r = re.compile(
        r'(?i)\b((?:[a-z][\w-]+:(?:/{1,3}|[a-z0-9%])|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:\'".,<>?«»“”‘’]))')
    url_list = r.findall(sentence)
    return url_list[0]


# 从原始url中获取音乐的id
def get_song_id(url):
    id = ''
    try:
        if 'c.y.qq.com' in url:
            res = requests.get(url, headers=headers, allow_redirects=False)
            url = res.headers['location']
            # https://i.y.qq.com/v8/playsong.html?ADTAG=erweimashare&_wv=1&appshare=android_qq&appsongtype=1&appversion=9000007&channelId=10036163&hosteuin=oK6kowEAoK4z7eEzoi4s7K6P7v%2A%2A&openinqqmusic=1&platform=11&songmid=001xd0HI0X9GNq&type=0
            for param in url.split('&'):
                if 'songmid' in param:
                    id = param.replace('songmid=', '')
                    if id is not '':
                        return id
                elif 'songid' in param:
                    songid = param.replace('songid=', '')
                    if songid is not '':
                        temp_url = 'https://c.y.qq.com/v8/fcg-bin/fcg_play_single_song.fcg?songid=' + songid + '&tpl=yqq_song_detail&format=jsonp&callback=getOneSongInfoCallback'
                        temp_res = requests.get(temp_url).text.replace('getOneSongInfoCallback(', '')[0:-1]
                        temp_res = json.loads(temp_res)

                        id = temp_res['data'][0]['mid']
                        return id
            return id

        elif 'i.y.qq.com' in url:
            for param in url.split('&'):
                if 'songid' in param:
                    songid = param.replace('songid=', '')
                    temp_url = 'https://c.y.qq.com/v8/fcg-bin/fcg_play_single_song.fcg?songid=' + songid + '&tpl=yqq_song_detail&format=jsonp&callback=getOneSongInfoCallback'
                    temp_res = requests.get(temp_url).text.replace('getOneSongInfoCallback(', '')[0:-1]
                    temp_res = json.loads(temp_res)
                    id = temp_res['data'][0]['mid']
                elif 'songmid' in param:
                    id = param.replace('songmid=', '')
                if id is not '':
                    return id


        elif 'y.qq.com' in url:
            end_index = url.find('.html')
            id = url[28:end_index].replace('.html', '')
            return id
    except KeyError:
        return None
    return None


# 根据音乐id获取音乐的真实地址
def get_song_url_by_id(id):
    url = "https://v1.itooi.cn/tencent/url?id=" + id + "&quality=128"
    res = requests.get(url, headers=headers, allow_redirects=False)
    return res.headers['location']


# 根据歌曲id获取歌曲图片
def get_song_pic_by_id(id):
    get_pic_url = "https://v1.itooi.cn/tencent/pic?id=" + id
    pic_res = requests.get(get_pic_url, headers=headers, allow_redirects=False)
    song_pic = pic_res.headers['location']
    return song_pic


# 根据歌曲id获取歌曲的名字、作者
def get_song_author_name_by_id(id):
    info_url = "https://v1.itooi.cn/tencent/song?id=" + id

    res = requests.get(info_url, headers=headers, allow_redirects=False)
    res_json = res.json()
    if res_json['code'] == 200:
        data = res_json['data'][0]
        sauthor = data['singer'][0]['name']
        sname = data['title']
        return sauthor, sname


# 从文本获取song对象
def get_song_by_text(text):
    try:
        url = find_all_url(text)[0]
    except IndexError:
        return None

    if len(url) > 0:
        sid = get_song_id(url)
        if sid is not None:
            song = get_song_in_mysql(sid)
            if song is None or song.sid.strip == '':
                try:
                    origin_url = get_song_url_by_id(sid)
                    spic = get_song_pic_by_id(sid)
                    sauthor, sname = get_song_author_name_by_id(sid)
                    download_url = upload_file_to_qiniu(sauthor + '_' + sname + '.m4a', origin_url)

                    song = Song(sid=sid, sname=sname, sauthor=sauthor, spic=spic, origin_url=origin_url,
                                download_url=download_url)
                    put_song_to_mysql(song)
                    return song
                except KeyError:
                    return None
            else:
                return song
        else:
            return None


# 从数据库中获取音乐数据
def get_song_in_mysql(sid):
    song = Song.query.filter(Song.sid == sid).first()
    return song


# 在数据库中新增音乐数据
def put_song_to_mysql(song):
    db.session.add(song)
    db.session.commit()
    return song.sid


if __name__ == '__main__':
    # origin_url, download_url = download_song_by_text("https://c.y.qq.com/base/fcgi-bin/u?__=9Vw3n9")
    # print(origin_url, download_url)

    # id = get_song_id('')
    # song = get_song_by_text(
    #     'https://i.y.qq.com/v8/playsong.html?hosteuin=oKokoK4qoeSF7v**&songid=200470437&songmid=&type=0&platform=1&appsongtype=1&_wv=1&source=qq&appshare=iphone&media_mid=0041DRmt21hZLU&_wv=1')
    # print(song)
    print(get_song_id('https://c.y.qq.com/base/fcgi-bin/u?__=Bcj7Jp'))
    pass
