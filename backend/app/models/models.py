from sqlalchemy import Column, Integer, String, DECIMAL, DateTime, Index
from sqlalchemy.sql import func
from app.database import Base


class ExchangeRate(Base):
    __tablename__ = "exchange_rates"

    id = Column(Integer, primary_key=True, autoincrement=True)
    base_currency = Column(String(3), nullable=False)
    target_currency = Column(String(3), nullable=False)
    rate = Column(DECIMAL(18, 8), nullable=False)
    fetched_at = Column(DateTime, nullable=False, server_default=func.now())

    __table_args__ = (
        Index("idx_currency_pair", "base_currency", "target_currency"),
        Index("idx_fetched_at", "fetched_at"),
    )


class Subscription(Base):
    __tablename__ = "subscriptions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    phone = Column(String(20), nullable=False, unique=True)
    currency_pair = Column(String(10), nullable=False)
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    active = Column(Integer, nullable=False, default=1)


class AlertLog(Base):
    __tablename__ = "alert_logs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    base_currency = Column(String(3), nullable=False)
    target_currency = Column(String(3), nullable=False)
    old_rate = Column(DECIMAL(18, 8), nullable=False)
    new_rate = Column(DECIMAL(18, 8), nullable=False)
    change_percent = Column(DECIMAL(8, 4), nullable=False)
    sms_sent = Column(Integer, nullable=False, default=0)
    created_at = Column(DateTime, nullable=False, server_default=func.now())

    __table_args__ = (
        Index("idx_alert_created_at", "created_at"),
    )
