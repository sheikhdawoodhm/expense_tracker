from fastapi import APIRouter, Depends
from src.finance.schemas import AnalyticsPayload
from src.finance.service import AnalyticsService

router = APIRouter(prefix="/finance", tags=["finance"])

@router.get("/analytics", response_model=AnalyticsPayload)
def get_dashboard_analytics():
    return AnalyticsService.calculate_user_analytics(user_id=1)