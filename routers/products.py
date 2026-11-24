import logging
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from settings.db import get_db
from models.product import Product
from schemas.product import ProductCreate, ProductRead, ProductUpdate

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/products", tags=["Products"])

SessionDepend = Annotated[AsyncSession, Depends(get_db)]


@router.get("/", response_model=list[ProductRead])
async def get_products(session: SessionDepend):
    try:
        result = await session.execute(select(Product))
        return result.scalars().all()
    except HTTPException:
        raise
    except Exception as exc:
        logger.exception("Failed to get products")
        raise HTTPException(
            status_code=500,
            detail="Failed to get products",
        ) from exc


@router.get("/{product_id}", response_model=ProductRead)
async def get_product(product_id: int, session: SessionDepend):
    try:
        product = await session.get(Product, product_id)

        if not product:
            raise HTTPException(
                status_code=404,
                detail="Product not found",
            )

        return product
    except HTTPException:
        raise
    except Exception as exc:
        logger.exception("Failed to get product")
        raise HTTPException(
            status_code=500,
            detail="Failed to get product",
        ) from exc


@router.post(
    "/",
    response_model=ProductRead,
    status_code=201,
)
async def create_product(
    product_data: ProductCreate,
    session: SessionDepend,
):
    try:
        new_product = Product(**product_data.model_dump())
        session.add(new_product)
        await session.commit()
        await session.refresh(new_product)
        return new_product
    except HTTPException:
        raise
    except Exception as exc:
        logger.exception("Failed to create product")
        raise HTTPException(
            status_code=500,
            detail="Failed to create product",
        ) from exc


@router.put("/{product_id}", response_model=ProductRead)
async def update_product(
    product_id: int,
    product_update: ProductUpdate,
    session: SessionDepend,
):
    try:
        product = await session.get(Product, product_id)

        if not product:
            raise HTTPException(
                status_code=404,
                detail="Product not found",
            )

        for field, value in product_update.model_dump(
            exclude_unset=True
        ).items():
            if value is None and field != "description":
                raise HTTPException(
                    status_code=422,
                    detail=f"{field} cannot be null",
                )
            setattr(product, field, value)

        await session.commit()
        await session.refresh(product)
        return product
    except HTTPException:
        raise
    except Exception as exc:
        logger.exception("Failed to update product")
        raise HTTPException(
            status_code=500,
            detail="Failed to update product",
        ) from exc


@router.delete("/{product_id}", status_code=204)
async def delete_product(
    product_id: int,
    session: SessionDepend,
):
    try:
        product = await session.get(Product, product_id)

        if not product:
            raise HTTPException(
                status_code=404,
                detail="Product not found",
            )

        await session.delete(product)
        await session.commit()
        return None
    except HTTPException:
        raise
    except Exception as exc:
        logger.exception("Failed to delete product")
        raise HTTPException(
            status_code=500,
            detail="Failed to delete product",
        ) from exc