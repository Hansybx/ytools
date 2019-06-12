# coding=utf-8
'''
  Created by lyy on 2019-04-04
'''
from flask_cors import CORS

__author__ = 'lyy'

from flask import Flask

from app.model import db


def create_app():
    app = Flask(__name__, template_folder='web/templates')
    CORS(app, supports_credentials=True)

    app.config.from_object('app.setting')
    app.config.from_object('app.secure')

    register_blueprint(app)
    init_db(app)
    return app


def register_blueprint(app):
    from app.api.v1 import v1
    from app.api.v1.img import img
    from app.api.v1.user import user
    from app.api.v1.text import text
    from app.api.v1.song import song
    from app.api.v1.others import others

    app.register_blueprint(v1, url_prefix='/api/v1')
    app.register_blueprint(img, url_prefix='/api/v1/img')
    app.register_blueprint(user, url_prefix='/api/v1/user')
    app.register_blueprint(text, url_prefix='/api/v1/text')
    app.register_blueprint(song, url_prefix='/api/v1/song')
    app.register_blueprint(song, url_prefix='/api/v2/others')


def init_db(app):
    # 注册db
    db.init_app(app)
    # 将代码映射到数据库中
    with app.app_context():
        db.create_all(app=app)


if __name__ == '__main__':
    create_app()
