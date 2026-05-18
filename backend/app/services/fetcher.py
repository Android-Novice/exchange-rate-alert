import logging
from datetime import datetime
import requests
from sqlalchemy.orm import Session
from app.config import config
from app.models.models import ExchangeRate

logger = logging.getLogger(__name__)

BASE_URL = config["exchange_api"]["base_url"]

CURRENCIES = [
    "USD", "EUR", "JPY", "GBP", "CNY",
    "AUD", "CAD", "CHF", "HKD", "NZD",
    "SEK", "KRW", "SGD", "NOK", "MXN",
    "INR", "RUB", "ZAR", "TRY", "BRL",
]


def fetch_and_store_rates(db: Session) -> dict:
    """从 ExchangeRate-API 拉取 USD 为基准的汇率，存储并返回最新汇率字典。"""
    try:
        resp = requests.get(f"{BASE_URL}/USD", timeout=10)
        resp.raise_for_status()
        data = resp.json()
    except Exception as e:
        logger.error(f"拉取汇率失败: {e}")
        return {}

    if data.get("result") != "success":
        logger.error(f"API 返回错误: {data}")
        return {}

    rates = data.get("rates", {})
    now = datetime.now()

    for currency in CURRENCIES:
        if currency == "USD":
            continue
        if currency not in rates:
            continue
        record = ExchangeRate(
            base_currency="USD",
            target_currency=currency,
            rate=rates[currency],
            fetched_at=now,
        )
        db.add(record)

    db.commit()
    logger.info(f"汇率拉取完成，共 {len(CURRENCIES) - 1} 个货币对")
    return rates
