from fastapi import APIRouter, HTTPException, status
from core.database import DatabaseManager

router = APIRouter(
    prefix="/health",
    tags=["System"],
)


@router.get("")
def health_check():
    try:
        # Perform a lightweight ping to the database
        DatabaseManager.fetch_one("SELECT 1")
        db_status = "connected"
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database connection is unavailable",
        )

    return {
        "status": "healthy",
        "database": db_status,
        "service": "customer-product-order-api",
    }
