#  -*- coding:utf-8 -*-
from flask import render_template, url_for
from app.app import create_app

app = create_app()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/banner", methods=['GET'])
def banner():
    return render_template("ai_banner.html")


if __name__ == '__main__':
    app.run('10.0.72.91', debug=True)
