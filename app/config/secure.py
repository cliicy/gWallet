from pymongo import MongoClient

symbol_list = ['ethusdt', 'btcusdt', 'bchusdt', 'ltcusdt', 'eosusdt', 'ethbtc', 'eosbtc', 'xrpusdt']
period = ['1min', '5min', '15min', '30min', '60min', '4hour', '1day', '1week', '1mon']

mdb = {
    "host": '172.24.132.208',
    # "host": '51facai.51vip.biz',
    "user": 'data',
    "password": 'data123',
    "db": 'invest',
    "port": '27017',
    # "port": '16538',
    "marketP1": 'dw_market',
    "M5": 'dw_M5',
    "M15": 'dw_M15',
    "M30": 'dw_M30',
    "D1": 'dw_D1',
    "H1": 'dw_H1',
    "H4": 'dw_H4',
    "W1": 'dw_W1',
    "M1": 'dw_M1',
    "Y1": 'dw_Y1',
    "MON1": 'dw_MON1',
    "depth": 'dw_depth',
    "api_secret": 'accounts',
    "jgy": 'jgy',
    "coin_logo": 'dw_coin_logo',
    "feixiaohao": 'dw_fxh',
    "future": 'ok_future'
}

mongo_url = 'mongodb://' + mdb["user"] + \
            ':' + mdb["password"] + '@' + mdb["host"] + ':' + \
            mdb["port"] + '/' + mdb["db"]
conn = MongoClient(mongo_url)
sdb = conn[mdb["db"]]
ticker_coll = sdb[mdb["marketP1"]]
ai_news_coll = sdb[mdb["jgy"]]
dwM1_coll = sdb[mdb["M1"]]
dwM5_coll = sdb[mdb["M5"]]
dwD1_coll = sdb[mdb["D1"]]
dwH1_coll = sdb[mdb["H1"]]
dwW1_coll = sdb[mdb["W1"]]
future_kline_coll = sdb[mdb["future"]]
logo_coll = sdb[mdb["coin_logo"]]
fxh_coll = sdb[mdb["feixiaohao"]]
depth_coll = sdb[mdb["depth"]]
keys_coll = sdb[mdb["api_secret"]]


class MonitoringAlarmConfig(object):
    WECHART_FRIENDS = ["15811161256", "大海"]
    WECHART_CHATROOMS = ["兴罗府"]
    EMAIL_FROM_ADDR = "cliicy@hotmail.com"
    EMAIL_PASSWORD = "yingu123"
    EMAIL_CONTACT = ["1294835592@qq.com"]
    EMAIL_SMTP_SERVER = "smtp.163.com"


# 火币配置信息
huobi_setting = {
    # API 请求地址
    'MARKET_URL' : "https://api.huobi.pro",
    'TRADE_URL' : "https://api.huobi.pro",
    # REST API GET请求 header信息
    'GET_HEADERS' : {
        "Content-type": "application/x-www-form-urlencoded",
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/39.0.2171.71 Safari/537.36',
    },
    # REST API POST请求 header信息
    'POST_HEADERS' : {
        "Accept": "application/json",
        'Content-Type': 'application/json'
    },
    'ORDER_PLACE_URL': '/v1/order/orders/place',
}
