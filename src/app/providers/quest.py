from datetime import datetime, timedelta, timezone

from fastapi import HTTPException
from sqlalchemy import and_, delete, func, select, or_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from starlette import status
from ..schemas import schemas
from ..models import models

async def add_quest(
    session: AsyncSession,
    payload: schemas.AddQuestDTO
):
    try:
        check_quest = await session.execute(
            select(models.Quest).where(models.Quest.Title == payload.Title)
        )
        get_quest = check_quest.scalars().first()
        if get_quest != None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Quest already exists"
            )
        print("Hello")
        new_quest = models.Quest(
            Title = payload.Title,
            ContractAddress = payload.ContractAddress,
            Description = payload.Description,
            Reward = payload.Reward,
            Image = str(payload.Image)
        )
        session.add(new_quest)
        await session.commit()
        await session.refresh(new_quest)
        validate_quest = schemas.QuestResponseDTO.model_validate(new_quest)
        return {
            "success": True,
            "status_code": status.HTTP_201_CREATED,
            "message": "Quest added successfully",
            "data": validate_quest
        }
    except HTTPException as e:
        return {
            "success": False,
            "status_code": e.status_code,
            "message": e.detail,
            "data": None
        }
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error"
        )
    
async def get_quests(session: AsyncSession, start: int, end: int):
    try:
        # Calculate the limit and offset based on start and end
        limit = end - start + 1  # Number of records to fetch
        offset = start - 1       # Starting point (SQL offset is 0-based)

        # Fetch quests within the specified range
        get_quests = await session.execute(
            select(models.Quest)
            .where(models.Quest.is_deleted == False)
            .offset(offset)  # Skip records before the start
            .limit(limit)    # Fetch only the specified number of records
        )
        quests = get_quests.scalars().all()

        # Fetch total count of quests (for metadata)
        total_quests = await session.execute(
            select(func.count()).select_from(models.Quest)
            .where(models.Quest.is_deleted == False)
        )
        total_quests = total_quests.scalar()

        # If no quests are found, return an empty list
        if not quests:
            return {
                "success": True,
                "status_code": status.HTTP_200_OK,
                "message": "Quests fetched successfully",
                "data": [],
                "pagination": {
                    "total": total_quests,
                    "start": start,
                    "end": end
                }
            }

        # Return paginated quests with metadata
        return {
            "success": True,
            "status_code": status.HTTP_200_OK,
            "message": "Quests fetched successfully",
            "data": quests,
            "pagination": {
                "total": total_quests,
                "start": start,
                "end": end
            }
        }
    except HTTPException as e:
        return {
            "success": False,
            "status_code": e.status_code,
            "message": e.detail,
            "data": None
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error"
        )
        
async def get_quest_by_id(session: AsyncSession, questId: str):
    try:
        get_quest = await session.execute(
            select(models.Quest).where(
                and_(
                    models.Quest.QuestId == questId,
                    models.Quest.is_deleted == False
                )
            )
        )
        quest = get_quest.scalars().first()
        if quest is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Quest not found"
            )
        return {
            "success": True,
            "status_code": status.HTTP_200_OK,
            "message": "Quest fetched successfully",
            "data": quest
        }
    except HTTPException as e:
        return {
            "success": False,
            "status_code": e.status_code,
            "message": e.detail,
            "data": None
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error"
        )
        
async def update_quest(session: AsyncSession, questId: str, payload: schemas.UpdateQuestDTO):
    try:
        get_quest = await session.execute(
            select(models.Quest).where(models.Quest.QuestId == questId)
        )
        quest = get_quest.scalars().first()
        if quest is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Quest not found"
            )
        quest.UpdatedAt = datetime.now()
        update_data = payload.model_dump(exclude_none=True, exclude_unset=True)
        for key, value in update_data.items():
            setattr(quest, key, value)
        validate_quest = schemas.QuestResponseDTO.model_validate(quest).model_dump()
        await session.commit()
        return {
            "success": True,
            "status_code": status.HTTP_200_OK,
            "message": "Quest updated successfully",
            "data": validate_quest
        }
    except HTTPException as e:
        return {
            "success": False,
            "status_code": e.status_code,
            "message": e.detail,
            "data": None
        }
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error"
        )

