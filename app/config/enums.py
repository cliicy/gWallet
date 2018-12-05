#  -*- coding:utf-8 -*-
from enum import Enum, unique


SYMBOL_LIST = ['btc_usdt', 'bch_usdt', 'eth_usdt', 'ltc_usdt', 'eos_usdt', 'eth_btc', 'eos_btc', 'xrpusdt']
STANDARD_SYMBOL_LIST = ["BTC/USDT", "BCH/USDT", "ETH/USDT", "LTC/USDT", "EOS/USDT", "ETH/BTC", "EOS/BTC",
                        "XRP/USDT", "BCC/USDT", "ETC/USDT", "BCH/BTC", "LTC/BTC",  "XRP/BTC", "BCH/ETH",
                        "LTC/ETH", "EOS/ETH", "XRP/ETH"]

HUOBI_SYMBOL_LIST = ['btcusdt', 'bchusdt', 'ethusdt', 'ltcusdt', 'eosusdt', 'ethbtc', 'eosbtc', 'xrpusdt']
BINANCE_SYMBOL_LIST = ['BTCUSDT', 'BCCUSDT', 'ETHUSDT', 'LTCUSDT', 'EOSUSDT', 'ETHBTC', 'EOSBTC', 'XRPUSDT']
OKEX_SYMBOL_LIST = ['btc_usdt', 'bch_usdt', 'eth_usdt', 'ltc_usdt', 'eos_usdt', 'eth_btc', 'eos_btc', 'xrp_usdt',
                    'bch_btc', "ltc_btc",  "xrp_btc", "bch_eth",  "ltc_eth", "eos_eth", "xrp_eth"]
OKEX_FUTURE_SYMBOL_LIST = ['btc_usd', 'bch_usd', 'eth_usd', 'ltc_usd', 'eos_usd', None, None, 'xrp_usd']
FCOIN_SYMBOL_LIST = ['btcusdt', 'bchusdt', 'ethusdt', 'ltcusdt', None, None, None, 'xrpusdt']

STANDARD_PERIOD_LIST = ["M1", "M5", "M15", "M30", "H1", "D1", "W1", "MON1", "Y1"]
MONGODB_PERIOD_DOC = ['dw_M1', 'dw_M5', 'dw_M15', 'dw_M30', 'dw_H1', 'dw_D1', 'dw_W1', 'dw_MON1', 'dw_Y1']
EXCHANGE_LIST = ['HUOBI', 'BINANCE', 'FCOIN', 'OKEX_FUTURE', 'OKEX']

@unique
class Platform(Enum):
    """
    交易平台枚举
    """
    PLATFORM_HUOBI = "1"
    PLATFORM_BINANCE = "2"
    PLATFORM_FCOIN = "3"
    PLATFORM_OKEX = "5"
    PLATFORM_OKEX_FUTURE = "4"


class Symbol(Enum):
    """
    货币对枚举
    """
    BTC_USDT = 0
    BCH_USDT = 1
    ETH_USDT = 2
    LTC_USDT = 3
    EOS_USDT = 4
    ETH_BTC = 5
    EOS_BTC = 6
    XRP_USDT = 7
    BCC_USDT = 8

    @staticmethod
    def convert_to_period_doc(period):
        """
        根据传入的不同的时间间隔获得标准mongodb document
        :param period:平台kline时间间隔
        :return:
        """
        index = STANDARD_PERIOD_LIST.index(period)
        return MONGODB_PERIOD_DOC[index]

    @staticmethod
    def convert_to_stander_sym(symbol):
        """
        获得标准的存在与mongodb中的货币对
        :param symbol:
        :return:
        """
        index = SYMBOL_LIST.index(symbol)
        return STANDARD_SYMBOL_LIST[index]

    @staticmethod
    def get_stander_sym_id(symbol):
        """
        获得标准的存在与mongodb中的货币对
        :param symbol:
        :return:
        """
        index = STANDARD_SYMBOL_LIST.index(symbol)
        return index

    @staticmethod
    def get_stander_symbol(req_para):
        if req_para == '':
            return ''
        sym_id = int(req_para)
        assert (sym_id < len(STANDARD_SYMBOL_LIST))
        return STANDARD_SYMBOL_LIST[sym_id]

    @staticmethod
    def convert_to_platform_symbol(platform, symbol):
        """
        获得平台货币对
        :param platform:平台枚举
        :param symbol:标准货币对
        :return:
        """
        if platform == Platform.PLATFORM_HUOBI.value:
            index = STANDARD_SYMBOL_LIST.index(symbol)
            return HUOBI_SYMBOL_LIST[index]
        elif platform == Platform.PLATFORM_BINANCE.value:
            index = STANDARD_SYMBOL_LIST.index(symbol)
            return BINANCE_SYMBOL_LIST[index]
        elif platform == Platform.PLATFORM_OKEX.value:
            index = STANDARD_SYMBOL_LIST.index(symbol)
            return OKEX_SYMBOL_LIST[index]
        elif platform == Platform.PLATFORM_OKEX_FUTURE.value:
            index = STANDARD_SYMBOL_LIST.index(symbol)
            return OKEX_FUTURE_SYMBOL_LIST[index]
        elif platform == Platform.PLATFORM_FCOIN.value:
            index = STANDARD_SYMBOL_LIST.index(symbol)
            return FCOIN_SYMBOL_LIST[index]


if __name__ == '__main__':
    pass
    doc_name = Symbol.convert_to_period_doc('H1')
    print(doc_name)
