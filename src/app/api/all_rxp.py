from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from ..providers.all_rxp import get_total_rxp
from ..config.database_config import async_get_db

router = APIRouter(prefix="/rxp", tags=["rxp"])

@router.get("/totals")
async def get_rxp_totals(
    db: AsyncSession = Depends(async_get_db)
):
    try:
        # Call the provider function to get RXP totals
        rxp_totals = await get_total_rxp(db)

        return {
            "success": True,
            "status_code": status.HTTP_200_OK,
            "message": "RXP totals fetched successfully",
            "data": rxp_totals
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
            detail=f"Error fetching RXP totals: {str(e)}"
        )