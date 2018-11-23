from flask import Flask, url_for


def register_blueprints(app):
    from app.api.vw.market import market
    from app.api.vw.trades import trades
    from app.api.vw.ticker import tickers
    from app.api.vw.candle import kline
    app.register_blueprint(market)
    app.register_blueprint(trades)
    app.register_blueprint(tickers)
    app.register_blueprint(kline)


def create_app():
    app = Flask(__name__)
    app.config['JSON_AS_ASCII'] = False
    # app.config.from_object('app.config.settings')
    app.config.from_object('app.config.secure')
    app.config.from_object('app.config.enums')
    register_blueprints(app)
    return app

