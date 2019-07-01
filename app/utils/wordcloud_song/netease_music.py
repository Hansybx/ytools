import os
import re
import numpy as np
import requests
import matplotlib.pyplot as plt
from PIL import Image
from app.utils.common_utils import upload_file_to_qiniu
from wordcloud import WordCloud
import jieba

mask_path = os.getcwd()
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


# 根据歌曲id获取歌曲图片
def get_song_pic_by_id(id):
    get_pic_url = "https://v1.itooi.cn/netease/pic?id=" + id
    pic_res = requests.get(get_pic_url, headers=headers, allow_redirects=False)
    song_pic = pic_res.headers['location']
    return song_pic


# 获取歌曲评论
def get_song_comment_by_id(id):
    text = ''
    get_comment_url = "https://v1.itooi.cn/netease/comment/song/hot?id=" + id
    res = requests.get(get_comment_url, headers=headers, allow_redirects=False)
    res = res.json()
    temp = res['data']['hotComments']
    length = temp.__len__()
    for i in range(length):
        text += temp[i]['content'] + '。'
    return text


# jieba分词
def trans_CN(text):
    word_list = jieba.cut(text)
    # 分词后在单独个体之间加上空格
    result = " ".join(word_list)
    return result


# mask图片生成
def mask_create(id):
    mask_url = get_song_pic_by_id(id)
    # response = requests.get(mask_url)
    # image = Image.open(BytesIO(response.content))
    # image.save(path)
    # mask = imread(path.join(d, "mask.jpg"))
    r = requests.get(mask_url)
    with open(mask_path+'/mask.jpg', 'wb') as f:
        f.write(r.content)
    mask_pic = Image.open("mask.jpg")
    mask = np.array(mask_pic)
    return mask


# 词云生成
def draw_wordCloud(text):
    try:
        url = find_all_url(text)[0]
    except IndexError:
        return None

    if len(url) > 0:
        id = get_song_id(url)
    else:
        return None
    text = get_song_comment_by_id(id)
    mask = mask_create(id)
    text = trans_CN(text)
    wordcloud = WordCloud(font_path="simkai.ttf", background_color="white", width=1000,
                          mask=mask, height=860, margin=2).generate(text)

    plt.imshow(wordcloud)
    plt.axis("off")

    wordcloud.to_file('test.jpg')
    img_url = upload_file_to_qiniu('test.jpg', mask_path+'/test.jpg')

    return img_url

if __name__ == "__main__":
    draw_wordCloud('https://music.163.com/#/song?id=1374051000/user/')
