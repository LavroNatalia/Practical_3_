from datetime import datetime
from decimal import Decimal
from sqlalchemy import Integer, String, DateTime, Numeric, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class Order(Base):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True
    )
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id")
    )
    order_date: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.now
    )
    status: Mapped[str] = mapped_column(
        String(50), default="pending"
    )
    total_price: Mapped[Decimal] = mapped_column(Numeric(10, 2))
    delivery_address: Mapped[str] = mapped_column(String(255))