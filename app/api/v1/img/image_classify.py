# coding=utf-8
'''
  Created by lyy on 2019-04-29
'''
import datetime
import os

from flask import request, jsonify

from app.api.v1.img import img
from app.model.res import Res
from app.utils.common_utils import get_date_now
from app.utils.image_classify.image_classify import animals_classify, plant_classify, car_classify, food_classify

__author__ = 'lyy'

path = os.getcwd() + '/app/utils/image_classify'


# 该文件用来存放所有图像识别的接口

# 识别动物
@img.route('/classify/animal', methods=['POST'])
def animal():
    start = datetime.datetime.now()
    img = request.files.get('img')
    save_path = path + '/temp/' + 'animal.jpg'
    img.save(save_path)

    result = animals_classify(save_path)

    end = datetime.datetime.now()

    status = 200
    msg = '图片识别成功'
    info = [
        {
            'query_time': get_date_now(),
            'finish_time': (end - start).seconds,
            'result': result['result']
        }
    ]

    res_json = Res(status, msg, info)

    return jsonify(res_json.__dict__)


# 识别植物
@img.route('/classify/plant', methods=['POST'])
def plant():
    start = datetime.datetime.now()
    img = request.files.get('img')
    save_path = path + '/temp/' + 'plant.jpg'
    img.save(save_path)

    result = plant_classify(save_path)

    end = datetime.datetime.now()

    status = 200
    msg = '图片识别成功'
    info = [
        {
            'query_time': get_date_now(),
            'finish_time': (end - start).seconds,
            'result': result['result']
        }
    ]

    res_json = Res(status, msg, info)

    return jsonify(res_json.__dict__)


# 识别车辆
@img.route('/classify/car', methods=['POST'])
def car():
    start = datetime.datetime.now()
    img = request.files.get('img')
    save_path = path + '/temp/' + 'car.jpg'
    img.save(save_path)

    result = car_classify(save_path)

    end = datetime.datetime.now()

    status = 200
    msg = '图片识别成功'
    info = [
        {
            'query_time': get_date_now(),
            'finish_time': (end - start).seconds,
            'result': result['result']
        }
    ]

    res_json = Res(status, msg, info)

    return jsonify(res_json.__dict__)


# 识别车辆
@img.route('/classify/food', methods=['POST'])
def food():
    start = datetime.datetime.now()
    img = request.files.get('img')
    save_path = path + '/temp/' + 'food.jpg'
    img.save(save_path)

    result = food_classify(save_path)

    end = datetime.datetime.now()

    status = 200
    msg = '图片识别成功'
    info = [
        {
            'query_time': get_date_now(),
            'finish_time': (end - start).seconds,
            'result': result['result']
        }
    ]

    res_json = Res(status, msg, info)

    return jsonify(res_json.__dict__)
