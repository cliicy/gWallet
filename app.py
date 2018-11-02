#  -*- coding:utf-8 -*-
from flask import Flask, jsonify
from config import emongodb as mdb
from pymongo import MongoClient
import time
import pandas as pd

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

details = [
    {
        'id': 'okex',
        'title': u'获取最新行情',
        'description': u'开盘价，收盘价，成交额'
    },
    {
        'id': '币安',
        'title': u'获取最新行情',
        'description': u'开盘价，收盘价，成交额'
    }
]

market = [
    {
        '交易所': 'Fcoin',
        '数字货币': 'BTC',
        '最新价': '$6365.98',
        '涨跌幅': '0.42%',
        '成交量': '约7.4亿'
    },
    {
        '交易所': 'OKEx',
        '数字货币': 'ETH',
        '最新价': '$198.25',
        '涨跌幅': '0.53%',
        '成交量': '约1524万'
    }
]

mongo_url = 'mongodb://' + mdb["user"] + \
            ':' + mdb["password"] + '@' + mdb["host"] + ':' + \
            mdb["port"] + '/' + mdb["db"]
conn = MongoClient(mongo_url)
sdb = conn[mdb["db"]]
coll = sdb[mdb["fcoin"]]


@app.route('/api/ticker', methods=['GET'])
def get_ticker_info():
    while True:
        try:
            ticker = []
            dd = {'ticker': ticker}
            data = pd.DataFrame(list(coll.find()))
            data = data[['sym', 'Change', 'High', 'Low', 'Price', 'Volume']]
            dc = data.set_index('sym').T.to_dict('dict')
            for k, vdata in dc.items():
                tk = {}
                tk['数字货币'] = k
                tk['最新价'] = vdata['Price']
                tk['涨跌幅'] = vdata['Change']
                tk['成交量'] = vdata['Volume']
                tk['24小时内最高价'] = vdata['High']
                tk['24小时内最低价'] = vdata['Low']
                ticker.append(tk)
            # print(data.to_string(index=False))
            return jsonify(dd)
        except Exception as error:
            print(error)
        time.sleep(30)
    # return jsonify(ticker)


@app.route('/api/markets', methods=['GET'])
def get_market_info():
    dd = {'markets': market}
    return jsonify(dd)


@app.route('/api/trades', methods=['GET'])
def get_trades_info():
    dd = {'trades': details}
    return jsonify(dd)


@app.route('/')
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    app.run(debug=True)
