from fastapi import APIRouter, HTTPException
from repositories.dashboard_repository import DashboardRepository

router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"],
)

repo = DashboardRepository()


@router.get("")
def get_dashboard_metrics():
    try:
        return repo.get_monthly_dashboard()
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to fetch dashboard metrics: {str(e)}",
        )
