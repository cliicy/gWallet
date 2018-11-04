from flask import jsonify, Blueprint

marketinfo = [
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


@market.route('/vw/market/<exchange>', methods=['GET'])
def get_market_info(exchange):
    # return 'aaa'
    dd = {'markets': {'exchange': exchange, 'info': marketinfo}}
    return jsonify(dd)


