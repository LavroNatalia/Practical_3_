from decimal import Decimal
from sqlalchemy import Integer, String, Text, Numeric, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True
    )
    category_id: Mapped[int] = mapped_column(
        ForeignKey("categories.id")
    )
    name: Mapped[str] = mapped_column(String(150))
    brand: Mapped[str] = mapped_column(String(100))
    description: Mapped[str | None] = mapped_column(Text)
    price: Mapped[Decimal] = mapped_column(Numeric(10, 2))
    volume: Mapped[int] = mapped_column(Integer)
    stock: Mapped[int] = mapped_column(Integer)