from datetime import datetime, timedelta
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.models import AlertLog

router = APIRouter(prefix="/api/alerts", tags=["alerts"])


@router.get("")
def get_alerts(hours: int = 24, db: Session = Depends(get_db)):
    """获取最近的预警记录。"""
    since = datetime.now() - timedelta(hours=hours)
    rows = (
        db.query(AlertLog)
        .filter(AlertLog.created_at >= since)
        .order_by(AlertLog.created_at.desc())
        .limit(50)
        .all()
    )
    return {
        "alerts": [
            {
                "id": a.id,
                "currency_pair": f"{a.base_currency}/{a.target_currency}",
                "old_rate": float(a.old_rate),
                "new_rate": float(a.new_rate),
                "change_percent": float(a.change_percent),
                "direction": "up" if a.new_rate > a.old_rate else "down",
                "sms_sent": bool(a.sms_sent),
                "time": a.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            }
            for a in rows
        ]
    }
