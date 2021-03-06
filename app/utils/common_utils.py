# coding=utf-8
'''
  Created by lyy on 2019-04-06
'''

import datetime
import random

from qiniu import Auth, put_file, BucketManager, urlsafe_base64_encode, PersistentFop

from app.setting import BASE_URL

__author__ = 'lyy'


# 获取今天的日期
def get_today():
    return str(datetime.datetime.now().strftime("%Y/%m/%d"))


# 获取当前时间
def get_date_now():
    return str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))


# 用时间生成一个唯一随机数
def get_ran_dom():
    now_time = datetime.datetime.now().strftime("%Y%m%d%H%M%S")  # 生成当前时间
    random_num = random.randint(0, 100)  # 生成的随机整数n，其中0<=n<=100
    if random_num <= 10:
        random_num = str(0) + str(random_num)
    unique_num = str(now_time) + str(random_num)
    return unique_num


# 将生成的文件上传到七牛云
# 传入filename和filepath，返回文件的URL
def upload_file_to_qiniu(filename, filepath):
    from app.secure import QINIU_AK
    from app.secure import QINIU_SK

    access_key = QINIU_AK
    secret_key = QINIU_SK

    auth = Auth(access_key, secret_key)

    # 要上传的空间
    bucket_name = 'ytools'

    # 如果是网络资源直接利用七牛抓取
    if 'http' in filepath:
        bucket_manager = BucketManager(auth)
        ret, info = bucket_manager.fetch(filepath, bucket_name, filename)

        if info.status_code == 200:
            # 如果是m4a格式的就进行转码
            if 'm4a' in filename:
                # 要进行转码的转码操作。
                fops = 'avthumb/mp3/ab/192k'
                # 可以对转码后的文件进行使用saveas参数自定义命名，当然也可以不指定文件会默认命名并保存在当前空间
                saveas_key = urlsafe_base64_encode('ytools:' + filename.replace('m4a', 'mp3'))
                fops = fops + '|saveas/' + saveas_key
                pfop = PersistentFop(auth, bucket_name)
                ops = []
                ops.append(fops)
                ret, info = pfop.execute(filename, ops, 1)
                if ret['persistentId'] is not None:
                    # 转码成功，生成新url
                    filename = filename.replace('m4a', 'mp3')
                    file_url = BASE_URL + filename
                    # # 删除原有文件
                    # ret, info = bucket_manager.delete(bucket_name, filename.replace('mp3', 'm4a'))
                    # print(ret)
                    # print(info)
                    return file_url
        else:
            return False
    # 如果不是网络资源那就自定义路径
    else:
        # 生成上传 Token，可以指定过期时间等
        token = auth.upload_token(bucket_name, filename, 3600)

        ret, info = put_file(token, filename, filepath)

    return BASE_URL + ret['key']


# 获取图片路径
def get_file_content(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()


# 序列化sqlalchemy model
def serialize(model):
    from sqlalchemy.orm import class_mapper
    columns = [c.key for c in class_mapper(model.__class__).columns]
    return dict((c, getattr(model, c)) for c in columns)


if __name__ == '__main__':
    url = upload_file_to_qiniu('test.mp3',
                               'http://mobileoc.music.tc.qq.com/C6000009BCJK1nRaad.m4a?guid=BZQLL&vkey=06835A70D790937C6A2E07FEC692858DAE1B32E76E5871903763323FA38AAEB822B3AFAE8A959FE451C2C71B8C41AC36DECE986FC1695119&uin=0&fromtag=8')
    print(url)
