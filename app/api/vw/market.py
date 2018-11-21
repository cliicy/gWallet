from flask import jsonify, Blueprint, request
from app.config.enums import Symbol, STANDARD_SYMBOL_LIST
from app.config.secure import ticker_coll, ai_news_coll
from app.api.common.transfer_func import num_transfer

# info = [
#     {
#         '交易所': 'Fcoin',
#         '数字货币': 'BTC',
#         '最新价': '$6365.98',
#         '涨跌幅': '0.42%',
#         '成交量': '约7.4亿'
#     },
#     {
#         '交易所': 'OKEx',
#         '数字货币': 'ETH',
#         '最新价': '$198.25',
#         '涨跌幅': '0.53%',
#         '成交量': '约1524万'
#     }
# ]

market = Blueprint('market', __name__)


@market.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')
        if username == "luoluo" and password == "1234":
            return "<h1>welcome, %s !</h1>" %username
        else:
            return "<h1>login Failure !</h1>"
    else:
        return "<h1>login Failure !</h1>"


@market.route('/vw/market/ai/news', methods=['POST'])
def get_ai_news():
    """
    -------------------------资讯
    :return:
    """
    data = ai_news_coll.find()
    if data is None:
        return jsonify({'code: ': 'Error'})
    else:
        rdata = []
        for dd in data:
            dd.pop('_id')
            rdata.append(dd)
        return jsonify({'code': 200, "msg": "成功", "data": {"list": rdata}})


@market.route('/vw/market', methods=['POST'])
def get_market_info():
    exchange = request.form.get('exchange')
    k_query = {"exchange": exchange}
    data = ticker_coll.find(k_query)
    if data is None:
        return jsonify({'code：': 'Error'})
    else:
        rdata = []
        for dd in data:
            doll_L, rmb_L = dd['Low'].split('≈')
            dd['Low'] = {'usd': '{0}{1}'.format('$', doll_L), 'rmb': rmb_L}
            dollH, rmbH = dd['High'].split('≈')
            dd['High'] = {'usd': '{0}{1}'.format('$', dollH), 'rmb': rmbH}
            dollP, rmbP = dd['Price'].split('≈')
            dd['Price'] = {'usd': '{0}{1}'.format('$', dollP), 'rmb': rmbP}
            # Volume换算成亿万单位
            dd['Volume'] = num_transfer(dd['Volume'])

            sym_id = 'Null'
            sym = dd['sym']
            if sym in STANDARD_SYMBOL_LIST:
                sym_id = Symbol.get_stander_sym_id(sym)
            dd['sym_id'] = sym_id
            sub_sym = sym.split('/')
            dd['Logo'] = '{0}{1}'.format(sub_sym[0].lower(), '.png')
            dd.pop('_id')
            rdata.append(dd)
        return jsonify({'code': 200, "msg": "成功", "data": {"list": rdata}})
    return jsonify(dd)


def do_ticker_test():
    k_query = {"exchange": 'huobi'}
    data = ticker_coll.find(k_query)
    if data is None:
        print('error')
    else:
        rdata = []
        for dd in data:
            doll_L, rmb_L = dd['Low'].split('≈')
            dd['Low'] = {'usd': '{0}{1}'.format('$', doll_L), 'rmb': rmb_L}
            dollH, rmbH = dd['High'].split('≈')
            dd['High'] = {'usd': '{0}{1}'.format('$', dollH), 'rmb': rmbH}
            dollP, rmbP = dd['Price'].split('≈')
            dd['Price'] = {'usd': '{0}{1}'.format('$', dollP), 'rmb': rmbP}
            # Volume换算成亿万单位
            sdd = dd['Volume'].replace(',', '')
            sdd = sdd.replace('¥ ', '')
            # print(sdd)
            yi_dd = float(sdd) * 0.00000001
            wan_dd = float(sdd) * 0.0001
            if yi_dd > 1:
                dd['Volume'] = '{0}{1}'.format(round(yi_dd, 1), '亿')
            elif wan_dd > 1:
                dd['Volume'] = '{0}{1}'.format(round(wan_dd, 1), '万')
            else:
                pass
            dd['Logo'] = 'huobi.jpg'
            sym_id = 'Null'
            sym = dd['sym']
            if sym in STANDARD_SYMBOL_LIST:
                sym_id = Symbol.get_stander_sym_id(sym)
            dd['sym_id'] = sym_id
            dd.pop('_id')
            rdata.append(dd)
    print(rdata)


if __name__ == '__main__':
    # data = {"exchange": "huobi", "sym": "btc_usdt", }
    do_ticker_test()
    pass
