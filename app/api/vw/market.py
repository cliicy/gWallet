from flask import jsonify, Blueprint, request
from app.config.enums import Symbol, STANDARD_SYMBOL_LIST
from app.config.secure import ticker_coll, ai_news_coll, logo_coll, fxh_coll, depth_coll, keys_coll
from app.api.common.transfer_func import num_transfer
from app.api.common.transfer_func import time_stamp
from app.api.common.utils import get_keys
from app.api.common.huobi_util import HuobiUtil

market = Blueprint('market', __name__)
logo_list = {}
ip_prefix = 'http://10.0.72.91:5000'


def get_sym_id_log(symbol, dd):
    sym = symbol
    sub_sym = sym.split('/')[0]
    if sub_sym in logo_list:
        dd_sym = logo_list[sub_sym]
        dd['Logo'] = dd_sym['Logo']
        dd['sym_id'] = dd_sym['id']
    if sym in STANDARD_SYMBOL_LIST:
        dd['sym_id'] = Symbol.get_stander_sym_id(sym)


def get_coin_logo():
    if len(logo_list) == 0:
        logo_data = logo_coll.find()
        for ones in logo_data:
            logo_list[ones['sym']] = {'Logo': ones['Logo'], 'id': ones['sym_id']}
    else:
        pass
        # print('pass to get logo')


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


@market.route('/vw/sym_list', methods=['POST'])
def get_symbol_list():
    """
    获取所有可交易的货币对
    :return:
    """
    exchange = request.form.get('exchange')
    k_query = {'exchange': exchange, 'sym': {'$in': STANDARD_SYMBOL_LIST}}
    data = ticker_coll.find(k_query, {'sym': 1, 'exchange': 1})
    if data is None:
        return jsonify({'code: ': 'Error'})
    else:
        ret = {'code': 200, "msg": "成功", "data": {"list": []}}
        count = data.count()
        if count > 0:
            rdata = []
            for dd in data:
                get_sym_id_log(dd['sym'], dd)
                dd.pop('_id')
                rdata.append(dd)
            ret['data']['list'] = rdata
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
                get_sym_id_log(dd['sym'], dd)
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
                get_sym_id_log(dd['sym'], dd)
                dd.pop('_id')
                rdata.append(dd)
            ret['data']['list'] = rdata
        return jsonify(ret)


@market.route('/vw/trade', methods=['POST'])
def get_trade_info():
    """
    交易管理接口 要提供给前端depth的部分信息及账户余额信息
    :return:
    """
    # sym_id = '0'
    # exchange = 'huobi'
    lt_name = request.form.get('limit_name')
    lt_date = request.form.get('limit_date')
    ent_num = request.form.get('num')
    deal_num = request.form.get('deal_num')
    ent_price = request.form.get('ent_price')
    cancel_yn = request.form.get('yn_cancel')
    exchange = request.form.get('exchange')
    sym_id = request.form.get('sym_id')
    symbol = Symbol.get_stander_symbol(sym_id)
    k_query = {"exchange": exchange, "sym": symbol}
    data = depth_coll.find(k_query).sort("ts", -1).limit(5)
    keys_data = keys_coll.find_one({"exchange": exchange})
    key_info = get_keys(keys_data)
    # 获取此账户及其下各个子账户中的所有拥有此币种的所有余额信息
    acc_ret = HuobiUtil().get_account_balance(key_info)
    balance = {}
    if len(acc_ret) > 0:
        balance_list = []
        sym = symbol.split('/')[0].lower()
        for acc in acc_ret:
            balance['status'] = acc['status']
            if acc['status'] == 'ok':
                coin_list = acc['data']['list']
                for info in coin_list:
                    if sym == info['currency']:
                        info['account_id'] = acc['data']['id']
                        info['account_type'] = acc['data']['type']
                        info['state'] = acc['data']['state']
                        balance_list.append(info)
            balance['list'] = balance_list
    else:
        balance['status'] = 'error'
    # print(key_info)
    if data is None:
        return jsonify({'code：': 'Error'})
        # print('Error')
    else:
        ret = {'code': 200, "msg": "成功", "data": {}}
        count = data.count()
        if count > 0:
            get_coin_logo()
            dd_data = {}
            rt = ticker_coll.find_one(k_query)
            if rt is None:
                pass
            else:
                vol_rmb = rt['Volume'].replace(',', '')
                vol_usd = float(vol_rmb[2:])/6.9  # 暂时定为6.9
                vol = num_transfer(vol_rmb)
                vol_usd = num_transfer(str(vol_usd))
                # rmbP = rt['Price'].split('≈')[1]
                # delta = rt["Change"].rstrip('%')
                # change = float(delta)*float(rmbP.replace(' ¥', ''))
                change = rt["Change"]
                dd_data['flag'] = 0 if change[0] == '-' else 1
                dd_data['Vol_RMB'] = vol
                dd_data['Vol_USD'] = vol_usd
                dd_data['Change'] = change
                dd_data['avaiable'] = balance
            buy_data = []
            sell_data = []
            for dd in data:
                get_sym_id_log(symbol, dd)
                dd['delta'] = change
                ts = time_stamp(dd['ts'])
                buy_data.append({'buy_price': str(dd['buy_price']), 'buy_amt': str(dd['buy_amt'])})  # , 'ts': ts
                sell_data.append({'sell_price': str(dd['sell_price']), 'sell_amt': str(dd['sell_amt'])})  # , 'ts': ts
            ret['data'].update(dd_data)
            ret['data']['list_sell_out'] = sell_data
            ret['data']['list_buying'] = buy_data
            ret['data']['list_Limit'] = [{'limit_name': lt_name, 'limit_date': lt_date,
                                          'entrustment_num': ent_num, 'make_deal__num': deal_num,
                                          'entrustment_price': ent_price, 'cancel_orderstate': cancel_yn}]
        return jsonify(ret)
        # print(ret)


