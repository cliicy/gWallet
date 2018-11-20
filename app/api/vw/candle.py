from flask import jsonify, Blueprint, request
from app.config.enums import Symbol
from app.config.secure import mdb, sdb, ticker_coll

kline = Blueprint('candle', __name__)


# @kline.route('/vw/kline/<symbol>/<exchange>/market', methods=['GET'])
# def get_market_info(symbol, exchange):
#     """
#     获取最新市场行情信息
#     :param symbol:
#     :param exchange:
#     :return:
#     """
#     pass


# @kline.route('/vw/kline/<symbol>/<exchange>/<period>', methods=['GET'])
# def get_kline_info(symbol, exchange, period):
@kline.route('/vw/kline/', methods=['POST'])
def get_kline_info():
    '''

    :param symbol: btc_usdt
    :param exchange: huobi fcoin okex okex_future
    :param period: M1 M5 h1
    :return: []
    '''
    symbol = request.form.get('symbol')
    exchange = request.form.get('exchange')
    period = request.form.get('period')
    k_coll = sdb[mdb[period]]
    sym = Symbol.convert_to_stander_sym(symbol)
    k_query = {"sym": sym, "exchange": exchange}
    data = k_coll.find(k_query)
    if data is None:
        return jsonify({'code': 300, 'msg': "失败", "data": 'Error'})
    else:
        rdata = []
        delta_query = {"sym": sym, "exchange": exchange}
        for dd in data:
            dd.pop('_id')
            ret = ticker_coll.find_one(delta_query)
            if ret is None:
                dd['change'] = 'Null'
            else:
                dd['change'] = ret["Change"]
            rdata.append(dd)
        return jsonify({'code': 200, 'msg': "成功", "data": {"list": rdata}})


if __name__ == '__main__':
    delta_query = {"sym": 'BTC/USDT', "exchange": 'huobi'}
    # delta_query = {"sym": 'BTC/USDT', "exchange": 'fcoin'}
    ret = ticker_coll.find_one(delta_query)
    print(ret["Change"])
    # for d in ret:
    #     print(d)

    # pass
    # k_coll = sdb[mdb['H1']]
    # sym = Symbol.convert_to_stander_sym('btc_usdt')
    # k_query = {"sym": sym, "exchange": 'fcoin'}
    # data = k_coll.find(k_query)
    # rdata = []
    # delta_query = {"sym": sym, "exchange": 'fcoin'}
    # for dd in data:
    #     dd.pop('_id')
    #     ret = ticker_coll.find(delta_query)
    #     for d in ret:
    #         print(d)
    #     if ret.count() > 0:
    #         dd['change'] = ret.Change
    #     rdata.append(dd)
    # print(rdata)
