from sqlalchemy import Column, BigInteger, Integer, Float, Text, TIMESTAMP, text

from api.database.database import Base


class CleanOrder(Base):
    __tablename__ = "clean_orders"

    order_id = Column(BigInteger, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    product_id = Column(Integer, nullable=False)
    quantity = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)
    status = Column(Text, nullable=False)
    created_at = Column(TIMESTAMP, nullable=False)
    processed_at = Column(TIMESTAMP, nullable=False, server_default=text("NOW()"))
