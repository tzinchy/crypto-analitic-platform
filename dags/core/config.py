from dataclasses import dataclass
from dotenv import load_dotenv
import os

# Загружаем переменные из .env файла
load_dotenv()

BINANCE_API_URL_CURRENT_COIN_PRICE = f"https://api.bitget.com/api/v2/mix/market/fills?symbol=*&productType=usdt-futures"

BINANCE_PAIRS = {
    "BTCUSDT": 1,
    "ETHUSDT": 2,
    "SOLUSDT": 3,
    "XRPUSDT": 4,
    "LTCUSDT": 5
}

@dataclass
class Settings:
    DB_HOST: str = os.environ.get("DB_HOST")
    DB_PORT: str = os.environ.get("DB_PORT")
    DB_USER: str = os.environ.get("DB_USER")
    DB_PASSWORD: str = os.environ.get("DB_PASS")
    DB_NAME: str = os.environ.get("DB_NAME")
    DB_SCHEMA: str = os.environ.get("DB_SCHEMA")

    @property
    def DATABASE_URL(self) -> str:
        return f"postgresql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

settings = Settings()
print(settings.DATABASE_URL)