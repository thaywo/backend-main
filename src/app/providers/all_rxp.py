from sqlalchemy import select, func, and_
from datetime import datetime, timedelta
from ..models import models
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from sqlalchemy import select, func, text
from datetime import datetime
from ..models import models
from fastapi import HTTPException, status

async def get_total_rxp(session: AsyncSession):
    try:
        # Query to calculate all-time RXP
        all_time_rxp = await session.execute(
            select(func.coalesce(func.sum(models.ActivityPoint.__table__.c["PointsEarned"]), 0))
        )
        all_time_rxp = all_time_rxp.scalar()

        # Query to calculate this week's RXP
        this_week_rxp = await session.execute(
            select(func.coalesce(func.sum(models.ActivityPoint.__table__.c["PointsEarned"]), 0))
            .where(models.ActivityPoint.__table__.c["CreatedAt"] >= text("date_trunc('week', CURRENT_DATE)"))
        )
        this_week_rxp = this_week_rxp.scalar()

        # Query to calculate this month's RXP
        this_month_rxp = await session.execute(
            select(func.coalesce(func.sum(models.ActivityPoint.__table__.c["PointsEarned"]), 0))
            .where(models.ActivityPoint.__table__.c["CreatedAt"] >= text("date_trunc('month', CURRENT_DATE)"))
        )
        this_month_rxp = this_month_rxp.scalar()

        return {
            "all_time_RXP": all_time_rxp,
            "this_weeks_RXP": this_week_rxp,
            "this_months_RXP": this_month_rxp
        }
    except Exception as e:
        print(f"Error calculating total RXP: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error"
        )