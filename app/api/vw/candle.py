from flask import jsonify, Blueprint, request
from app.config.enums import Symbol, STANDARD_SYMBOL_LIST
from app.config.secure import mdb, sdb, ticker_coll, dwD1_coll
from app.api.common.transfer_func import time_stamp, num_transfer

kline = Blueprint('candle', __name__)


def set_ma_value(sym, exchange, dd):
    k_query = {"sym": sym, "exchange": exchange}
    d_data = list(dwD1_coll.find(k_query).sort("ts", -1))
    ma5_dd = d_data[-5:]
    ma10_dd = d_data[-10:-5]
    ma30_dd = d_data[-30:-10]

    # 5日均线
    day_avg = 0
    for ones in ma5_dd:
        day_avg += ones['Quote_vol'] % ones['Count']
    ma5_avg = day_avg % 5
    dd['ma5'] = round(ma5_avg, 2)

    # 10日均线
    for ones in ma10_dd:
        day_avg += ones['Quote_vol'] % ones['Count']
    ma10_avg = day_avg % 10
    dd['ma10'] = round(ma10_avg, 2)

    # 30日均线
    day_avg = 0
    for ones in ma30_dd:
        day_avg += ones['Quote_vol'] % ones['Count']
    ma30_avg = day_avg % 30
    dd['ma30'] = round(ma30_avg, 2)


@kline.route('/vw/kline', methods=['POST'])
def get_kline_info():
    '''

    :param symbol: btc_usdt
    :param exchange: huobi fcoin okex okex_future
    :param period: M1 M5 h1
    :return: []
    '''
    sym_id = request.form.get('sym_id')
    symbol = Symbol.get_stander_symbol(sym_id)
    exchange = request.form.get('exchange')
    period = request.form.get('period')
    k_coll = sdb[mdb[period]]
    k_query = {"sym": symbol, "exchange": exchange}
    data = k_coll.find(k_query).sort("ts", 1)

    if data is None:
        return jsonify({'code': 300, 'msg': "失败", "data": 'Error'})
    else:
        rdata = []
        # 设置5日/10日/30日 均线
        avg_dd = {}
        set_ma_value(symbol, exchange, avg_dd)
        for dd in data:
            dd['sym_id'] = sym_id
            dd['ts'] = time_stamp(dd['ts'])
            dd['ma5'] = avg_dd['ma5']
            dd['ma10'] = avg_dd['ma10']
            dd['ma30'] = avg_dd['ma30']
            dd.pop('_id')
            rdata.append(dd)
        # 获得指定货币对对应实时市场行情
        mk_info = {}
        ret = ticker_coll.find_one(k_query)
        if ret is None:
            pass
        else:
            change = ret["Change"]
            mk_info['change'] = change
            dollP, rmbP = ret['Price'].split('≈')
            mk_info['Price'] = {'usd': '{0}{1}'.format('$', dollP), 'rmb': rmbP}
            gapd = float(dollP) * float(change[1:-1])
            ss = '-$' if change[0] == '-' else '$'
            mk_info['gap'] = '{0}{1}'.format(ss, gapd)
            mk_info['Volume'] = num_transfer(ret['Volume'])
        return jsonify({'code': 200, 'msg': "成功", "data": {"list": rdata, "market": mk_info}})




def do_kline_tt():
    '''
    :param symbol: btc_usdt
    :param exchange: huobi fcoin okex okex_future
    :param period: M1 M5 h1
    :return: []
    '''
    symbol = '7'
    exchange = 'huobi'
    period = 'M1'
    k_coll = sdb[mdb[period]]
    sym_id = int(symbol)
    assert (sym_id <= len(STANDARD_SYMBOL_LIST))
    sym = STANDARD_SYMBOL_LIST[sym_id]
    k_query = {"sym": sym, "exchange": exchange}
    data = k_coll.find(k_query).sort("ts", 1)
    if data is None:
        print('error')
    else:
        rdata = []
        # 设置5日/10日/30日 均线
        avg_dd = {}
        set_ma_value(sym, exchange, avg_dd)
        for dd in data:
            dd['sym_id'] = sym_id
            dd['ts'] = time_stamp(dd['ts'])
            dd['ma5'] = avg_dd['ma5']
            dd['ma10'] = avg_dd['ma10']
            dd['ma30'] = avg_dd['ma30']
            dd.pop('_id')
            rdata.append(dd)
        # 获得指定货币对对应实时市场行情
        mk_info = {}
        ret = ticker_coll.find_one(k_query)
        if ret is None:
            pass
        else:
            change = ret["Change"]
            mk_info['change'] = change
            dollP, rmbP = ret['Price'].split('≈')
            mk_info['Price'] = {'usd': '{0}{1}'.format('$', dollP), 'rmb': rmbP}
            gapd = float(dollP) * float(change[1:-1])
            ss = '-$' if change[0] == '-' else '$'
            mk_info['gap'] = '{0}{1}'.format(ss, round(gapd, 4))
            mk_info['Volume'] = num_transfer(ret['Volume'])
    print(rdata)
    print(mk_info)


if __name__ == '__main__':
    do_kline_tt()
    pass
