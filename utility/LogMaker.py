from utility import settings
from datetime import datetime, timezone, timedelta
from dhooks import Webhook
hook = Webhook(settings.DISCORD_WEBHOOK_URL)

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

