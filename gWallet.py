#  -*- coding:utf-8 -*-

from app.app import create_app

app = create_app()


@app.route('/')
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    app.run('10.0.72.91', debug=True)
