import ccxt
from model import MarketBuyOrder, MarketSellOrder


class Upbit:
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "_instance"):
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, key, secret):
        cls = type(self)
        if not hasattr(cls, "_init"):
            # print("upbit client start\n")
            self.upbit = ccxt.upbit({
                'apiKey': key,
                'secret': secret,
                'enableRateLimit': True
            })
            self.upbit.load_markets()
            cls._init = True

    def market_buy(self, order_info: MarketBuyOrder):
        return self.upbit.create_order(order_info.base+'/'+order_info.quote, order_info.type.lower(),
                                       order_info.side.lower(), order_info.amount, order_info.price)

    def market_sell(self, order_info: MarketSellOrder):
        result = None
        free_balance = self.upbit.fetch_free_balance()
        if free_balance.get(order_info.base):
            sell_amount = free_balance[order_info.base] * \
                float(order_info.sell_percent)/100
            result = self.upbit.create_order(order_info.base+'/' +
                                             order_info.quote, order_info.type.lower(), order_info.side.lower(), sell_amount)
            return result
        else:
            raise Exception("팔 수 있는 물량이 없습니다.")
