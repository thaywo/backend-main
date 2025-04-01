# Quick check script - run this in your Python shell
from app.config.database_config import async_get_db
from sqlalchemy import select, and_
from .app.models import models
async def check_quest_completion():
    db = await async_get_db()
    result = await db.execute(
        select(models.ActivityPoint)
        .join(models.User)
        .where(
            and_(
                models.User.PublicAddress == "0xabcdef1234567890abcdef1234567890abcdef12",
                models.ActivityPoint.QuestId == "3e834fc3-cdfb-40d9-b43c-b43557b5c72f"
            )
        )
    )
    return result.scalars().first()

# Run this
completion_record = await check_quest_completion()
print(completion_record)