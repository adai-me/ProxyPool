#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Date: 18-12-13

from flask import Flask, request
from config import API_PORT
from util.util_sql import SQLManager

app = Flask(__name__)


@app.route("/")
def index():
    return str(SQLManager().select(50))


@app.route("/get")
def get():
    conditions = {}
    for key, values in request.args.items():
        conditions[key] = values
    return str(SQLManager().select(count=20, conditions=conditions))


@app.route("/get-more/")
def get_more():
    return str(SQLManager().select(100))


@app.route("/delete/<ip>")
@app.route("/delete/ip=<ip>")
def delete(ip):
    if SQLManager().delete(ip):
        return "Delete Success!"
    else:
        return "Delete None!"


@app.route("/refresh/")
def refresh():
    SQLManager().drop()
    SQLManager().create()
    return "Refresh Success!"


@app.route("/readme/")
def readme():
    return """
        "/": 获取IP，以速度与评分排序,<br>
        "/get": 以指定条件获取IP: '?types=1&protocol=1&country=中国&area=北京'<br>
        "/get-more/": 获取100个IP，以速度与评分排序,<br>
        "/delete/<ip>": 删除IP,<br>
        "/delete/ip=<ip>": 删除IP,<br>
        "/refresh/": 删除数据库中所有IP，重新收集,<br>
        "/readme": API说明
    """


def run():
    app.run(port=API_PORT, debug=True)


if __name__ == "__main__":
    run()