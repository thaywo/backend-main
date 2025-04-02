from pydantic import BaseModel, HttpUrl, Field, EmailStr
from typing import List, Optional
from datetime import datetime

class AddUserDTO(BaseModel):
    PublicAddress: str = Field(..., example="0x742d35Cc6634C0532925a3b844Bc454e4438f44e")
    ReferralCode: Optional[str] = Field(None, example="ABCD12")
    
class UserResponseDTO(BaseModel):
    id: int
    UserId: str
    PublicAddress: str
    ReferralCode: Optional[str] 
    RefferedBy: Optional[str] 
    email: Optional[str] 
    TotalReferrals: int 
    CreatedAt: datetime
    
    class Config:
        from_attributes = True  # Enables ORM mode
        
class UpdateUserDTO(BaseModel):
    email: Optional[EmailStr] = Field(None, example="example@gmail.com")
    ReferralCode: Optional[str] = Field(None, example="ABCD12")
    
class AddQuestDTO(BaseModel):
    Title: str = Field(..., example="Quest 1")
    ContractAddress: str = Field(..., example="0x742d35Cc6634C0532925a3b844Bc454e4438f44e")
    Description: str = Field(..., example="Description of Quest 1")
    Reward: int = Field(..., example=100)
    Image: Optional[HttpUrl] = Field(None, example="https://example.com/image.jpg")
    
    class Config:
        from_attributes = True  # Enables ORM mode
    
class UpdateQuestDTO(BaseModel):
    Title: Optional[str] = Field(None, example="Quest 1")
    ContractAddress: Optional[str] = Field(None, example="0x742d35Cc6634C0532925a3b844Bc454e4438f44e")
    Description: Optional[str] = Field(None, example="Description of Quest 1")
    Reward: Optional[int] = Field(None, example=100)
    Image: Optional[str] = Field(None, example="https://example.com/image.jpg")
    
class CompleteQuestDTO(BaseModel):
    PublicAddress: str
    
class QuestResponseDTO(BaseModel):
    id: int
    QuestId: str
    Title: str
    ContractAddress: Optional[str]
    Description: str
    Reward: int
    Image: Optional[str]
    CreatedAt: datetime
    UpdatedAt: datetime
    
    class Config:
        from_attributes = True  # Enables ORM mode
        
class QuestSummary(BaseModel):
    quest_id: str
    quest_title: str
    total_completions: int
    total_points: int

class PointsSummaryResponse(BaseModel):
    total_points: int
    quests: List[QuestSummary]       
    
class SignatureResponse(BaseModel):
    user_address: str
    token_id: int 
    chain_id: int
    nonce: int        