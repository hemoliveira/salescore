from fastapi import APIRouter

router = APIRouter(
    prefix="/health",
    tags=["System"],
)


@router.get("")
def health_check():
    return {
        "status": "healthy",
        "service": "customer-product-order-api",
    }
