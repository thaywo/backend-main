import logging
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from ..models import models
from fastapi import HTTPException, status
from fastapi import APIRouter, Depends
from ..config.database_config import async_get_db

logger = logging.getLogger(__name__)

async def calculate_rxp(session: AsyncSession, user_id: str) -> int:
    """
    Calculate RXP (Referral Experience Points) for a user.
    RXP is the total points earned from the points accumulated by the user's referrals.
    """
    try:
        # Step 1: Get the ReferralCode of the user
        user = await session.execute(
            select(models.User)
            .where(models.User.UserId == user_id)
        )
        user = user.scalars().first()

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )

        referral_code = user.ReferralCode

        # Step 2: Get all referrals for the user (users who have this user's ReferralCode in their RefferedBy field)
        referrals = await session.execute(
            select(models.User)
            .where(models.User.RefferedBy == referral_code)  # Corrected column name
        )
        referrals = referrals.scalars().all()

        logger.debug(f"Referrals for user {user_id} (ReferralCode: {referral_code}): {referrals}")

        if not referrals:
            logger.debug(f"No referrals found for user {user_id}")
            return 0  # No referrals, RXP is 0

        # Step 3: Calculate total RXP from referrals
        referral_points = await session.execute(
            select(func.coalesce(func.sum(models.ActivityPoint.PointsEarned), 0))
            .join(models.User, models.User.UserId == models.ActivityPoint.UserId)
            .where(models.User.RefferedBy == referral_code)  # Corrected column name
        )
        total_rxp = referral_points.scalar()

        logger.debug(f"Total RXP for user {user_id}: {total_rxp}")
        return total_rxp
    except Exception as e:
        logger.error(f"Error calculating RXP: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error"
        )