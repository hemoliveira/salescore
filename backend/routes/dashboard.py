from fastapi import APIRouter
from repositories.dashboard_repository import DashboardRepository

router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"],
)

repo = DashboardRepository()


@router.get("")
def get_dashboard_metrics():
    return repo.get_monthly_dashboard()