@market.route('/vw/depth', methods=['POST'])
def get_depth_info():
    """
    交易管理接口 要提供给前端depth的部分信息及账户余额信息
    :return:
    """
    pass
    # sym_id = '0'
    # exchange = 'huobi'
    # lt_name = request.form.get('limit_name')
    # lt_date = request.form.get('limit_date')
    # ent_num = request.form.get('num')
    # deal_num = request.form.get('deal_num')
    # ent_price = request.form.get('ent_price')
    # cancel_yn = request.form.get('yn_cancel')
    # exchange = request.form.get('exchange')
    # sym_id = request.form.get('sym_id')
    # symbol = Symbol.get_stander_symbol(sym_id)
    # k_query = {"exchange": exchange, "sym": symbol}
    # data = depth_coll.find(k_query).sort("ts", -1).limit(5)
    # keys_data = keys_coll.find_one({"exchange": exchange})
    # key_info = get_keys(keys_data)
    # # 获取此账户及其下各个子账户中的所有拥有此币种的所有余额信息
    # acc_ret = HuobiUtil().get_account_balance(key_info)
    # balance = {}
    # if len(acc_ret) > 0:
    #     balance_list = []
    #     sym = symbol.split('/')[0].lower()
    #     for acc in acc_ret:
    #         balance['status'] = acc['status']
    #         if acc['status'] == 'ok':
    #             coin_list = acc['data']['list']
    #             for info in coin_list:
    #                 if sym == info['currency']:
    #                     balance_list.append(info)
    #         balance['list'] = balance_list
    # else:
    #     balance['status'] = 'error'
    # print(key_info)
    # if data is None:
    #     return jsonify({'code：': 'Error'})
    #     # print('Error')
    # else:
    #     ret = {'code': 200, "msg": "成功", "data": {}}
    #     count = data.count()
    #     if count > 0:
    #         get_coin_logo()
    #         dd_data = {}
    #         rt = ticker_coll.find_one(k_query)
    #         if rt is None:
    #             pass
    #         else:
    #             vol_rmb = rt['Volume'].replace(',', '')
    #             vol_usd = float(vol_rmb[2:])/6.9  # 暂时定为6.9
    #             vol = num_transfer(vol_rmb)
    #             vol_usd = num_transfer(str(vol_usd))
    #             # rmbP = rt['Price'].split('≈')[1]
    #             # delta = rt["Change"].rstrip('%')
    #             # change = float(delta)*float(rmbP.replace(' ¥', ''))
    #             change = rt["Change"]
    #             dd_data['flag'] = 0 if change[0] == '-' else 1
    #             dd_data['Vol_RMB'] = vol
    #             dd_data['Vol_USD'] = vol_usd
    #             dd_data['Change'] = change
    #             # dd_data['avaiable'] = balance
    #         buy_data = []
    #         sell_data = []
    #         for dd in data:
    #             get_sym_id_log(symbol, dd)
    #             dd['delta'] = change
    #             ts = time_stamp(dd['ts'])
    #             buy_data.append({'buy_price': str(dd['buy_price']), 'buy_amt': str(dd['buy_amt'])})  # , 'ts': ts
    #             sell_data.append({'sell_price': str(dd['sell_price']), 'sell_amt': str(dd['sell_amt'])})  # , 'ts': ts
    #         ret['data'].update(dd_data)
    #         ret['data']['list_sell_out'] = sell_data
    #         ret['data']['list_buying'] = buy_data
    #         ret['data']['list_Limit'] = [{'limit_name': lt_name, 'limit_date': lt_date,
    #                                       'entrustment_num': ent_num, 'make_deal__num': deal_num,
    #                                       'entrustment_price': ent_price, 'cancel_orderstate': cancel_yn}]
    #     return jsonify(ret)
        # print(ret)


def do_ticker_test():
    exchange = 'huobi'
    k_query = {'exchange': exchange, 'sym': {'$in': STANDARD_SYMBOL_LIST}}
    # k_query = {'exchange': exchange, 'sym': STANDARD_SYMBOL_LIST}
    data = ticker_coll.find(k_query, {'sym': 1, 'exchange': 1})
    # data = ticker_coll.find(k_query, {'sym': 1, 'exchange': 1})
    if data is None:
        print('Error')
    else:
        ret = {'code': 200, "msg": "成功", "data": {"list": []}}
        count = data.count()
        if count > 0:
            rdata = []
            for dd in data:
                dd.pop('_id')
                # dd.pop('api')
                rdata.append(dd)
            ret['data']['list'] = rdata
        print(ret)


if __name__ == '__main__':
    # data = {"exchange": "huobi", "sym": "btc_usdt", }
    # do_ticker_test()
    # get_market_ai_delta()
    # get_depth_info()
    keys_data = keys_coll.find_one({"exchange": 'huobi'})
    key_info = get_keys(keys_data)
    print(key_info)
    # HuobiUtil().get_accounts(key_info)
    HuobiUtil().get_account_balance(key_info)
    pass
