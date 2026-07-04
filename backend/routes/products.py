from decimal import Decimal

from fastapi import APIRouter, HTTPException, status

from models.product import Product
from repositories.product_repository import ProductRepository
from schemas.product_schema import ProductCreate, ProductResponse, ProductUpdate

router = APIRouter(
    prefix="/products",
    tags=["Products"],
)

repo = ProductRepository()


@router.get("", response_model=list[ProductResponse])
def find_all_products():
    products = repo.find_all()
    return [product.to_dict() for product in products]


@router.get("/{product_id}", response_model=ProductResponse)
def find_product_by_id(product_id: int):
    product = repo.find_by_id(product_id)

    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")

    return product.to_dict()


@router.post("", status_code=status.HTTP_201_CREATED)
def create_product(payload: ProductCreate):
    try:
        product = Product(
            name=payload.name,
            category=payload.category,
            price=payload.price,
        )

        new_id = repo.create(product)

        return {
            "message": "Product created successfully",
            "product_id": new_id,
        }

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/{product_id}")
def update_product(product_id: int, payload: ProductUpdate):
    existing = repo.find_by_id(product_id)

    if existing is None:
        raise HTTPException(status_code=404, detail="Product not found")

    try:
        product = Product(
            product_id=product_id,
            name=payload.name,
            category=payload.category,
            price=payload.price,
        )

        updated = repo.update(product)

        if not updated:
            raise HTTPException(status_code=404, detail="Product not found")

        return {"message": "Product updated successfully"}

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{product_id}")
def delete_product(product_id: int):
    try:
        deleted = repo.delete(product_id)

        if not deleted:
            raise HTTPException(status_code=404, detail="Product not found")

        return {"message": "Product deleted successfully"}

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
