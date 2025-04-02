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
    token_id: int
    chain_id: int
    nonce: int

@router.post("/quest", response_model=dict)
async def generate_mint_signature(request: SignatureResponse):
    try:
        provider = SignatureProvider()
        return provider.generate_mint_signature(
            user_address=request.user_address,
            token_id=request.token_id,
            chain_id=request.chain_id,
            nonce=request.nonce
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))