async def delete_quest(session: AsyncSession, questId: str):
    try:
        get_quest = await session.execute(
            select(models.Quest).where(models.Quest.QuestId == questId)
        )
        quest = get_quest.scalars().first()
        if quest is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Quest not found"
            )
        quest.is_deleted = True
        await session.commit()
        return {
            "success": True,
            "status_code": status.HTTP_200_OK,
            "message": "Quest deleted successfully",
            "data": None
        }
    except HTTPException as e:
        return {
            "success": False,
            "status_code": e.status_code,
            "message": e.detail,
            "data": None
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error"
        )
        
async def complete_quest(session: AsyncSession, PublicAddress: str, questId: str):
    try:
        get_user = await session.execute(
            select(models.User).where(models.User.PublicAddress == PublicAddress)
        )
        user = get_user.scalars().first()
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        get_quest = await session.execute(
            select(models.Quest).where(models.Quest.QuestId == questId)
        )
        quest = get_quest.scalars().first()
        if quest is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Quest not found"
            )
        get_referral = await session.execute(
            select(models.ReferralPoint).where(
                and_(
                    models.ReferralPoint.Referee == user.UserId,
                    models.ReferralPoint.Referer == user.RefferedBy 
                )
            )
        )
        referral = get_referral.scalars().first()
        if referral is not None:
            referral.PointsEarned += quest.Reward
            referral.UpdatedAt = datetime.now()
        else:
            if user.RefferedBy:
                new_referral = models.ReferralPoint(
                    Referer = user.RefferedBy,
                    Referee = user.UserId,
                    PointsEarned = quest.Reward
                )
                session.add(new_referral)
                await session.commit()
                await session.refresh(new_referral)
        get_user_activity = await session.execute(
            select(models.ActivityPoint).where(
                and_(
                    models.ActivityPoint.UserId == user.UserId,
                    models.ActivityPoint.QuestId == questId
                )
            )
        )
        user_activity = get_user_activity.scalars().first()
        if user_activity is not None:
            user_activity.MintCount += 1
            user_activity.PointsEarned += quest.Reward
            user_activity.UpdatedAt = datetime.now()
        else:
            new_activity = models.ActivityPoint(
                UserId = user.UserId,
                QuestId = questId,
                MintCount = 1,
                PointsEarned = quest.Reward
            )
            session.add(new_activity)
            await session.commit()
            await session.refresh(new_activity)
        await session.commit()
        return {
            "success": True,
            "status_code": status.HTTP_200_OK,
            "message": "Quest completed successfully",
            "data": None
        }  
    except HTTPException as e:
        return {
            "success": False,
            "status_code": e.status_code,
            "message": e.detail,
            "data": None
        }
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error"
        )
        
async def get_leaderboard(session: AsyncSession):
    try:
        referral_points = await session.execute(
            select(
                models.ReferralPoint.Referer, 
                func.sum(models.ReferralPoint.PointsEarned).label("total_points")
            )
            .group_by(models.ReferralPoint.Referer)
            .order_by(func.sum(models.ReferralPoint.PointsEarned).desc())
        )
        get_referral_points = referral_points.all()
        # print(get_referral_points)
        leaderboard = []
        for referer, total_points in get_referral_points:
            user_info = {}
            get_user = await session.execute(
                select(models.User).where(models.User.UserId == referer)
            )
            user = get_user.scalars().first()
            if user is not None:
                user_info["PublicAddress"] = user.PublicAddress
                user_info["RXP"] = total_points
                user_info["ReferralCount"] = user.TotalReferrals
                leaderboard.append(user_info)
            else:
                continue
        return {
            "success": True,
            "status_code": status.HTTP_200_OK,
            "message": "Leaderboard fetched successfully",
            "data": leaderboard
        }
                
    except HTTPException as e:
        return {
            "success": False,
            "status_code": e.status_code,
            "message": e.detail,
            "data": None
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error"
        )
        
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