#  -*- coding:utf-8 -*-
from app.api.common.signature_util import SignatureUtil
from app.api.communicators import HttpCommunicator
from app.config.secure import huobi_setting
import operator as op
import base64
import datetime
import hashlib
import hmac
import urllib
import urllib.parse
import urllib.request
import json
place_type = ['buy-limit', 'sell-limit', 'buy-market', 'sell-market']


class HuobiUtil(SignatureUtil):
    """
    火币工具类
    """

    def sign(self, *args):
        """
        签名
        :return:
        """
        pass

    def verify(self, *args):
        """
        验证签名
        :return:
        """
        pass

    def api_key_get_params_prepare(self, params, request_path):

        """
            必须需要签名认证的get请求参数整理

        :param params: 请求参数  字典类型
        :param request_path: get请求接口路径 字符串类型
        :return:
            url：实际get请求地址 字符串类型
            params：整理之后的get请求参数 字典类型
            headers_get : get请求headers信息 字典类型
        """
        method = 'GET'
        timestamp = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S')
        params.update({'AccessKeyId': params['ACCESS_KEY'],
                       'SignatureMethod': 'HmacSHA256',
                       'SignatureVersion': '2',
                       'Timestamp': timestamp})
        host_url = huobi_setting['TRADE_URL']
        host_name = urllib.parse.urlparse(host_url).hostname
        host_name = host_name.lower()
        params['Signature'] = HuobiUtil.createSign(self,params, method, host_name, request_path,
                                                   params['SECRET_KEY'])

        url = host_url + request_path
        headers_get = huobi_setting['GET_HEADERS']
        return url, params, headers_get

    def api_key_post_params_prepare(self,params, request_path):

        """
        必须需要签名认证的post请求参数整理

        :param params: 请求参数  字典类型
        :param request_path: post请求接口路径 字符串类型
        :return:
            url：实际post请求地址 字符串类型
            params：整理之后的post请求参数 字典类型
            headers_post : post请求headers信息 字典类型
        """
        method = 'POST'
        timestamp = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S')
        params_to_sign = {'AccessKeyId': params['ACCESS_KEY'],
                          'SignatureMethod': 'HmacSHA256',
                          'SignatureVersion': '2',
                          'Timestamp': timestamp}
        host_url = huobi_setting['TRADE_URL']
        host_name = urllib.parse.urlparse(host_url).hostname
        host_name = host_name.lower()
        params_to_sign['Signature'] = HuobiUtil.createSign(self, params_to_sign, method, host_name, request_path,
                                                           params['SECRET_KEY'])

        url = host_url + request_path + '?' + urllib.parse.urlencode(params_to_sign)
        headers_post = huobi_setting['POST_HEADERS']

        return url, json.dumps(params), headers_post

    def createSign(self, pParams, method, host_url, request_path, secret_key):

        """
        签名生成方法
        """
        sorted_params = sorted(pParams.items(), key=lambda d: d[0], reverse=False)
        encode_params = urllib.parse.urlencode(sorted_params)
        payload = [method, host_url, request_path, encode_params]
        payload = '\n'.join(payload)
        payload = payload.encode(encoding='UTF8')
        secret_key = secret_key.encode(encoding='UTF8')

        digest = hmac.new(secret_key, payload, digestmod=hashlib.sha256).digest()
        signature = base64.b64encode(digest)
        signature = signature.decode()
        return signature

    def get_accounts(self, acc_info):
        # """
        # :return:
        # """
        return
        path = "/v1/account/accounts"
        params = {}
        params.update({'ACCESS_KEY': acc_info[0], 'SECRET_KEY': acc_info[1]})
        url, params, headers_post = HuobiUtil.api_key_get_params_prepare(self, params, path)
        return HttpCommunicator.http_get(self, url=url, params=params, headers=headers_post)

    def get_account_balance(self, acc_info):
        """
        :param acc_info:
        :return:
        """
        return
        rbalance = []
        try:
            ret = self.get_accounts(acc_info)
            # print('获取到的账户信息：', ret)
            for item in ret['data']:
                path = '{}/{}/{}'.format("/v1/account/accounts", item['id'], "balance")
                # print('获取到的账户信息中的ID和path：', path)
                params = {}
                params.update({'ACCESS_KEY': acc_info[0], 'SECRET_KEY': acc_info[1]})
                url, params, headers_post = HuobiUtil.api_key_get_params_prepare(self, params, path)
                # print('要查询账户余额信息的参数：', params)
                rdata = HttpCommunicator.http_get(self, url=url, params=params, headers=headers_post)
                print('获取到的账户[{0}]余额信息：{1}'.format(item['id'], rdata))
                rbalance.append(rdata)
        except EnvironmentError as e:
            print(e)
            rbalance.append(e)
        finally:
            return rbalance

    def place(self, **args):
        """
        下单
        https://github.com/huobiapi/API_Docs/wiki/
        REST_api_reference#post-v1orderordersplace-pro%E7%AB%99%E4%B8%8B%E5%8D%95
        buy-market：市价买, sell-market：市价卖, buy-limit：限价买, sell-limit：限价卖
        """
        try:
            acct_id = 0
            if 'account_id' in args:
                acct_id = args['account_id']
            else:
                accounts = HuobiUtil.get_accounts(self)
                acct_id = accounts['data'][0]['id']
        except BaseException as e:
            print('get acct_id error.%s' % e)
        symbol = ''
        if "symbol" in args:
            symbol = args["symbol"]
        if "amount" in args:
            amount = args["amount"]
        if "price" in args:
            price = args["price"]
        if "trade_flag" in args:
            flag = args["trade_flag"]
        if "api_key" in args:
            api_key = args["api_key"]
        if "api_secret" in args:
            api_secret = args["api_secret"]
        params = {
              "amount": amount,
              "symbol": symbol,
              "price": price,
              "source": ''
        }

        params.update({"account-id": acct_id, "type": flag})
        params.update({'ACCESS_KEY': api_key, 'SECRET_KEY': api_secret})
        order_place_url = huobi_setting['ORDER_PLACE_URL']
        # 代签名post请求，参数准备
        url, params, headers = HuobiUtil.api_key_post_params_prepare(self, params, order_place_url)
        # print(url, params, headers)
        ret = None
        try:
            result_json = HttpCommunicator.http_post(self, url, params, headers)
            print(result_json)
            ret = result_json
        except BaseException as e:
            ret = e
        finally:
            return ret

    def get_order(self, **args):
        """
        查询订单信息
         :param order_id:
          :return:
        """
        return
        params = {}
        url = "/v1/order/orders/"
        try:
            if "order_id" in args:
                url = "/v1/order/orders/{0}".format(args["order_id"])
            if "api_key" in args:
                params.update({'ACCESS_KEY': args["api_key"]})
            if "sym" in args:
                params.update({'sym': args['sym']})
            if "api_secret" in args:
                params.update({'SECRET_KEY': args["api_secret"]})
            if "types" in args:
                params.update({'types': args["types"]})
        except BaseException as e:
            print('get acct_id error.%s' % e)
        params.update({"states": 'submitted'})
        print('传入的请求参数：', params)
        url, params, headers = HuobiUtil.api_key_get_params_prepare(self, params, url)
        ret = None
        try:
            ret = HttpCommunicator.http_get(self, url, params, headers)
            print(ret)
        except BaseException as e:
            ret = e
        finally:
            return ret


if __name__ == '__main__':
    # ret = {'code': 200, "msg": "成功"}
    # if accounts['status'] == 'error':
    #     ret.update({'status': accounts})
    #     ret['msg'] = '失败'
    #     ret.pop('code')
    # else:
    #     acc_id_list[0] = accounts['data'][0]['id']
    #     place_ret = HuobiUtil().place(symbol=ssym, trade_flag=trade_flag, price=price, amount=num,
    #                                   account_id=acc_id_list[0], api_key=key_info[0], api_secret=key_info[1])
    #     ret.update({'status': place_ret})
    pass
