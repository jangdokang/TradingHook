import ccxt
from model import MarketBuyOrder, MarketOrder, MarketSellOrder


class Binance:
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "_instance"):
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, key, secret):
        cls = type(self)
        if not hasattr(cls, "_init"):
            print("binance client start")
            self.binance_future = ccxt.binance({
                'apiKey': key,
                'secret': secret,
                'enableRateLimit': True,
                'options': {
                    'defaultType': 'future'
                }
            })
            self.binance = ccxt.binance({
                'apiKey': key,
                'secret': secret,
                'enableRateLimit': True
            })
            self.binance.load_markets()
            cls._init = True

    def market_order(self, order_info: MarketOrder):
        self.binance.load_markets()
        if "PERP" in order_info.quote:
            return self.binance_future.create_order(order_info.base+'/'+order_info.quote.replace("PERP", ""), order_info.type.lower(),
                                                    order_info.side.lower(), order_info.amount)
        else:
            return self.binance.create_order(order_info.base+'/'+order_info.quote, order_info.type.lower(),
                                             order_info.side.lower(), order_info.amount)

    def market_buy(self, order_info: MarketBuyOrder):
        return self.market_order(order_info)

    def market_sell(self, order_info: MarketSellOrder):
        return self.market_order(order_info)
