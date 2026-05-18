import threading
import time
import logging
import schedule
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import engine, SessionLocal, Base
from app.models.models import ExchangeRate, Subscription, AlertLog
from app.routers import rates, subscriptions, alerts
from app.services.fetcher import fetch_and_store_rates
from app.services.alert_checker import check_alerts

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

app = FastAPI(title="全球货币汇率监控", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(rates.router)
app.include_router(subscriptions.router)
app.include_router(alerts.router)


@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)
    t = threading.Thread(target=_scheduler_loop, daemon=True)
    t.start()


def _scheduler_loop():
    """后台定时任务：每小时拉取汇率并检测波动。"""
    time.sleep(2)
    _fetch_job()
    schedule.every().hour.do(_fetch_job)

    while True:
        schedule.run_pending()
        time.sleep(1)


def _fetch_job():
    try:
        db = SessionLocal()
        rates = fetch_and_store_rates(db)
        if rates:
            check_alerts(db)
        db.close()
    except Exception as e:
        logger.error(f"定时任务异常: {e}")


@app.get("/")
def root():
    return {"service": "全球货币汇率监控", "status": "running"}
