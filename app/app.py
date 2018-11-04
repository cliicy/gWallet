from flask import Flask


def register_blueprints(app):
    from app.api.vw.market import market
    from app.api.vw.trades import trades
    from app.api.vw.ticker import ticker
    app.register_blueprint(market)
    app.register_blueprint(trades)
    app.register_blueprint(ticker)


def create_app():
    app = Flask(__name__)
    app.config['JSON_AS_ASCII'] = False
    app.config.from_object('app.config.settings')
    register_blueprints(app)
    return app

