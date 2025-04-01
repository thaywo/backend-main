from datetime import datetime, timedelta
from fastapi import HTTPException
from sqlalchemy import and_, delete, func, or_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from starlette import status
from ..apputils import utils
from ..schemas import schemas
from ..models import models

async def add_user(
    session: AsyncSession,
    payload: schemas.AddUserDTO
):
    try:
        print(payload)
        # Convert PublicAddress to lowercase
        lowercase_address = payload.PublicAddress.lower()
        getUser = await session.execute(
            select(models.User).where(models.User.PublicAddress == lowercase_address)
        )
        user = getUser.scalars().first()
        print("**********",user)
        if user != None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User already exists"
            )
        if payload.ReferralCode != None:
            referal_code_validity = await session.execute(
                select(models.User).where(models.User.ReferralCode == payload.ReferralCode)
            )
            referer = referal_code_validity.scalars().first()
            if referer is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Referral code is invalid"
                )
            else:
                referer.TotalReferrals += 1
                new_user = models.User(
                    PublicAddress=lowercase_address,  # Use lowercase address
                    ReferralCode=utils.generate_referral_code(),
                    RefferedBy=referer.UserId,
                )
        else:
            new_user = models.User(
                PublicAddress=lowercase_address,  # Use lowercase address
                ReferralCode=utils.generate_referral_code(),
            )
        session.add(new_user)
        await session.commit()
        await session.refresh(new_user)
        response = schemas.UserResponseDTO.model_validate(new_user)
        return {
            "success": True,
            "status_code": status.HTTP_201_CREATED,
            "message": "User added successfully",
            "data": response
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
  
async def update_user_info(
    session: AsyncSession,
    payload: schemas.UpdateUserDTO,
    public_address: str
):
    try:
        check_user = await session.execute(
            select(models.User).where(models.User.PublicAddress == public_address)
        )
        valid_user = check_user.scalars().first()
        if valid_user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        if payload.email:
            getUser = await session.execute(
                select(models.User)
                .options(selectinload("*"))
                .where(func.lower(models.User.email) == payload.email.lower())
            )
            user = getUser.scalars().first()
            if user:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="A user with this email already exists"
                )
            valid_user.email = payload.email
        if payload.ReferralCode:
            if valid_user.ReferralCode == payload.ReferralCode:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="You cannot use your own referral code"
                )
            if valid_user.RefferedBy != None:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Referral code can only be updated once"
                )
            code_validity = await session.execute(
                select(models.User)
                .where(models.User.ReferralCode == payload.ReferralCode)
            )
            referral_code = code_validity.scalars().first()
            if referral_code == None:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Invalid referral code"
                )
            valid_user.RefferedBy = referral_code.UserId
            referral_code.TotalReferrals += 1
        validated_user = schemas.UserResponseDTO.model_validate(valid_user).model_dump()
        await session.commit()
        return {
            "success": True,
            "status_code": status.HTTP_200_OK,
            "message": "Quest updated successfully",
            "data": validated_user
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
        
async def get_user_info(
    session: AsyncSession,
    PublicAddress: str
):
    try:
        getUser = await session.execute(
            select(models.User).where(models.User.PublicAddress == PublicAddress)
        )
        user = getUser.scalars().first()
        print("**************", user)
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        referralCount = await session.execute(
            select(func.count(models.User.UserId)).where(models.User.RefferedBy == user.UserId)
        )
        totalReferrals = referralCount.scalars().first()
        totalReferralPoints = await session.execute(
            select(func.sum(models.ReferralPoint.PointsEarned)).where(models.ReferralPoint.Referer == user.UserId)
        )
        totalPoints = totalReferralPoints.scalars().first()
        user_info = schemas.UserResponseDTO.model_validate(user).model_dump()
        print(user_info)
        user_info["TotalReferrals"] = totalReferrals
        user_info["ReferralPoints"] = totalPoints
        return {
            "success": True,
            "status_code": status.HTTP_200_OK,
            "message": "User info retrieved successfully",
            "data": user_info
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
        
async def get_all_points_earned_from_referees(
    session: AsyncSession,
    PublicAddress: str
):
    try:
        getUser = await session.execute(
            select(models.User).where(models.User.PublicAddress == PublicAddress)
        )
        user = getUser.scalars().first()
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        getAllReferees = await session.execute(
            select(models.User).where(models.User.RefferedBy == user.UserId)
        )
        allReferees = getAllReferees.scalars().all()
        if len(allReferees) == 0:
            return {
                "success": True,
                "status_code": status.HTTP_200_OK,
                "message": "No referees found",
                "data": []
            }
        refereeList = []
        for referee in allReferees:
            referee_details = {}
            refereeDetails = await session.execute(
                select(models.ReferralPoint)
                .where(
                    and_(
                        models.ReferralPoint.Referer == user.UserId,
                        models.ReferralPoint.Referee == referee.UserId
                    )
                )
            )
            getReferee = refereeDetails.scalars().first()
            if getReferee is None:
                referee_details["PublicAddress"] = referee.PublicAddress
                referee_details["PointsEarned"] = 0
                refereeList.append(referee_details)
            else:
                referee_details["PublicAddress"] = referee.PublicAddress
                referee_details["PointsEarned"] = getReferee.PointsEarned
                refereeList.append(referee_details)
        # refereePoints = await session.execute(
        #     select(models.ReferralPoint).where(models.ReferralPoint.Referer == user.UserId)
        #     .order_by(models.ReferralPoint.PointsEarned.desc())
        # )
        # allRefereePoints = refereePoints.scalars().all()
        # refereeList = []
        # for referee in allRefereePoints:
        #     referee_details = {}
        #     refereeDetails = await session.execute(
        #         select(models.User).where(models.User.UserId == referee.Referee)
        #     )
        #     getReferee = refereeDetails.scalars().first()
        #     referee_details["PublicAddress"] = getReferee.PublicAddress
        #     referee_details["PointsEarned"] = referee.PointsEarned
        #     refereeList.append(referee_details)
        return {
            "success": True,
            "status_code": status.HTTP_200_OK,
            "message": "Total points earned from referees retrieved successfully",
            "data": refereeList
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
        
async def get_all_users(session: AsyncSession):
    try:
        getAllUsers = await session.execute(
            select(models.User)
        )
        users = getAllUsers.scalars().all()
        if users is None:
            return {
                "success": True,
                "message": "Users retrieved successfully",
                "data": []
            }
        return {
                "success": True,
                "message": "Users retrieved successfully",
                "data": users
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