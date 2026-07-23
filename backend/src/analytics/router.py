from fastapi import APIRouter, Depends, status, BackgroundTasks
from fastapi.responses import StreamingResponse
from src.analytics.schemas import AnalyticsPayload, GoalSettings
from src.analytics.service import AnalyticsService
from src.auth.dependencies import get_current_user, get_current_user_sse
from src.sse_manager import sse_manager

router = APIRouter(prefix="/api/analytics", tags=["analytics"])

@router.get("/", response_model=AnalyticsPayload)
def get_dashboard_analytics(current_user=Depends(get_current_user)):
    return AnalyticsService.calculate_user_analytics(user_id=current_user["user_id"])

@router.get("/stream")
async def sse_stream(current_user=Depends(get_current_user_sse)):
    return StreamingResponse(
        sse_manager.event_generator(current_user["user_id"]),
        media_type="text/event-stream"
    )

@router.put("/settings", response_model=GoalSettings, status_code=status.HTTP_200_OK)
def update_financial_goal(settings: GoalSettings, background_tasks: BackgroundTasks, current_user=Depends(get_current_user)):
    saved_goal = AnalyticsService.save_user_goal(current_user["user_id"], settings)
    background_tasks.add_task(sse_manager.notify, current_user["user_id"], "update")
    return saved_goal