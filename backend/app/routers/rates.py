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


@router.get("/convert")
def convert_rate(
    from_currency: str = "USD",
    to_currency: str = "CNY",
    amount: float = 1.0,
    db: Session = Depends(get_db),
):
    """根据最新汇率换算两个货币之间的汇率。"""
    if from_currency == to_currency:
        return {"rate": 1.0, "amount": amount}

    if from_currency == "USD":
        row = (
            db.query(ExchangeRate)
            .filter(ExchangeRate.target_currency == to_currency)
            .order_by(ExchangeRate.fetched_at.desc())
            .first()
        )
        if row:
            rate = float(row.rate)
            return {"rate": rate, "amount": amount * rate, "fetched_at": row.fetched_at.strftime("%Y-%m-%d %H:%M:%S")}

    if to_currency == "USD":
        row = (
            db.query(ExchangeRate)
            .filter(ExchangeRate.target_currency == from_currency)
            .order_by(ExchangeRate.fetched_at.desc())
            .first()
        )
        if row:
            rate = 1.0 / float(row.rate)
            return {"rate": rate, "amount": amount * rate, "fetched_at": row.fetched_at.strftime("%Y-%m-%d %H:%M:%S")}

    from_row = (
        db.query(ExchangeRate)
        .filter(ExchangeRate.target_currency == from_currency)
        .order_by(ExchangeRate.fetched_at.desc())
        .first()
    )
    to_row = (
        db.query(ExchangeRate)
        .filter(ExchangeRate.target_currency == to_currency)
        .order_by(ExchangeRate.fetched_at.desc())
        .first()
    )
    if from_row and to_row:
        rate = float(to_row.rate) / float(from_row.rate)
        return {"rate": rate, "amount": amount * rate, "fetched_at": to_row.fetched_at.strftime("%Y-%m-%d %H:%M:%S")}

    return {"error": "汇率数据不可用"}
