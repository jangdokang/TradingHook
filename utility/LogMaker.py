import sys
from model import MarketOrder
from utility import settings
from datetime import datetime, timezone, timedelta
from dhooks import Webhook, Embed

from loguru import logger
logger.remove(0)
logger.add("./log/tradinghook.log",rotation="1 days", retention="7 days", format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}")
logger.add(sys.stderr, colorize=True,format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level}</level> | <level>{message}</level>")

try:
    hook = Webhook(settings.DISCORD_WEBHOOK_URL.replace("discordapp", "discord"))
except Exception as e:
    print("웹훅 URL이 유효하지 않습니다: ", settings.DISCORD_WEBHOOK_URL)

def parse_time(utc_timestamp):
    timestamp = utc_timestamp + timedelta(hours=9).seconds
    date = datetime.fromtimestamp(timestamp)
    return date.strftime('%y-%m-%d %H:%M:%S')

def logger_test():
    date = parse_time(datetime.utcnow().timestamp())
    logger.info(date)

def log_message(message="None", embed: Embed = None):
    if hook:
        if embed:
            hook.send(embed=embed)
        else:
            hook.send(message)
        # hook.send(str(message), embed)
    else:
        logger.info(message)
        print(message)

def log_order_message(exchange_name, order_result: dict, order_info: MarketOrder):
    date = parse_time(datetime.utcnow().timestamp())
    if exchange_name == "UPBIT" and order_result.get('side') == "buy":
        f_name = "비용"
        amount = str(order_result.get('cost'))
    else:
        f_name = "수량"
        amount = str(order_result.get('amount'))
    side = ""
    symbol = order_info.base + '/' + order_info.quote
    if order_info.side == "BUY":
        side = "BUY"
    elif order_info.side == "SELL":
        side = "SELL"
    elif order_info.side == "entry/buy":
        side = "LONG"
    elif order_info.side == "entry/sell":
        side = "SHORT"
    elif order_info.side == "close/buy":
        side = "Close/SHORT"
    elif order_info.side == "close/sell":
        side = "CLOSE/LONG"

    content = f"일시\n{date}\n\n거래소\n{exchange_name}\n\n심볼\n{symbol}/{order_info.quote}\n\n거래유형\n{order_result.get('side')}\n\n{amount}"
    embed = Embed(
    title = order_info.order_name,
    description=f"체결: {exchange_name} {symbol} {side} {amount}",
    color=0x0000FF,
    )
    
    
    embed.add_field(name='일시', value=str(date), inline=False)
    embed.add_field(name='거래소', value=exchange_name, inline=False)
    embed.add_field(name='심볼', value=symbol, inline=False)
    embed.add_field(name='거래유형', value=side, inline=False)
    embed.add_field(name=f_name, value=amount, inline=False)

    log_message(content, embed)

def log_order_error_message(error, order_info: MarketOrder):
    embed = Embed(
    title = order_info.order_name,
    description=f"[주문 오류가 발생했습니다]\n{error}",
    color=0xFF0000,
    )
    logger.error(f"주문 오류가 발생했습니다 : {error}")
    
    log_message(embed=embed)

def log_validation_error_message(msg):
    logger.error(f"검증 오류가 발생했습니다\n{msg}")
    log_message(msg)

def print_alert_message(order_info: MarketOrder):
    if order_info.side == "BUY":
        side = "BUY"
        f_name = "amount"
        value = order_info.amount
    elif order_info.side == "SELL":
        side = "SELL"
        # print("sell_percent: ",order_info.sell_percent)
        # print("sell_amount", order_info.amount)
        if order_info.sell_percent == "0":
            f_name = "amount"
            value = order_info.amount
        else:
            f_name = "sell_percent"
            value = f"{order_info.sell_percent}%"
    elif order_info.side == "entry/buy":
        side = "LONG"
        f_name = "amount"
        value = order_info.amount
    elif order_info.side == "entry/sell":
        side = "SHORT"
        f_name = "amount"
        value = order_info.amount
    elif order_info.side == "close/buy":
        side = "ClOSE/SHORT"
        if order_info.close_percent == "0":
            f_name = "amount"
            value = order_info.amount
        else:
            f_name = "close_percent"
            value = f"{order_info.close_percent}%"
    elif order_info.side == "close/sell":
        side = "CLOSE/LONG"
        if order_info.close_percent == "0":
            f_name = "amount"
            value = order_info.amount
        else:
            f_name = "close_percent"
            value = f"{order_info.close_percent}%"
    msg = f"\n[alert_message]\nexchange: {order_info.exchange}\norder_name: {order_info.order_name}\nsymbol: {order_info.base}/{order_info.quote}\nside: {side}\nprice: {order_info.price}\n{f_name}: {value}"
    logger.info("주문 성공 웹훅메세지"+msg)
    # print(msg)

def log_alert_message(order_info: MarketOrder):
    embed = Embed(
    title = order_info.order_name,
    description="[웹훅 alert_message]",
    color=0xFF0000,
    )
    if order_info.side == "BUY":
        side = "BUY"
        f_name = "amount"
        value = order_info.amount
    elif order_info.side == "SELL":
        side = "SELL"
        if order_info.sell_percent == (None,):
            f_name = "amount"
            value = order_info.amount
        else:
            f_name = "sell_percent"
            value = f"{order_info.sell_percent}%"
    elif order_info.side == "entry/buy":
        side = "LONG"
        f_name = "amount"
        value = order_info.amount
    elif order_info.side == "entry/sell":
        side = "SHORT"
        f_name = "amount"
        value = order_info.amount
    elif order_info.side == "close/buy":
        side = "Close/SHORT"
        if order_info.close_percent == (None,):
            f_name = "amount"
            value = order_info.amount
        else:
            f_name = "close_percent"
            value = f"{order_info.close_percent}%"
    elif order_info.side == "close/sell":
        side = "CLOSE/LONG"
        if order_info.close_percent == (None,):
            f_name = "amount"
            value = order_info.amount
        else:
            f_name = "close_percent"
            value = f"{order_info.close_percent}%"

    embed.add_field("exchange", order_info.exchange, inline=False)
    embed.add_field("order_name", order_info.order_name, inline=False)
    embed.add_field("base", order_info.base, inline=False)
    embed.add_field("quote", order_info.quote, inline=False)
    embed.add_field("price", str(order_info.price), inline = False)
    embed.add_field("side", side, inline=False)
    embed.add_field(f_name, str(value))
    msg = f"\n[alert_message]\nexchange: {order_info.exchange}\norder_name: {order_info.order_name}\nsymbol: {order_info.base}/{order_info.quote}\nside: {side}\nprice: {order_info.price}\n{f_name}: {value}"
    logger.info("주문 실패 웹훅메세지"+msg)
    log_message(embed=embed)