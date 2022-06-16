from fastapi.exception_handlers import (
    request_validation_exception_handler,
)
from fastapi import FastAPI, Depends, HTTPException, Request, status, BackgroundTasks
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.exceptions import RequestValidationError
from requests import request
from exchange import Upbit, Binance
from model import MarketOrder, BaseModel
from utility import settings, log_message, log_order_message
app = FastAPI()

whitelist = ["52.89.214.238", "34.212.75.30",
             "54.218.53.128", "52.32.178.7", "127.0.0.1"]
whitelist = whitelist + settings.WHITELIST


class Exchange(BaseModel):
    UPBIT: Upbit | None = None
    BINANCE: Binance | None = None

    class Config:
        arbitrary_types_allowed = True


@app.middleware('http')
async def settings_whitelist_middleware(request: Request, call_next):
    if request.client.host not in whitelist:
        msg = f"{request.client.host}는 안됩니다"
        print(msg)
        return JSONResponse(status_code=status.HTTP_403_FORBIDDEN, content=f"{request.client.host} Not Allowed")
    response = await call_next(request)
    return response


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    msgs = [f"[에러{index+1}] "+error.get("msg")
            for index, error in enumerate(exc.errors())]
    message = "[Error]\n"
    for msg in msgs:
        message = message+msg+"\n"

    log_message(f"{message}\n {exc.body}")
    return await request_validation_exception_handler(request, exc)


def check_key(exchange_name):
    key = settings.dict().get(exchange_name+"_KEY")
    secret = settings.dict().get(exchange_name+"_SECRET")
    if not key:
        msg = f"{exchange_name}_KEY가 없습니다"
        log_message(msg)
        raise HTTPException(
            status_code=404, detail=msg)
    elif not secret:
        msg = f"{exchange_name}_SECRET가 없습니다"
        log_message(msg)
        raise HTTPException(
            status_code=404, detail=msg)
    return key, secret


@app.get("/ip")
async def get_ip():
    data = request("get", "https://ifconfig.me").text
    log_message(data)
    return data


@ app.get("/hi")
async def welcome():
    return "hi!!"

@ app.get("/honey")
async def welcome():
    return RedirectResponse("https://finlife.fss.or.kr/deposit/selectDeposit.do?menuId=2000100")


@ app.post("/order")
async def order(order_info: MarketOrder, background_tasks: BackgroundTasks):
    result = None
    try:
        exchange_name = order_info.exchange.upper()
        KEY, SECRET = check_key(exchange_name)
        payload = {exchange_name: globals(
        )[exchange_name.title()](KEY, SECRET)}
        exchange = Exchange(**payload)

        if order_info.side == "BUY":
            result = exchange.dict()[order_info.exchange].market_buy(order_info)
        elif order_info.side == "SELL":
            result = exchange.dict()[order_info.exchange].market_sell(order_info)
        elif order_info.side.startswith("entry/"):
            result = exchange.dict()[order_info.exchange].market_entry(order_info)
        elif order_info.side.startswith("close/"):
            result = exchange.dict()[order_info.exchange].market_close(order_info)
        log_order_message(exchange_name, result)

    except Exception as e:
        log_message(f"[Error]\n{e}")

    finally:
        if order_info.side == "BUY":
            msg = f"[alert_message]\nExchange: {order_info.exchange}\nOrderName: {order_info.order_name}\nSymbol: {order_info.base}/{order_info.quote}\nSide: {order_info.side}\nPrice: {order_info.price}\nAmount: {order_info.amount}"
        elif order_info.side == "SELL":
            msg = f"[alert_message]\nExchange: {order_info.exchange}\nOrderName: {order_info.order_name}\nSymbol: {order_info.base}/{order_info.quote}\nSide: {order_info.side}\nPrice: {order_info.price}\nPercent: {order_info.sell_percent}"
        elif order_info.side == "entry/buy":
            msg = f"[alert_message]\nExchange: {order_info.exchange}\nOrderName: {order_info.order_name}\nSymbol: {order_info.base}/{order_info.quote}\nSide: LONG\nPrice:{order_info.price}\nAmount: {order_info.amount}"
        elif order_info.side == "entry/sell":
            msg = f"[alert_message]\nExchange: {order_info.exchange}\nOrderName: {order_info.order_name}\nSymbol: {order_info.base}/{order_info.quote}\nSide: SHORT\nPrice:{order_info.price}\nAmount: {order_info.amount}"
        elif order_info.side == "close/buy":
            msg = f"[alert_message]\nExchange: {order_info.exchange}\nOrderName: {order_info.order_name}\nSymbol: {order_info.base}/{order_info.quote}\nSide: Close LONG\nPrice:{order_info.price}\nPercent: {order_info.close_percent}"
        elif order_info.side == "close/sell":
            msg = f"[alert_message]\nExchange: {order_info.exchange}\nOrderName: {order_info.order_name}\nSymbol: {order_info.base}/{order_info.quote}\nSide: Close SHORT\nPrice: {order_info.price}\nPercent: {order_info.close_percent}"
        background_tasks.add_task(log_message, msg)
