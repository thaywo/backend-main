from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from starlette import status
from ..models import models
from ..schemas import schemas

async def get_points_summary(session: AsyncSession):
    try:
        # Get the total points accrued by all users
        total_points_result = await session.execute(
            select(func.sum(models.ActivityPoint.PointsEarned))
        )
        total_points = total_points_result.scalar() or 0

        # Get the breakdown by quest
        quest_summary_result = await session.execute(
            select(
                models.Quest.QuestId,
                models.Quest.Title,
                func.count(models.ActivityPoint.QuestId).label("total_completions"),
                func.sum(models.ActivityPoint.PointsEarned).label("total_points")
            )
            .join(models.ActivityPoint, models.ActivityPoint.QuestId == models.Quest.QuestId, isouter=True)
            .group_by(models.Quest.QuestId, models.Quest.Title)
        )
        quest_summary = quest_summary_result.all()

        # If no quests are found, return an empty list
        if not quest_summary:
            return {
                "total_points": total_points,
                "quests": []
            }

        # Format the response
        quests = [
            schemas.QuestSummary(
                quest_id=row.QuestId,
                quest_title=row.Title,
                total_completions=row.total_completions or 0,
                total_points=row.total_points or 0
            )
            for row in quest_summary
        ]

        return {
            "total_points": total_points,
            "quests": quests
        }
    except Exception as e:
        print(f"Error in get_points_summary: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error"
        )