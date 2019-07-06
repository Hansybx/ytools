import os

from bs4 import BeautifulSoup
from lxml import html
import xml
import requests

_path = os.getcwd()


# 下载图片函数
def download_img(url, name):
    """"
    下载指定url的图片
    url：图片的url；
    name:保存图片的名字
    """
    try:
        respone = requests.get(url)
        f_img = respone.content
        path = _path + name + '.jpg'
        with open(path, "wb")as f:
            f.write(f_img)
    except Exception as e:
        print("---------地址出错------------")


url_list = []

f = requests.get("http://wufazhuce.com/")

# #打印网页内容
# print(f.content.decode())

soup = BeautifulSoup(f.content, "lxml")

try:
    first_div = soup.find("div", attrs={'id': 'main-container'}).find('div', attrs={'class': 'carousel-inner'})
    a_all = first_div.find_all('a')

    for i in a_all:
        url_list.append(i.attrs['href'])

except Exception as e:
    print("---------出错------------")

# 得到one的首页推荐页面
f_1 = requests.get(url_list[0])

# 打印网页内容
# print(f_1.content.decode())

soup_1 = BeautifulSoup(f_1.content, "lxml")

try:
    second_div = soup_1.find("div", attrs={'id': 'main-container'}).find('div', attrs={'class': 'one-cita-wrapper'})
    third_div = soup_1.find("div", attrs={'id': 'main-container'}).find('div', attrs={'class': 'one-imagen'})

    # 获得时期值
    now_month = second_div.find('p', attrs={'class': 'may'}).text
    now_one_day = second_div.find('p', attrs={'class': 'dom'}).text

    # 获得图片的url
    img_url = third_div.find('img').attrs['src']

    # 获得一段话并去除开头的空格
    one_text = second_div.find("div", attrs={'class': 'one-cita'}).text.strip()

    # 将获得日期拼接
    now_day = now_one_day + ' ' + now_month

    # 调用函数下载图片

    download_img(img_url, now_day)

except Exception as e:
    print("---------出错------------")


