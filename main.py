# coding=utf-8
'''
  Created by lyy on 2019-04-04
'''

__author__ = 'lyy'

from app import create_app

app = create_app()


@app.route('/')
def hello():
    return 'hello,flask'


if __name__ == '__main__':
    app.run(port=8080, debug=app.config['DEBUG'], host='0.0.0.0')
