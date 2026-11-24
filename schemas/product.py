from decimal import Decimal
from pydantic import BaseModel, Field, ConfigDict


class ProductCreate(BaseModel):
    category_id: int = Field(gt=0)
    name: str = Field(min_length=1, max_length=150)
    brand: str = Field(max_length=100)
    description: str | None = None
    price: Decimal = Field(gt=0, max_digits=10, decimal_places=2)
    volume: int = Field(gt=0)
    stock: int = Field(ge=0)


class ProductRead(ProductCreate):
    id: int

    model_config = ConfigDict(from_attributes=True)


class ProductUpdate(BaseModel):
    category_id: int | None = Field(default=None, gt=0)
    name: str | None = Field(default=None, min_length=1, max_length=150)
    brand: str | None = Field(default=None, max_length=100)
    description: str | None = None
    price: Decimal | None = Field(default=None, gt=0, max_digits=10, decimal_places=2)
    volume: int | None = Field(default=None, gt=0)
    stock: int | None = Field(default=None, ge=0)