from flask import jsonify, Blueprint, request
from app.config.enums import Symbol, STANDARD_SYMBOL_LIST, WALLET_SYMBOL, EXCHANGE_LIST
from app.config.secure import ticker_coll, ai_news_coll, logo_coll, fxh_coll, depth_coll, acc_coll, \
    rate_coll, detail_coll, balance_coll, orders_coll
from app.api.common.transfer_func import num_transfer
from app.api.common.utils import get_apikeys, set_apikeys
from app.api.common.huobi_util import HuobiUtil, place_type
import time

market = Blueprint('market', __name__)
logo_list = {}
exchange_id_list = {}
acc_id_list = []  # 特指现货ID， 实际上会有其他总类的ID
account_info = {}
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


def get_rate(exchange='huobi'):
    exchange = exchange
    k_query = {'exchange': exchange}
    data = []
    ret = {'rate_list': data}
    get_coin_logo()
    cc = 0
    rate_data = rate_coll.find(k_query)
    for ones in rate_data:
        if ones['sym'] == 'usdt_cny':
            data.append({'USDT': ones['rate']})
    for keys, values in logo_list.items():
        if cc > len(WALLET_SYMBOL):
            break
        sym = '{0}{1}'.format(keys, '/USDT')
        if sym in WALLET_SYMBOL:
            info = {}
            info['logo'] = values['Logo']
            k_query.update({'sym': sym})
            rt = detail_coll.find_one(k_query)
            if rt is None:
                continue
            info[keys] = rt['Price']
            data.append(info)
            cc += 1
    # print(ret)
    return ret


@market.route("/vw/rate", methods=['POST'])
def get_exchange_rate():
    # exchange = request.form.get('exchange')
    exchange = 'huobi'
    k_query = {'exchange': exchange}
    data = []
    ret = {'rate_list': data}
    get_coin_logo()
    cc = 0
    rate_data = rate_coll.find(k_query)
    for ones in rate_data:
        data.append({ones['sym']: ones['rate']})
    for keys, values in logo_list.items():
        if cc > len(WALLET_SYMBOL):
            break
        sym = '{0}{1}'.format(keys, '/USDT')
        if sym in WALLET_SYMBOL:
            info = {}
            info['logo'] = values['Logo']
            k_query.update({'sym': sym})
            rt = detail_coll.find_one(k_query)
            if rt is None:
                continue
            info[keys] = rt['Price']
            data.append(info)
            cc += 1
    return jsonify(ret)


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
                ex_id = dd['id']
                ex_name = dd['exchange']
                if ex_name not in exchange_id_list:
                    exchange_id_list.update({ex_name: ex_id})
            ret['data']['list'] = rdata
            # print(exchange_id_list)
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


@market.route('/vw/add_exchange', methods=['POST'])
def add_exchange():
    """
    2ce08492-1d69-4e97-9e4a-78801d454a1b
    15BDC2068842DDA5F9F90B71ED826276
    :return:
    """
    ret = {'code': 200, "msg": "成功"}
    exchange = request.form.get('exchange')
    api_key = request.form.get('api_key')
    secret_key = request.form.get('secret_key')
    # api_key = '2ce08492-1d69-4e97-9e4a-78801d454a1b'
    # secret_key = '15BDC2068842DDA5F9F90B71ED826276'
    # only for test
    # exchange = 'okex'
    # only for test
    key_info = set_apikeys({'access': api_key, 'secret': secret_key})
    try:
        acc_coll.update({'exchange': exchange, 'api': 'key'},
                        {'$set': {'access': key_info[0], 'secret': key_info[1]}}, True)
    except Exception as e:
        ret.update({'data': e})
    finally:
        return jsonify(ret)
        # print(ret)


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


