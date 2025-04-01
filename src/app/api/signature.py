from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta
from app.providers.signature import SignatureProvider
from app.models.enums import SignatureType
from app.schemas.schemas import SignatureRequest, SignatureResponse
from typing import Optional

router = APIRouter(
    prefix="/signature",
    tags=["signature"],
    responses={404: {"description": "Not found"}},
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")

@router.post("/generate", response_model=SignatureResponse)
async def generate_signature(
    request: SignatureRequest,
    token: str = Depends(oauth2_scheme)
):
    """
    Generate a signature for minting rewards after quest completion
    
    Required in request:
    - user_address: Ethereum address of the user
    - quest_id: ID of the completed quest
    - chain_id: EVM chain ID where contract is deployed
    - contract_address: Address of the reward contract
    - expiry (optional): Signature expiry timestamp
    """
    try:
        signature_provider = SignatureProvider()
        
        # Optional expiry date handling
        expiry_date = None
        if request.expiry:
            expiry_date = datetime.fromtimestamp(request.expiry)
        
        signature, expiry = signature_provider.generate_signature(
            user_address=request.user_address,
            quest_id=request.quest_id,
            chain_id=request.chain_id,
            contract_address=request.contract_address,
            expiry=expiry_date,
            signature_type=SignatureType.QUEST_COMPLETION
        )
        
        return {
            "signature": signature,
            "expiry": expiry,
            "user_address": request.user_address,
            "quest_id": request.quest_id,
            "contract_address": request.contract_address,
            "chain_id": request.chain_id
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Error generating signature: {str(e)}"
        )