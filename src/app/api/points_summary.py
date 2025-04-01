from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from ..config.database_config import async_get_db
from ..providers.points_summary import get_points_summary  # Import the function
from ..schemas import schemas

router = APIRouter(prefix="/all", tags=["points-summary"])

@router.get("/points-summary", response_model=schemas.PointsSummaryResponse)
async def points_summary_endpoint(db: AsyncSession = Depends(async_get_db)):
    return await get_points_summary(db)