@market.route('/vw/orders', methods=['POST'])
def get_orders_info():
    """
    获取所有提交的订单信息
      "limitMarketOrderFlag":"限价单、市价单的标识，0，1表示，不分买卖",
    :return: 
    """
    exchange = request.form.get('exchange')
    sym_id = request.form.get('sym_id')
    symbol = Symbol.get_stander_symbol(sym_id)
    order_type = request.form.get('order_flag')

    ex_id = EXCHANGE_LIST.index(exchange.upper()) + 1
    sym = Symbol.convert_to_platform_symbol(str(ex_id), symbol)

    # 用户的登陆信息 默认数据库中的值
    if len(acc_id_list) == 0:
        acc_info = acc_coll.find({"exchange": exchange, "api": 'accounts', "type": 'spot'})
        for one in acc_info:
            acc_id = one['id']
            acc_id_list.append(acc_id)
    accid = '{0}'.format(acc_id_list[0])
    k_query = {"exchange": exchange, "sym": sym, "acc_id": accid}
    if order_type == '0':  # 显示所有的限价单
        k_query['type'] = {"$regex": "^\S+limit$"}
    elif order_type == '1':  # 显示所有的市价单
        k_query['type'] = {"$regex": "^\S+market$"}
    ord_ret = orders_coll.find(k_query)

    ord_list = []
    ret = {'code': 200, "msg": "成功", "data": {}}
    try:
        for rdata in ord_ret:
            status = rdata['state']
            cancel_yn = 'Y'
            if status == 'filled' or status == 'canceled':
                cancel_yn = 'N'
            od_info = {}
            od_info.update({'name': rdata['order_id']})
            od_info.update({'date': rdata['created-at']})
            od_info.update({'entrustment_num': rdata['field-amount']})
            od_info.update({'make_deal__num': rdata['field-cash-amount']})
            od_info.update({'entrustment_price': rdata['price']})
            od_info.update({'cancel_orderstate': cancel_yn})
            ord_list.append(od_info)
    except Exception as e:
        ord_list.append({'msg': e})
    finally:
        ret['data']['list'] = ord_list
    return jsonify(ret)


@market.route('/vw/depth', methods=['POST'])
def get_depth_info():
    """
    交易页面获取数据接口 要提供给前端depth的部分信息及账户余额信息
    :return:
    """
    exchange = request.form.get('exchange')
    sym_id = request.form.get('sym_id')
    total_amount = request.form.get('total_sum')
    symbol = Symbol.get_stander_symbol(sym_id)
    acc_sym = symbol.split('/')[0].lower()
    k_query = {"exchange": exchange, "sym": symbol}

    # 获取当前登陆用户的sym对应的余额
    # 用户的登陆信息 默认数据库中的值
    acc_info = acc_coll.find({"exchange": exchange, "api": 'accounts'})
    balance = '-1'
    for one in acc_info:
        acc_id = one['id']
        acc_id_list.append(acc_id)
        rt = balance_coll.find_one({"exchange": exchange, "acc_id": acc_id, "acc_state": 'working',
                                    "acc_type": 'spot', "sym": acc_sym, "type": 'trade'})
        if 'balance' in rt:
            balance = rt['balance']
    # 获取当前登陆用户的sym对应的余额

    data = depth_coll.find(k_query).sort("ts", -1).limit(5)
    if data is None:
        return jsonify({'code：': 'Error'})
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
                change = rt["Change"]
                dd_data['flag'] = 0 if change[0] == '-' else 1
                dd_data['Vol_RMB'] = vol
                dd_data['Vol_USD'] = vol_usd
                dd_data['Change'] = change
                dd_data['AvaiableNum'] = balance
                dd_data['MakeDealPrice'] = total_amount
            buy_data = []
            sell_data = []
            for dd in data:
                get_sym_id_log(symbol, dd)
                dd['delta'] = change
                # ts = time_stamp(dd['ts'])
                buy_data.append({'buy_price': str(dd['buy_price']), 'buy_amt': str(dd['buy_amt'])})
                sell_data.append({'sell_price': str(dd['sell_price']), 'sell_amt': str(dd['sell_amt'])})
            ret['data'].update(dd_data)
            ret['data']['list_sell_out'] = sell_data
            ret['data']['list_buying'] = buy_data
        return jsonify(ret)


