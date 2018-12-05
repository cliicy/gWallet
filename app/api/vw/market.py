from flask import jsonify, Blueprint, request
from app.config.enums import Symbol, STANDARD_SYMBOL_LIST, WALLET_SYMBOL, EXCHANGE_LIST
from app.config.secure import ticker_coll, ai_news_coll, logo_coll, fxh_coll, depth_coll, keys_coll, \
    rate_coll, detail_coll
from app.api.common.transfer_func import num_transfer
from app.api.common.utils import get_apikeys
from app.api.common.huobi_util import HuobiUtil, place_type
import json

market = Blueprint('market', __name__)
logo_list = {}
exchange_id_list = {}
acc_id_list = []
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


@market.route('/vw/depth', methods=['POST'])
def get_depth_info():
    """
    交易页面获取数据接口 要提供给前端depth的部分信息及账户余额信息
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
    total_amount = request.form.get('total_sum')
    symbol = Symbol.get_stander_symbol(sym_id)
    k_query = {"exchange": exchange, "sym": symbol}
    data = depth_coll.find(k_query).sort("ts", -1).limit(5)
    keys_data = keys_coll.find_one({"exchange": exchange})
    key_info = get_apikeys(keys_data)
    # 获取此账户及其下各个子账户中的所有拥有此币种的所有余额信息
    acc_ret = HuobiUtil().get_account_balance(key_info)
    print('账户信息：', acc_ret)
    bal = request.form.get('bal')  # 只是设置初始值为null
    balance = bal
    if len(acc_ret) > 0:
        sym = symbol.split('/')[0].lower()
        for acc in acc_ret:
            # balance['status'] = acc['status']
            if acc['status'] == 'ok':
                coin_list = acc['data']['list']
                for info in coin_list:
                    if sym == info['currency']:
                        if acc['data']['type'] == 'spot':
                            if acc['data']['state'] == 'working':
                                if info['type'] == 'trade':
                                    # print('&&&&&&&&&&& ', info)
                                    balance = info['balance']
                                    acc_id_list.append(acc['data']['id'])
                                    break
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
                buy_data.append({'buy_price': str(dd['buy_price']), 'buy_amt': str(dd['buy_amt'])})  # , 'ts': ts
                sell_data.append({'sell_price': str(dd['sell_price']), 'sell_amt': str(dd['sell_amt'])})  # , 'ts': ts
            ret['data'].update(dd_data)
            ret['data']['list_sell_out'] = sell_data
            ret['data']['list_buying'] = buy_data

            # 获取所有提交的订单信息
            ex_id = EXCHANGE_LIST.index(exchange.upper()) + 1
            sym = Symbol.convert_to_platform_symbol(str(ex_id), symbol)
            types = ''
            for item in place_type:
                types += item + ','
            types = types.rstrip(',')
            od_info = {}
            try:
                orders_ret = HuobiUtil().get_order(sym=sym, types=types, api_key=key_info[0], api_secret=key_info[1])
                if len(orders_ret['data']):
                    rdata = orders_ret['data']
                    lt_name = rdata['type']
                    lt_date = rdata['created-at']
                    ent_num = orders_ret('field-amount')
                    deal_num = orders_ret('field-cash-amount')
                    ent_price = orders_ret('price')
                    status = orders_ret('state')
                    cancel_yn = 'Y'
                    if status == 'filled' or status == 'canceled':
                        cancel_yn = 'N'
            except BaseException as e:
                od_info.update({'msg': e})
            finally:
                od_info.update({'limit_name': lt_name})
                od_info.update({'limit_date': lt_date})
                od_info.update({'entrustment_num': ent_num})
                od_info.update({'make_deal__num': deal_num})
                od_info.update({'entrustment_price': ent_price})
                od_info.update({'cancel_orderstate': cancel_yn})
                ret['data']['list_Limit'] = [od_info]
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
    keys_data = keys_coll.find_one({"exchange": exchange})
    key_info = get_apikeys(keys_data)
    ret = {'code': 200, "msg": "成功"}
    if len(acc_id_list):
        pass
    else:
        accounts = HuobiUtil().get_accounts(key_info)
        if accounts['status'] == 'error':
            ret.update({'status': accounts})
            ret['msg'] = '失败'
            ret.pop('code')
        else:
            acc_id_list.append(accounts['data'][0]['id'])
            place_ret = HuobiUtil().place(symbol=sym, trade_flag=trade_flag, price=price, amount=num,
                                  account_id=acc_id_list[0], api_key=key_info[0], api_secret=key_info[1])
            ret.update({'status': place_ret})
            ret['msg'] = place_ret['status']
    return jsonify(ret)


# def do_ticker_test():
# #     exchange = 'huobi'
# #     k_query = {'exchange': exchange, 'sym': {'$in': STANDARD_SYMBOL_LIST}}
# #     # k_query = {'exchange': exchange, 'sym': STANDARD_SYMBOL_LIST}
# #     data = ticker_coll.find(k_query, {'sym': 1, 'exchange': 1})
# #     # data = ticker_coll.find(k_query, {'sym': 1, 'exchange': 1})
# #     if data is None:
# #         print('Error')
# #     else:
# #         ret = {'code': 200, "msg": "成功", "data": {"list": []}}
# #         count = data.count()
# #         if count > 0:
# #             rdata = []
# #             for dd in data:
# #                 dd.pop('_id')
# #                 # dd.pop('api')
# #                 rdata.append(dd)
# #             ret['data']['list'] = rdata
# #         print(ret)
# #
# #
def do_place():
    exchange = 'huobi'
    sym_id = '0'
    print('sym_id= ', sym_id)
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
    do_place()
    # do_trade()
    # get_exchange_rate()
    # test----
    # get_rate('fcoin')
    # exchange = 'huobi'.upper()
    # ex_id = EXCHANGE_LIST.index(exchange)+1
    # test----
    pass
