# coding=utf-8
'''
  Created by lyy on 2019-04-04
'''
from PIL import Image, ImageFont, ImageDraw

from app.utils.common_utils import upload_pic_to_qiniu, get_ran_dom

import os

__author__ = 'lyy'

path = os.getcwd()+'/app/utils/ph_logo'

# 在背景图片上写字
def write_text_on_photo(text1, text2):
    # 获取背景图片
    img = Image.open(path + '/assets/bg.jpg')
    # 获取字体,第一个参数为字体路径，第二个为字体大小
    font = ImageFont.truetype(path + '/assets/songti.otf', 150)
    # 获取绘图对象
    draw = ImageDraw.Draw(img)

    textWidth1, textHeight1 = font.getsize(text1)
    textWidth2, textHeight2 = font.getsize(text2)

    # text1 的起始坐标
    text1_w = (1550 - textWidth1 - textWidth2) / 2
    text1_h = int((800 - textHeight1) / 2.2)

    # text2 的起始坐标
    text2_w = text1_w + textWidth1 + 50
    text2_h = int((800 - textHeight1) / 2.2)

    draw.text([text1_w, text1_h], text1, font=font)

    drawRoundRec(img, (242, 157, 56), text2_w - 25, text2_h, textWidth2 + 50, textHeight2 + 40, 20)

    draw.text([text2_w, text2_h], text2, font=font, fill=(0, 0, 0, 0))

    img.save(path + '/output/ph_logo.jpg', 'jpeg')

    filename = str(text1 + '_' + text2 + '_' + get_ran_dom() + '.jpg').lower()
    filepath = path + '/output/ph_logo.jpg'

    img_url = upload_pic_to_qiniu(filename, filepath)

    return img_url


# 给背景图片添加圆角背景
def drawRoundRec(img, color, x, y, w, h, r):
    drawObject = ImageDraw.Draw(img)

    '''Rounds'''
    drawObject.ellipse((x, y, x + r, y + r), fill=color)
    drawObject.ellipse((x + w - r, y, x + w, y + r), fill=color)
    drawObject.ellipse((x, y + h - r, x + r, y + h), fill=color)
    drawObject.ellipse((x + w - r, y + h - r, x + w, y + h), fill=color)

    '''rec.s'''
    drawObject.rectangle((x + r / 2, y, x + w - (r / 2), y + h), fill=color)
    drawObject.rectangle((x, y + r / 2, x + w, y + h - (r / 2)), fill=color)


if __name__ == '__main__':
    write_text_on_photo('Cool', 'Kid')
