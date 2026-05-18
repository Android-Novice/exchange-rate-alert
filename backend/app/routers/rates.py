from datetime import datetime, timedelta
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.models import ExchangeRate

router = APIRouter(prefix="/api/rates", tags=["rates"])

CURRENCIES = [
    "USD", "EUR", "JPY", "GBP", "CNY",
    "AUD", "CAD", "CHF", "HKD", "NZD",
    "SEK", "KRW", "SGD", "NOK", "MXN",
    "INR", "RUB", "ZAR", "TRY", "BRL",
]


@router.get("/currencies")
def get_currencies():
    return {"currencies": CURRENCIES}


@router.get("/latest")
def get_latest_rates(db: Session = Depends(get_db)):
    """获取最新汇率（每种货币取最新一条）。"""
    from sqlalchemy import func as sql_func

    sub = (
        db.query(
            ExchangeRate.target_currency,
            sql_func.max(ExchangeRate.fetched_at).label("max_time"),
        )
        .filter(ExchangeRate.base_currency == "USD")
        .group_by(ExchangeRate.target_currency)
        .subquery()
    )

    rows = (
        db.query(ExchangeRate)
        .join(
            sub,
            (ExchangeRate.target_currency == sub.c.target_currency)
            & (ExchangeRate.fetched_at == sub.c.max_time),
        )
        .all()
    )

    rates = {}
    for r in rows:
        rates[r.target_currency] = {
            "rate": float(r.rate),
            "fetched_at": r.fetched_at.strftime("%Y-%m-%d %H:%M:%S"),
        }
    return {"base": "USD", "rates": rates}


@router.get("/history")
def get_rate_history(
    from_currency: str = "USD",
    to_currency: str = "CNY",
    hours: int = 24,
    db: Session = Depends(get_db),
):
    """获取指定货币对的历史汇率。"""
    since = datetime.now() - timedelta(hours=hours)
    rows = (
        db.query(ExchangeRate)
        .filter(
            ExchangeRate.base_currency == from_currency,
            ExchangeRate.target_currency == to_currency,
            ExchangeRate.fetched_at >= since,
        )
        .order_by(ExchangeRate.fetched_at.desc())
        .limit(100)
        .all()
    )
    return {
        "base": from_currency,
        "target": to_currency,
        "history": [
            {
                "rate": float(r.rate),
                "time": r.fetched_at.strftime("%Y-%m-%d %H:%M:%S"),
            }
            for r in rows
        ],
    }


def _get_usd_rate(db: Session, target: str):
    """获取某货币对 USD 的最新汇率。"""
    row = (
        db.query(ExchangeRate)
        .filter(ExchangeRate.target_currency == target)
        .order_by(ExchangeRate.fetched_at.desc())
        .first()
    )
    return float(row.rate) if row else None


def _get_usd_rate_24h_ago(db: Session, target: str):
    """获取某货币对 USD 在 24 小时前的汇率。"""
    yesterday = datetime.now() - timedelta(hours=24)
    row = (
        db.query(ExchangeRate)
        .filter(
            ExchangeRate.target_currency == target,
            ExchangeRate.fetched_at <= yesterday,
        )
        .order_by(ExchangeRate.fetched_at.desc())
        .first()
    )
    return float(row.rate) if row else None


@router.get("/convert")
def convert_rate(
    from_currency: str = "USD",
    to_currency: str = "CNY",
    amount: float = 1.0,
    db: Session = Depends(get_db),
):
    """根据最新汇率换算两个货币之间的汇率，含 24h 涨跌幅。"""
    if from_currency == to_currency:
        return {"rate": 1.0, "amount": amount, "change_24h": 0.0}

    # Calculate current cross rate
    current_rate = _calc_cross_rate(db, from_currency, to_currency)
    if current_rate is None:
        return {"error": "汇率数据不可用"}

    # Calculate 24h ago cross rate
    change_24h = _calc_24h_change(db, from_currency, to_currency, current_rate)

    return {
        "rate": current_rate,
        "amount": amount * current_rate,
        "fetched_at": _get_latest_fetch_time(db, from_currency, to_currency),
        "change_24h": round(change_24h, 6) if change_24h is not None else None,
        "rate_24h_ago": _calc_cross_rate_24h(db, from_currency, to_currency),
    }


def _calc_cross_rate(db: Session, from_currency: str, to_currency: str):
    """计算当前交叉汇率。"""
    if from_currency == "USD":
        rate = _get_usd_rate(db, to_currency)
        return rate
    if to_currency == "USD":
        rate = _get_usd_rate(db, from_currency)
        return 1.0 / rate if rate else None
    from_rate = _get_usd_rate(db, from_currency)
    to_rate = _get_usd_rate(db, to_currency)
    if from_rate and to_rate:
        return to_rate / from_rate
    return None


def _calc_cross_rate_24h(db: Session, from_currency: str, to_currency: str):
    """计算 24 小时前的交叉汇率。"""
    if from_currency == "USD":
        rate = _get_usd_rate_24h_ago(db, to_currency)
        return rate
    if to_currency == "USD":
        rate = _get_usd_rate_24h_ago(db, from_currency)
        return 1.0 / rate if rate else None
    from_rate = _get_usd_rate_24h_ago(db, from_currency)
    to_rate = _get_usd_rate_24h_ago(db, to_currency)
    if from_rate and to_rate:
        return to_rate / from_rate
    return None


def _calc_24h_change(db: Session, from_currency: str, to_currency: str, current_rate: float):
    """计算 24h 涨跌幅百分比。"""
    old_rate = _calc_cross_rate_24h(db, from_currency, to_currency)
    if old_rate and old_rate != 0:
        return ((current_rate - old_rate) / old_rate) * 100
    return None


def _get_latest_fetch_time(db: Session, from_currency: str, to_currency: str):
    """获取最新数据的拉取时间。"""
    if from_currency == "USD":
        target = to_currency
    elif to_currency == "USD":
        target = from_currency
    else:
        target = to_currency
    row = (
        db.query(ExchangeRate)
        .filter(ExchangeRate.target_currency == target)
        .order_by(ExchangeRate.fetched_at.desc())
        .first()
    )
    return row.fetched_at.strftime("%Y-%m-%d %H:%M:%S") if row else None