@market.route('/vw/trade', methods=['POST'])
def do_trade():
    """
    交易管理接口 从前端接收交易价格和数量后 调用交易api
    入参{"exchang":"交易所名字"  "sym_id":"货币对id" "flag":"买卖标识，0买，1卖"
         "price":"价格" "num":"数量"
    """
    exchange = request.form.get('exchange')
    sym_id = request.form.get('sym_id')
    # print('sym_id= ', sym_id)
    symbol = Symbol.get_stander_symbol(sym_id)
    ex_id = EXCHANGE_LIST.index(exchange.upper()) + 1
    sym = Symbol.convert_to_platform_symbol(str(ex_id), symbol)
    trade_flag = request.form.get('flag')
    # print('flag类型：', type(trade_flag))
    trade_flag = place_type[int(trade_flag)]
    price = request.form.get('price')
    num = request.form.get('num')
    keys_data = acc_coll.find_one({"exchange": exchange, "api": 'key'})
    key_info = get_apikeys(keys_data)
    ret = {'code': 200, "msg": "成功"}
    # 需要验证登陆状态
    if len(acc_id_list):
        pass
    else:
        ret['msg'] = '请先登陆'
        time.sleep(2)
        acc_info = acc_coll.find({"exchange": exchange, "api": 'accounts', "type": 'spot'})
        for one in acc_info:
            acc_id = one['id']
            acc_id_list.append(acc_id)
        place_ret = HuobiUtil().place(symbol=sym, trade_flag=trade_flag, price=price, amount=num,
                                      account_id=acc_id_list[0], api_key=key_info[0], api_secret=key_info[1])
        ret.update({'status': place_ret})
        ret['msg'] = place_ret['status']
    return jsonify(ret)


def do_place():
    exchange = 'huobi'
    sym_id = '0'
    print('sym_id= ', sym_id)

    order_query = {'acc_id': '5632276', 'exchange': exchange, 'sym': 'btcusdt'}
    orders_ret = orders_coll.find(order_query)
    print(orders_ret)
    for rdata in orders_ret:
        status = rdata['state']
        cancel_yn = 'Y'
        if status == 'filled' or status == 'canceled':
            cancel_yn = 'N'
        print(cancel_yn)
    return
    symbol = Symbol.get_stander_symbol(sym_id)
    ex_id = EXCHANGE_LIST.index(exchange.upper()) + 1
    sym = Symbol.convert_to_platform_symbol(str(ex_id), symbol)
    # trade_flag = request.form.get('flag')
    trade_flag = 0
    trade_flag = place_type[int(trade_flag)]
    price = 5000
    num = 0.001
    # keys_data = keys_coll.find_one({"exchange": exchange})
    # # key_info = get_apikeys(keys_data)
    ret = {'code': 200, "msg": "成功"}
    if len(acc_id_list):
        pass
    else:
        # accounts = HuobiUtil().get_accounts(key_info)
        accounts = {'status': 'ok', 'data': [{'id': 5632276}]}
        if accounts['status'] == 'error':
            ret.update({'status': accounts})
            ret['msg'] = '失败'
            ret.pop('code')
        else:
            acc_id_list.append(accounts['data'][0]['id'])
    # place_ret = HuobiUtil().place(symbol=sym, trade_flag=trade_flag, price=price, amount=num,
    #                               account_id=acc_id_list[0], api_key=key_info[0], api_secret=key_info[1])
    types = ''
    for item in place_type:
        types += item + ','
    types = types.rstrip(',')
    place_ret = HuobiUtil().get_order(sym=sym, types=types, api_key=key_info[0], api_secret=key_info[1])
    ret.update({'status': place_ret})
    ret['msg'] = place_ret
    print(ret)


if __name__ == '__main__':
    # data = {"exchange": "huobi", "sym": "btc_usdt", }
    # do_ticker_test()
    # get_market_ai_delta()
    # get_depth_info()
    # keys_data = keys_coll.find_one({"exchange": 'huobi'})
    # key_info = get_keys(keys_data)
    # print(key_info)
    # # HuobiUtil().get_accounts(key_info)
    # HuobiUtil().get_account_balance(key_info)

    # do_trade()
    # keys_data = keys_coll.find_one({"exchange": 'huobi'})
    # key_info = get_apikeys(keys_data)
    # place_ret = HuobiUtil().place(symbol='btcusdt', trade_flag='sell-market', price=5.01, amount=0.001,
    #                               account_id=4461503, api_key=key_info[0], api_secret=key_info[1])
    # keys_data = keys_coll.find_one({"exchange": 'huobi'})
    # key_info = get_apikeys(keys_data)
    # do_place()
    # get_orders_info()
    # get_exchange_rate()
    add_exchange()
    # test----
    # get_rate('fcoin')
    # exchange = 'huobi'.upper()
    # ex_id = EXCHANGE_LIST.index(exchange)+1
    # test----
    pass
