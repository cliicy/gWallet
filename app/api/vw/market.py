from flask import jsonify, Blueprint
from app.config.enums import Symbol
from app.config.secure import ticker_coll


info = [
    {
        '交易所': 'Fcoin',
        '数字货币': 'BTC',
        '最新价': '$6365.98',
        '涨跌幅': '0.42%',
        '成交量': '约7.4亿'
    },
    {
        '交易所': 'OKEx',
        '数字货币': 'ETH',
        '最新价': '$198.25',
        '涨跌幅': '0.53%',
        '成交量': '约1524万'
    }
]

market = Blueprint('market', __name__)


@market.route('/vw/market/<exchange>/<symbol>', methods=['GET'])
def get_market_info(exchange, symbol):
    # dd = {'markets': {'exchange': exchange, 'info': info}}
    sym = Symbol.convert_to_stander_sym(symbol)
    k_query = {"sym": sym, "exchange": exchange}
    data = ticker_coll.find(k_query)
    if data is None:
        return jsonify({'code：': 'Error'})
    else:
        rdata = []
        for dd in data:
            dd.pop('_id')
            rdata.append(dd)
        return jsonify({'code': 200, "msg": "成功", "data": {"list": [rdata]}})
    return jsonify(dd)


if __name__ == '__main__':
    pass
    # get_market_info('fcoin', 'btc_usdt')
