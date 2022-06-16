from pydantic import BaseModel, BaseSettings, Field, validator
from typing import Literal
import os
env = "dev" if os.path.exists("dev.env") else "prod"


class Settings(BaseSettings):
    PASSWORD: str
    UPBIT_KEY: str | None = None
    UPBIT_SECRET: str | None = None
    BINANCE_KEY: str | None = None
    BINANCE_SECRET: str | None = None
    DISCORD_WEBHOOK_URL: str | None = None
    WHITELIST: list[str] | None = None

    class Config:
        env_file = '.env' if env == "prod" else 'dev.env'
        env_file_encoding = "utf-8"


class OrderBase(BaseModel):
    password: str
    exchange: Literal["UPBIT", "BINANCE"]
    base: str
    quote: Literal["KRW", "USDT", "USDTPERP"]
    type: Literal["MARKET", "LIMIT"]
    side: Literal["BUY", "SELL", "entry/buy", "entry/sell", "close/buy", "close/sell"]
    amount: float
    price: float
    cost: float | None = None,
    sell_percent: str | None = None,
    close_percent: str | None = None,
    leverage: int = 0,
    order_name: str = "주문"

    @validator("password")
    def password_validate(cls, v):
        setting = Settings()
        if v != setting.PASSWORD:
            raise ValueError("비밀번호가 틀렸습니다")
        return v


class MarketOrder(OrderBase):
    price: float | None = None
    type: Literal["MARKET"] = "MARKET"


class MarketBuyOrder(MarketOrder):
    side: Literal['BUY'] = "BUY"


class MarketSellOrder(MarketOrder):
    price: float = None
    side: Literal['SELL'] = "SELL"
    sell_percent: str
