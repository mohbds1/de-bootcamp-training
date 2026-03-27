from datetime import datetime, timedelta

from fastapi import APIRouter, Depends
from sqlalchemy import func
from sqlalchemy.orm import Session

from api.database.database import get_db
from api.models.order import CleanOrder
from api.schemas.order_schema import LatestOrdersResponse, OrderStatsResponse

router = APIRouter(prefix="/orders", tags=["Orders"])


@router.get("/latest", response_model=LatestOrdersResponse)
def get_latest_orders(db: Session = Depends(get_db)):
    orders = (
        db.query(CleanOrder)
        .order_by(CleanOrder.created_at.desc())
        .limit(10)
        .all()
    )
    return {"orders": orders}


@router.get("/stats", response_model=OrderStatsResponse)
def get_order_stats(db: Session = Depends(get_db)):
    one_hour_ago = datetime.now() - timedelta(hours=1)

    recent_orders = db.query(CleanOrder).filter(CleanOrder.created_at >= one_hour_ago)

    orders_last_hour = recent_orders.count()
    total_sales = (
        recent_orders.with_entities(func.coalesce(func.sum(CleanOrder.quantity * CleanOrder.price), 0.0)).scalar()
        or 0.0
    )

    status_rows = (
        recent_orders.with_entities(CleanOrder.status, func.count(CleanOrder.order_id))
        .group_by(CleanOrder.status)
        .all()
    )
    status_distribution = {status: count for status, count in status_rows}

    return {
        "orders_last_hour": orders_last_hour,
        "total_sales": round(float(total_sales), 2),
        "status_distribution": status_distribution,
    }
