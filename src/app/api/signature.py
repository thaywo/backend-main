from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from ..providers.signature import SignatureProvider
from ..schemas.schemas import SignatureResponse
from typing import Optional
from pydantic import BaseModel

router = APIRouter(
    prefix="/signature",
    tags=["signature"],
    responses={404: {"description": "Not found"}},
)

# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")

# Add request model
class SignatureRequest(BaseModel):
    user_address: str
    quest_id: str
    chain_id: int = 1

@router.post("/quest")
async def generate_quest_signature(
    request: SignatureRequest  # Now expects JSON body
):
    try:
        provider = SignatureProvider()
        return provider.generate_quest_signature(
            user_address=request.user_address,
            quest_id=request.quest_id,
            chain_id=request.chain_id
        )
    except Exception as e:
        raise HTTPException(400, detail=str(e))