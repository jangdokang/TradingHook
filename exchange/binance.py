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
            # print("binance client start")
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
        return self.binance.create_order(order_info.base+'/'+order_info.quote, order_info.type.lower(),
                                             order_info.side.lower(), order_info.amount)

    def market_buy(self, order_info: MarketBuyOrder):
        return self.market_order(order_info)
    def market_sell(self, order_info: MarketSellOrder):
        result = None
        free_balance = self.binance.fetch_free_balance()
        if free_balance.get(order_info.base):
            sell_amount = free_balance[order_info.base] * \
                float(order_info.sell_percent)/100
            order_info.amount = sell_amount
            result = self.market_order(order_info)
            return result
        else:
            raise Exception("팔 수 있는 물량이 없습니다.")

    def market_entry(self, order_info: MarketOrder):
        print(order_info.leverage)
        if "PERP" in order_info.quote:
            if order_info.leverage != 0:
                self.set_leverage(order_info)
            return self.binance_future.create_order(order_info.base+'/'+order_info.quote.replace("PERP", ""), order_info.type.lower(),
                                                    order_info.side.lower().split("/")[-1], abs(order_info.amount))
        else:
            raise Exception("선물마켓이 아닙니다.")
    
    def market_close(self, order_info: MarketOrder):
        if "PERP" not in order_info.quote:
            raise Exception("선물마켓이 아닙니다.")
        result = None
        symbol = order_info.base+'/'+order_info.quote.replace("PERP", "")
        position = self.binance_future.fetch_positions_risk(symbols=[symbol])
        if position:
            contracts = position[0]["contracts"]
            if contracts == 0:
                raise Exception("포지션이 없습니다")
            if order_info.close_percent != "0":
                close_amount = contracts*float(order_info.close_percent)/100
            elif order_info.amount != 0:
                close_amount = order_info.amount
            
            return self.binance_future.create_order(symbol, order_info.type.lower(),
                                                    order_info.side.lower().split("/")[-1], close_amount, params={"reduceOnly": True})
        else:
            raise Exception("포지션이 없습니다")

    def set_leverage(self, order_info: MarketOrder):
        self.binance_future.set_leverage(order_info.leverage, order_info.base + "/" + order_info.quote.replace("PERP", ""))
