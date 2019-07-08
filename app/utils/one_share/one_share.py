import datetime
import os
import textwrap

from PIL import ImageDraw, Image, ImageFont
from bs4 import BeautifulSoup
from lxml import html
import xml
import requests

from app.utils.common_utils import upload_file_to_qiniu

# _path0 = os.getcwd()
_path0 = 'C:/Users/handsomeyuan/Desktop/flask/ytools-server'
_path = _path0 + '/assets'

_path1 = _path0 + '/output'


# 下载图片函数
def download_img(url):
    """"
    下载指定url的图片
    url：图片的url；
    name:保存图片的名字
    """
    try:
        respone = requests.get(url)
        f_img = respone.content
        path = _path0 + '/app/utils/one_share/assets/base.jpg'
        with open(path, "wb")as f:
            f.write(f_img)
    except Exception as e:
        raise e


# 获取图片及其相关信息
def img_info_spider():
    url_list = []

    f = requests.get("http://wufazhuce.com/")

    soup = BeautifulSoup(f.content, "lxml")

    try:
        first_div = soup.find("div", attrs={'id': 'main-container'}).find('div', attrs={'class': 'carousel-inner'})
        a_all = first_div.find_all('a')

        for i in a_all:
            url_list.append(i.attrs['href'])

    except Exception as e:
        raise e

    # 得到one的首页推荐页面
    f_1 = requests.get(url_list[0])

    soup_1 = BeautifulSoup(f_1.content, "lxml")

    try:
        second_div = soup_1.find("div", attrs={'id': 'main-container'}).find('div', attrs={'class': 'one-cita-wrapper'})
        third_div = soup_1.find("div", attrs={'id': 'main-container'}).find('div', attrs={'class': 'one-imagen'})

        # 获得时期值
        # now_month = second_div.find('p', attrs={'class': 'may'}).text
        # now_one_day = second_div.find('p', attrs={'class': 'dom'}).text

        # 获得图片的url
        img_url = third_div.find('img').attrs['src']

        # 获得一段话并去除开头的空格
        one_text = second_div.find("div", attrs={'class': 'one-cita'}).text.strip()

        # # 将获得日期拼接
        # now_day = now_one_day + ' ' + now_month

        # 调用函数下载图片
        download_img(img_url)
        return one_text
    except Exception as e:
        raise e


class postMaker(object):
    def __init__(self, backImg, font):
        self.backImg = backImg
        self.font = font
        self.post = None

    def create(self, postPic, postTitle, qrImg, textColor):
        """
        @postPic: 文章封面图
        @postTitle 文章标题
        @qrImg: 文章二维码
        @textColor: 文字颜色，{R，G，B}
        """
        try:
            # 获取背景图
            backImg = Image.open(self.backImg)
            # 获取封面图
            postPic = Image.open(postPic)
            # 获取字体
            font = ImageFont.truetype(self.font, 30, encoding="utf-8")

            # postPic.thumbnail((600, 600))

            bg_w, bg_h = backImg.size
            pic_w, pic_h = postPic.size

            # 文字换行设置
            astr = postTitle

            para = textwrap.wrap(astr, width=15)

            # 将封面图粘贴到背景图的指定位置，第二个参数为坐标
            backImg.paste(postPic, (0, 0, pic_w, pic_h))

            draw = ImageDraw.Draw(backImg)
            draw.ink = textColor.get(
                'R', 0) + textColor.get('G', 0) * 256 + textColor.get('B', 1) * 256 * 256
            textWidth, textHeight = font.getsize(postTitle)

            h = 510
            for postTitle in para:
                draw.text([pic_w - textWidth / 2, h], postTitle, font=font)
                h += textHeight
            qrImg = Image.open(qrImg)
            qrImg.thumbnail((150, 150))
            backImg.paste(qrImg, (bg_w-150, bg_h-150))

            self.post = backImg

            # today = datetime.date.today()
            # folder_path = 'output/' + str(today)

            backImg.save(_path0 + '/app/utils/one_share/output/one_post.jpg')
        except Exception as e:
            raise e


# 生成海报
def generatePost():
    # today = datetime.date.today()
    # folder_path = 'output/' + str(today)
    title = img_info_spider()
    backImg = _path0 + '/app/utils/one_share/assets/backImg.png'
    font = _path0 + '/app/utils/one_share/assets/simkai.ttf'
    pMaker = postMaker(backImg=backImg, font=font)
    postPic = _path0 + '/app/utils/one_share/assets/base.jpg'

    qrImg = _path0 + '/app/utils/one_share/assets/wxapp.jpg'
    pMaker.create(
        postPic=postPic,
        postTitle=title,
        qrImg=qrImg,
        textColor={'R': 0, 'G': 0, 'B': 0})
    today = datetime.date.today()
    img_url = upload_file_to_qiniu(str(today)+'one_share.jpg', _path0 + '/app/utils/one_share/output/one_post.jpg')
    return img_url

print(generatePost())