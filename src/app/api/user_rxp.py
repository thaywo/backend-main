from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from ..providers.user_rxp import calculate_rxp
from ..config.database_config import async_get_db

router = APIRouter(prefix="/points", tags=["point"])

@router.get("/{user_id}/rxp")
async def get_user_rxp(
    user_id: str,
    db: AsyncSession = Depends(async_get_db)
):
    try:
        # Calculate RXP for the user
        rxp = await calculate_rxp(db, user_id)

        return {
            "success": True,
            "status_code": 200,
            "message": "RXP calculated successfully",
            "data": {
                "user_id": user_id,
                "rxp": rxp
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
            status_code=500,
            detail=f"Error calculating RXP: {str(e)}"
        )