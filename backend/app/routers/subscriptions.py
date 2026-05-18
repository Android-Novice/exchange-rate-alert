from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.models import Subscription

router = APIRouter(prefix="/api/subscriptions", tags=["subscriptions"])


class SubscribeRequest(BaseModel):
    phone: str
    currency_pair: str


@router.post("")
def subscribe(req: SubscribeRequest, db: Session = Depends(get_db)):
    """订阅短信预警。"""
    existing = (
        db.query(Subscription)
        .filter(Subscription.phone == req.phone, Subscription.active == 1)
        .first()
    )
    if existing:
        raise HTTPException(status_code=400, detail="该手机号已订阅")

    sub = Subscription(
        phone=req.phone,
        currency_pair=req.currency_pair,
        created_at=datetime.now(),
        active=1,
    )
    db.add(sub)
    db.commit()
    return {"message": "订阅成功", "phone": req.phone}


@router.delete("/{phone}")
def unsubscribe(phone: str, db: Session = Depends(get_db)):
    """取消订阅。"""
    sub = (
        db.query(Subscription)
        .filter(Subscription.phone == phone, Subscription.active == 1)
        .first()
    )
    if not sub:
        raise HTTPException(status_code=404, detail="订阅不存在")

    sub.active = 0
    db.commit()
    return {"message": "取消订阅成功"}
