#  -*- coding:utf-8 -*-
from flask import render_template, request
from app.app import create_app

app = create_app()


@app.route("/")
def index():
    return render_template("index.html")


if __name__ == '__main__':
    app.run('10.0.72.91', debug=True)
