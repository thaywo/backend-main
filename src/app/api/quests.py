from typing import Annotated, Optional

from fastapi import APIRouter, BackgroundTasks, Depends, Query, Response
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from ..config.database_config import async_get_db
from ..models import models
from ..schemas import schemas
from ..providers import quest
from sqlalchemy import func, select

router = APIRouter(prefix="/quests", tags=["quests"])

@router.post(
    "",
    status_code= status.HTTP_201_CREATED
)
async def add_quests(
    payload: schemas.AddQuestDTO,
    db: AsyncSession = Depends(async_get_db)
):
    result = await quest.add_quest(db, payload)
    return result

@router.get(
    "",
    status_code=status.HTTP_200_OK
)
async def get_all_quests(
    start: int = Query(1, description="Start index (inclusive)", gt=0),  # Default to 1
    end: int = Query(10, description="End index (inclusive)", gt=0),    # Default to 10
    db: AsyncSession = Depends(async_get_db)
):
    result = await quest.get_quests(db, start, end)
    return result

@router.get(
    "/{questId}",
    status_code= status.HTTP_200_OK
)
async def get_quest(
    questId: str,
    db: AsyncSession = Depends(async_get_db)
):
    result = await quest.get_quest_by_id(db, questId)
    return result


@router.patch(
    "/{questId}",
    status_code= status.HTTP_200_OK
)
async def update_quest(
    questId: str,
    payload: schemas.UpdateQuestDTO,
    db: AsyncSession = Depends(async_get_db)
):
    result = await quest.update_quest(db, questId, payload)
    return result


@router.delete(
    "/{questId}",
    status_code= status.HTTP_200_OK
)
async def delete_quest(
    questId: str,
    db: AsyncSession = Depends(async_get_db)
):
    result = await quest.delete_quest(db, questId)
    return result


@router.post(
    "/complete/{questId}",
    status_code= status.HTTP_200_OK
)
async def complete_quest(
    payload: schemas.CompleteQuestDTO,
    questId: str,
    db: AsyncSession = Depends(async_get_db)
):
    result = await quest.complete_quest(db, payload.PublicAddress, questId)
    return result
  
  
@router.get("/points-summary", response_model=schemas.PointsSummaryResponse)
async def points_summary_endpoint(db: AsyncSession = Depends(async_get_db)):
    return await quest.get_points_summary(db)
  
  
@router.get(
    "/complete",
    status_code= status.HTTP_200_OK
)
async def complete_questss():
    return "Hello, world!"  