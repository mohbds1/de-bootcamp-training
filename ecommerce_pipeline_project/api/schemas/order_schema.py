from datetime import datetime
from typing import Dict, List

from pydantic import BaseModel, ConfigDict


class OrderResponse(BaseModel):
    order_id: int
    user_id: int
    product_id: int
    quantity: int
    price: float
    status: str
    created_at: datetime
    processed_at: datetime

    model_config = ConfigDict(from_attributes=True)


class OrderStatsResponse(BaseModel):
    orders_last_hour: int
    total_sales: float
    status_distribution: Dict[str, int]


class LatestOrdersResponse(BaseModel):
    orders: List[OrderResponse]
