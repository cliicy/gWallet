#  -*- coding:utf-8 -*-
from enum import Enum

SYMBOL_LIST = ['btc_usdt', 'bch_usdt', 'eth_usdt', 'ltc_usdt', 'eos_usdt', 'eth_btc', 'eos_btc', 'xrpusdt']
STANDARD_SYMBOL_LIST = ["BTC/USDT", "BCH/USDT", "ETH/USDT", "LTC/USDT", "EOS/USDT", "ETH/BTC", "EOS/BTC",
                        "XRP/USDT", "BCH/BTC", "LTC/BTC",  "XRP/BTC", "BCH/ETH",  "LTC/ETH", "EOS/ETH", "XRP/ETH"]

STANDARD_PERIOD_LIST = ["M1", "M5", "M15", "M30", "H1", "D1", "W1", "MON1", "Y1"]
MONGODB_PERIOD_DOC = ['dw_M1', 'dw_M5', 'dw_M15', 'dw_M30', 'dw_H1', 'dw_D1', 'dw_W1', 'dw_MON1', 'dw_Y1']
# MONGODB_PERIOD_DOC = ["dw_M1", "dw_M5", "dw_M15", "dw_M30", "dw_H1", "dw_D1", "dw_W1", "dw_MON1", "dw_Y1"]


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
    BCC_USDT = 7

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


if __name__ == '__main__':
    pass
    doc_name = Symbol.convert_to_period_doc('H1')
    print(doc_name)
