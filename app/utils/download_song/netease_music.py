import re

import requests

from app import db
from app.model.song import Song
from app.utils.common_utils import upload_file_to_qiniu

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
    char = re.findall('song[\s\S]', url)
    Jchar = str(char[0])
    if Jchar[-1] == '?':
        id = re.findall('id=(\d*)', url)
        return id[0]
    elif Jchar[-1] == '/':
        id = re.findall('song/(\d*)', url)
        return id[0]


# 根据音乐id获取音乐的真实地址
def get_song_url_by_id(id):
    url = "https://v1.itooi.cn/netease/url?id=" + id + "&quality=flac"
    res = requests.get(url, headers=headers, allow_redirects=False)
    return res.headers['location']


# 根据歌曲id获取歌曲图片
def get_song_pic_by_id(id):
    get_pic_url = "https://v1.itooi.cn/netease/pic?id=" + id
    pic_res = requests.get(get_pic_url, headers=headers, allow_redirects=False)
    song_pic = pic_res.headers['location']
    return song_pic


# 根据歌曲id获取歌曲的名字、作者
def get_song_author_name_by_id(id):
    info_url = "https://v1.itooi.cn/netease/song?id=" + id

    res = requests.get(info_url, headers=headers, allow_redirects=False)
    res_json = res.json()

    if res_json['code'] == 200:
        data = res_json['data']
        sauthor = data['songs'][0]['ar'][0]['name']
        sname = data['songs'][0]['name']
        return sauthor, sname


# 从数据库中获取音乐数据
def get_song_in_mysql(sid):
    song = Song.query.filter(Song.sid == sid).first()
    return song


# 在数据库中新增音乐数据
def put_song_to_mysql(song):
    db.session.add(song)
    db.session.commit()
    return song.sid


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
                    download_url = upload_file_to_qiniu(str(sid) + '.m4a', origin_url)

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


if __name__ == "__main__":
    id = get_song_id('分享弦子的单曲《舍不得》: http://music.163.com/song/306575/?userid=135960009 (来自@网易云音乐)')
    # res = get_song_by_text('http://music.163.com/song/432698825/?userid=377405358 (来自@网易云音乐)')
    url = get_song_url_by_id(id)
    print(url)
