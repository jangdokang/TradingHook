from model import MarketOrder
from utility import settings
from datetime import datetime, timezone, timedelta
from dhooks import Webhook

try:
    hook = Webhook(settings.DISCORD_WEBHOOK_URL.replace("discordapp", "discord"))
except Exception as e:
    print("웹훅 URL이 유효하지 않습니다: ", settings.DISCORD_WEBHOOK_URL)

def parse_time(utc_timestamp):
    timestamp = utc_timestamp + timedelta(hours=9).seconds
    date = datetime.fromtimestamp(timestamp)
    return date.strftime('%y.%m.%d %H:%M:%S')


def log_message(message):
    if hook:
        hook.send(str(message))
    else:
        print(message)


def log_order_message(exchange_name, order_result: dict):
    print(order_result)
    date = parse_time(datetime.utcnow().timestamp())
    if exchange_name == "UPBIT" and order_result.get('side') == "buy":
        amount = order_result.get('cost')
    else:
        amount = order_result.get('amount')
    log_message(
        f"[OrderResult]\n{date} {exchange_name} {order_result.get('symbol')} {order_result.get('type')} {order_result.get('side')} {amount}")

def log_alert_message(order_info: MarketOrder):
    if order_info.side == "BUY":
            msg = f"[alert_message]\nExchange: {order_info.exchange}\nOrderName: {order_info.order_name}\nSymbol: {order_info.base}/{order_info.quote}\nSide: {order_info.side}\nPrice: {order_info.price}\nAmount: {order_info.amount}"
    elif order_info.side == "SELL":
        msg = f"[alert_message]\nExchange: {order_info.exchange}\nOrderName: {order_info.order_name}\nSymbol: {order_info.base}/{order_info.quote}\nSide: {order_info.side}\nPrice: {order_info.price}\nPercent: {order_info.sell_percent}"
    elif order_info.side == "entry/buy":
        msg = f"[alert_message]\nExchange: {order_info.exchange}\nOrderName: {order_info.order_name}\nSymbol: {order_info.base}/{order_info.quote}\nSide: LONG\nPrice:{order_info.price}\nAmount: {order_info.amount}"
    elif order_info.side == "entry/sell":
        msg = f"[alert_message]\nExchange: {order_info.exchange}\nOrderName: {order_info.order_name}\nSymbol: {order_info.base}/{order_info.quote}\nSide: SHORT\nPrice:{order_info.price}\nAmount: {order_info.amount}"
    elif order_info.side == "close/buy":
        msg = f"[alert_message]\nExchange: {order_info.exchange}\nOrderName: {order_info.order_name}\nSymbol: {order_info.base}/{order_info.quote}\nSide: Close SHORT\nPrice:{order_info.price}\nPercent: {order_info.close_percent}"
    elif order_info.side == "close/sell":
        msg = f"[alert_message]\nExchange: {order_info.exchange}\nOrderName: {order_info.order_name}\nSymbol: {order_info.base}/{order_info.quote}\nSide: Close LONG\nPrice: {order_info.price}\nPercent: {order_info.close_percent}"
    log_message(msg)