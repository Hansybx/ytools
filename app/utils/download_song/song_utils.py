# coding=utf-8
'''
  Created by lyy on 2019-05-16
'''
import json
import re

import requests

from app.utils.common_utils import upload_file_to_qiniu, get_ran_dom

__author__ = 'lyy'


# 获取字符串中的url
def find_all_url(sentence):
    r = re.compile(
        r'(?i)\b((?:[a-z][\w-]+:(?:/{1,3}|[a-z0-9%])|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:\'".,<>?«»“”‘’]))')
    url_list = r.findall(sentence)
    return url_list[0]


# 从原始url中获取音乐的id
def get_song_id(url):
    id = ''
    if 'c.y.qq.com' in url:
        headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                   'Accept-Encoding': 'gzip, deflate, sdch, br',
                   'Accept-Language': 'zh-CN,zh;q=0.8',
                   'Connection': 'keep-alive',
                   'Host': 'pan.baidu.com',
                   'Upgrade-Insecure-Requests': '1',
                   'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'}
        res = requests.get(url, headers=headers, allow_redirects=False)
        url = res.headers['location']
        # https://i.y.qq.com/v8/playsong.html?ADTAG=erweimashare&_wv=1&appshare=android_qq&appsongtype=1&appversion=9000007&channelId=10036163&hosteuin=oK6kowEAoK4z7eEzoi4s7K6P7v%2A%2A&openinqqmusic=1&platform=11&songmid=001xd0HI0X9GNq&type=0
        for param in url.split('&'):
            if 'songmid' in param:
                id = param.replace('songmid=', '')
            elif 'songid' in param:
                songid = param.replace('songid=', '')
                temp_url = 'https://c.y.qq.com/v8/fcg-bin/fcg_play_single_song.fcg?songid=' + songid + '&tpl=yqq_song_detail&format=jsonp&callback=getOneSongInfoCallback'
                temp_res = requests.get(temp_url).text.replace('getOneSongInfoCallback(', '')[0:-1]
                temp_res = json.loads(temp_res)
                id = temp_res['data'][0]['mid']
        return id


    elif 'y.qq.com' in url:
        end_index = url.find('.html')
        id = url[28:end_index].replace('.html', '')
        return id
    return 'url异常'


# 根据音乐id获取音乐的真实地址
def get_song_url_by_id(id):
    url = "https://v1.itooi.cn/tencent/url?id=" + id + "&quality=128"
    headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
               'Accept-Encoding': 'gzip, deflate, sdch, br',
               'Accept-Language': 'zh-CN,zh;q=0.8',
               'Connection': 'keep-alive',
               'Host': 'pan.baidu.com',
               'Upgrade-Insecure-Requests': '1',
               'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'}
    res = requests.get(url, headers=headers, allow_redirects=False)
    return res.headers['location']


# 根据传递来的字符串返回音乐原始url
def get_song_url_by_text(text):
    res_url = []
    urls = find_all_url(text)
    for url in urls:
        if len(url) > 0:
            id = get_song_id(url)
            song_url = get_song_url_by_id(id)
            res_url.append(song_url)

    return res_url[0]


# 根据url把歌曲下载到本地
def download_song_by_text(text):
    origin_url = get_song_url_by_text(text)

    filename = str(get_ran_dom() + '.mp3').lower()
    download_url = upload_file_to_qiniu(filename, origin_url)

    return origin_url, download_url


if __name__ == '__main__':
    # origin_url, download_url = download_song_by_text("https://c.y.qq.com/base/fcgi-bin/u?__=9Vw3n9")
    # print(origin_url, download_url)
    id = get_song_id('https://c.y.qq.com/base/fcgi-bin/u?__=9Vw3n9')
    print(id)
