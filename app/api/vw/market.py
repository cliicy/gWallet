from flask import jsonify, Blueprint, request
from app.config.enums import Symbol, STANDARD_SYMBOL_LIST
from app.config.secure import ticker_coll, ai_news_coll, logo_coll, fxh_coll
from app.api.common.transfer_func import num_transfer

market = Blueprint('market', __name__)
logo_list = {}
ip_prefix = 'http://10.0.72.91:5000'


def get_coin_logo():
    if len(logo_list) == 0:
        logo_data = logo_coll.find()
        for ones in logo_data:
            logo_list[ones['sym']] = {'Logo': ones['Logo'], 'id': ones['sym_id']}
    else:
        print('pass to get logo')


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


@market.route('/vw/ai/banner', methods=['POST'])
def get_banner_info():
    """
    AI（banner,AI大数据预测，市场强弱）
    :return:
    """
    ret = {'code': 200, 'msg': '成功', 'data': {'banners': {'imgUrl': {}, 'pageRoute': {},
                                                          'routeData': []}}}
    rdata = {}
    rdata['platform'] = ip_prefix + '/static/images/banner1@2x.png'
    rdata['newbie'] = ip_prefix + '/static/images/banner2@2x.png'
    rdata['vw_news'] = ip_prefix + '/static/images/banner3@2x.png'
    rdata['master'] = ip_prefix + '/static/images/banner4@2x.png'
    ret['data']['banners']['imgUrl'] = rdata
    return jsonify(ret)


@market.route('/vw/market/ex_list', methods=['POST'])
def get_exchange_list():
    """
    获取所有可选交易所
    :return:
    """
    data = fxh_coll.find()
    if data is None:
        return jsonify({'code: ': 'Error'})
    else:
        ret = {'code': 200, "msg": "成功", "data": {"list": []}}
        count = data.count()
        if count > 0:
            rdata = []
            for dd in data:
                dd.pop('_id')
                dd.pop('api')
                rdata.append(dd)
            ret['data']['list'] = rdata
        return jsonify(ret)


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


@market.route('/vw/market/ai_delta', methods=['POST'])
def get_market_ai_delta():
    exchange = request.form.get('exchange')
    delta = request.form.get('delta')
    k_query = {'exchange': exchange}
    if delta == '1':
        k_query['Change'] = {"$regex": "^[+0-9]"}
    elif delta == '0':
        k_query['Change'] = {"$regex": "^-"}
    print(k_query)
    data = ticker_coll.find(k_query)
    if data is None:
        return jsonify({'code: ': 'Error'})
    else:
        ret = {'code': 200, "msg": "成功", "data": {"list": []}}
        count = data.count()
        if count > 0:
            get_coin_logo()
            rdata = []
            for dd in data:
                dollP, rmbP = dd['Price'].split('≈')
                dd['Price'] = {'usd': '{0}{1}'.format('$', dollP), 'rmb': rmbP}
                dd['pDollar'] = '{0}{1}'.format('$', dollP)
                dd['pRMB'] = rmbP
                # Volume换算成亿万单位
                dd['Volume'] = num_transfer(dd['Volume'])
                sym = dd['sym']
                sub_sym = sym.split('/')[0]
                if sub_sym in logo_list:
                    dd_sym = logo_list[sub_sym]
                    dd['sym_id'] = dd_sym['id']
                if sym in STANDARD_SYMBOL_LIST:
                    dd['sym_id'] = Symbol.get_stander_sym_id(sym)
                dd.pop('_id')
                dd.pop('High')
                dd.pop('Low')
                dd.pop('api')
                dd.pop('exchange')
                dd.pop('gearing')
                dd.pop('Price')
                dd.pop('amount')
                rdata.append(dd)
            ret['data']['list'] = rdata
        return jsonify(ret)


@market.route('/vw/market', methods=['POST'])
def get_market_info():
    exchange = request.form.get('exchange')
    k_query = {"exchange": exchange}
    data = ticker_coll.find(k_query)
    if data is None:
        return jsonify({'code：': 'Error'})
    else:
        ret = {'code': 200, "msg": "成功", "data": {"list": []}}
        count = data.count()
        if count > 0:
            get_coin_logo()
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
                sym = dd['sym']
                sub_sym = sym.split('/')[0]
                if sub_sym in logo_list:
                    dd_sym = logo_list[sub_sym]
                    dd['Logo'] = dd_sym['Logo']
                    dd['sym_id'] = dd_sym['id']
                if sym in STANDARD_SYMBOL_LIST:
                    dd['sym_id'] = Symbol.get_stander_sym_id(sym)
                dd.pop('_id')
                rdata.append(dd)
            ret['data']['list'] = rdata
        return jsonify(ret)


def do_ticker_test():
    k_query = {"exchange": 'huobi'}
    data = ticker_coll.find(k_query)
    if data is None:
        print('Error')
    else:
        get_coin_logo()
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
            sym = dd['sym']
            sub_sym = sym.split('/')[0]
            if sub_sym in logo_list:
                dd_sym = logo_list[sub_sym]
                dd['Logo'] = dd_sym['Logo']
            if sym in STANDARD_SYMBOL_LIST:
                dd['sym_id'] = Symbol.get_stander_sym_id(sym)
            else:
                dd['sym_id'] = dd_sym['id']
            dd.pop('_id')
            rdata.append(dd)
    print(rdata)


if __name__ == '__main__':
    # data = {"exchange": "huobi", "sym": "btc_usdt", }
    # do_ticker_test()
    get_market_ai_delta()
    pass
