from flask import jsonify, Blueprint
import time
import pandas as pd
from app.config.secure import ticker_coll

tickers = Blueprint('ticker', __name__)


# only for test
@tickers.route('/vw/tickers', methods=['GET'])
def get_ticker_info():
    while True:
        try:
            ticker = []
            dd = {'ticker': ticker}
            data = pd.DataFrame(list(ticker_coll.find()))
            data = data[['sym', 'Change', 'High', 'Low', 'Price', 'Volume']]
            dc = data.set_index('sym').T.to_dict('dict')
            for k, vdata in dc.items():
                tk = {}
                tk['数字货币'] = k
                tk['最新价'] = vdata['Price']
                tk['涨跌幅'] = vdata['Change']
                tk['成交量'] = vdata['Volume']
                tk['24小时内最高价'] = vdata['High']
                tk['24小时内最低价'] = vdata['Low']
                ticker.append(tk)
            # print(data.to_string(index=False))
            return jsonify(dd)
        except Exception as error:
            print(error)
        time.sleep(30)
    # return jsonify(ticker)
