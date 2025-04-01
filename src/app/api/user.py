from typing import Annotated, Optional

from fastapi import APIRouter, BackgroundTasks, Depends, Query, Response
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from ..config.database_config import async_get_db
from ..models import models
from ..schemas import schemas
from ..providers import users, quest

router = APIRouter(prefix="/users", tags=["user"])

@router.post(
    "",
    status_code= status.HTTP_201_CREATED
)
async def add_user(
    payload: schemas.AddUserDTO,
    db: AsyncSession = Depends(async_get_db)
):
    result = await users.add_user(db, payload)
    return result

@router.get(
    "",
    status_code= status.HTTP_200_OK
)
async def get_users(
    db: AsyncSession = Depends(async_get_db)
):
    result = await users.get_all_users(db)
    return result

@router.patch(
    "/update/{PublicAddress}",
    status_code= status.HTTP_200_OK
)
async def update_user(
    PublicAddress: str,
    payload: schemas.UpdateUserDTO,
    db: AsyncSession = Depends(async_get_db)
):
    result = await users.update_user_info(db, payload, PublicAddress)
    return result

@router.get(
    "/info/{PublicAddress}",
    status_code= status.HTTP_200_OK
)
async def get_user_information(
    PublicAddress: str,
    db: AsyncSession = Depends(async_get_db)
):
    result = await users.get_user_info(db, PublicAddress)
    return result

@router.get(
    "/leaderboard",
    status_code= status.HTTP_200_OK
)
async def leaderboards(
    db: AsyncSession = Depends(async_get_db)
):
    result = await quest.get_leaderboard(db)
    return result

@router.get(
    "/referees/{PublicAddress}",
    status_code= status.HTTP_200_OK
)
async def get_referees(
    PublicAddress: str,
    db: AsyncSession = Depends(async_get_db)
):
    result = await users.get_all_points_earned_from_referees(db, PublicAddress)
    return result
