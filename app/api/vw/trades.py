from flask import jsonify, Blueprint

details = [
    {
        'id': 'okex',
        'title': u'获取最新行情',
        'description': u'开盘价，收盘价，成交额'
    },
    {
        'id': '币安',
        'title': u'获取最新行情',
        'description': u'开盘价，收盘价，成交额'
    }
]

# blueprint
trades = Blueprint('trades', __name__)


@trades.route('/vw/trades/<exchange>/<symbol>', methods=['GET'])
def get_trades_info(exchange, symbol):
    # print(exchange)
    dd = {'trades': {'exchange': exchange, 'symbol': symbol, 'information': details}}
    return jsonify(dd)


if __name__ == '__main__':
    pass

