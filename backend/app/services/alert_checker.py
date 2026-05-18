import logging
from datetime import datetime, timedelta
from decimal import Decimal
from sqlalchemy.orm import Session
from app.models.models import ExchangeRate, AlertLog, Subscription
from app.services.sms import send_alert_sms

logger = logging.getLogger(__name__)

ALERT_THRESHOLD = Decimal("0.1")  # 0.1%
CURRENCIES = [
    "EUR", "JPY", "GBP", "CNY", "AUD",
    "CAD", "CHF", "HKD", "NZD", "SEK",
    "KRW", "SGD", "NOK", "MXN", "INR",
    "RUB", "ZAR", "TRY", "BRL",
]


def check_alerts(db: Session):
    """检查所有货币对的波动，超过阈值触发预警。"""
    now = datetime.now()

    for currency in CURRENCIES:
        rows = (
            db.query(ExchangeRate)
            .filter(
                ExchangeRate.base_currency == "USD",
                ExchangeRate.target_currency == currency,
            )
            .order_by(ExchangeRate.fetched_at.desc())
            .limit(2)
            .all()
        )
        if len(rows) < 2:
            continue

        new_rate = rows[0].rate
        old_rate = rows[1].rate

        if old_rate == 0:
            continue

        change_percent = abs((new_rate - old_rate) / old_rate) * 100

        if change_percent > ALERT_THRESHOLD:
            direction = "+" if new_rate > old_rate else "-"
            logger.info(
                f"预警触发: USD/{currency} 波动 {direction}{change_percent:.4f}%"
            )

            alert = AlertLog(
                base_currency="USD",
                target_currency=currency,
                old_rate=old_rate,
                new_rate=new_rate,
                change_percent=change_percent,
                sms_sent=0,
                created_at=now,
            )
            db.add(alert)
            db.flush()

            _notify_subscribers(db, alert, currency, change_percent, new_rate)

    db.commit()


def _notify_subscribers(
    db: Session, alert: AlertLog, currency: str,
    change_percent: Decimal, new_rate: Decimal,
):
    """查询订阅者并发送短信预警（1小时内不重复发送）。"""
    currency_pair = f"USD/{currency}"
    one_hour_ago = datetime.now() - timedelta(hours=1)

    subscribers = (
        db.query(Subscription)
        .filter(
            Subscription.currency_pair == currency_pair,
            Subscription.active == 1,
        )
        .all()
    )

    for sub in subscribers:
        recent_sent = (
            db.query(AlertLog)
            .filter(
                AlertLog.target_currency == currency,
                AlertLog.sms_sent == 1,
                AlertLog.created_at >= one_hour_ago,
            )
            .first()
        )
        if recent_sent:
            logger.info(f"手机号 {sub.phone} 1小时内已收到过短信，跳过")
            continue

        success = send_alert_sms(
            phone=sub.phone,
            currency_pair=currency_pair,
            change_percent=f"{float(change_percent):.4f}",
            current_rate=f"{float(new_rate):.6f}",
        )
        if success:
            alert.sms_sent = 1
            logger.info(f"已向 {sub.phone} 发送短信预警")
