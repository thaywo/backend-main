import uuid
from datetime import datetime, timezone

from sqlalchemy import JSON, Boolean, Column, DateTime
from sqlalchemy import Enum as EnumColumn
from sqlalchemy import Float, ForeignKey, Integer, String, Text, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import (
    Column, Integer, String, ForeignKey, BigInteger, 
    Date, DateTime, Text, Boolean, Enum, ARRAY
)
from sqlalchemy.dialects.postgresql import (
    UUID, JSONB, TIMESTAMP, BYTEA, CITEXT
)

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    UserId = Column(
        String(36), default=lambda: str(uuid.uuid4()), unique=True, nullable=False
    )
    PublicAddress = Column(
        String(100),
        unique=True,
        index=True,
        nullable=False,
    )
    email = Column(
        String(100),
        unique=True,
        index=True,
        nullable=True,
    )
    ReferralCode = Column(String(6), unique=True, nullable=True)
    RefferedBy = Column(String(36), nullable=True)
    TotalReferrals = Column(Integer, default=0)
    CreatedAt = Column(DateTime, default=datetime.now())
    activity_points = relationship("ActivityPoint", back_populates="user")
    referrals_made = relationship(
        "ReferralPoint",
        back_populates="referrer",
        primaryjoin="User.UserId==ReferralPoint.Referer"
    )
    referrals_received = relationship(
        "ReferralPoint",
        back_populates="referee",
        primaryjoin="User.UserId==ReferralPoint.Referee"
    )

class Quest(Base):
    __tablename__ = "quests"

    id = Column(Integer, primary_key=True, index=True)
    QuestId = Column(
        String(36), default=lambda: str(uuid.uuid4()), unique=True, nullable=False
    )
    Title = Column(String(100), nullable=False)
    Description = Column(Text, nullable=False)
    ContractAddress = Column(String(1000), nullable=True)
    Reward = Column(Integer, nullable=False) # Points
    Image = Column(Text, nullable=True)
    is_deleted = Column(Boolean, default=False)
    CreatedAt = Column(DateTime, default=datetime.now())
    UpdatedAt = Column(DateTime, default=datetime.now())
    activity_points = relationship("ActivityPoint", back_populates="quest")
    
class ActivityPoint(Base):
    __tablename__ = "activity_points"

    id = Column(Integer, primary_key=True, index=True)
    UserId = Column(String(36), ForeignKey("users.UserId", ondelete="CASCADE"), nullable=False)
    QuestId = Column(String(36), ForeignKey("quests.QuestId", ondelete="CASCADE"), nullable=False)
    MintCount = Column(Integer, nullable=False)
    PointsEarned = Column(Integer, nullable=False)
    CreatedAt = Column(DateTime, default=datetime.now())
    UpdatedAt = Column(DateTime, default=datetime.now()) 
    user = relationship("User", back_populates="activity_points")   
    quest = relationship("Quest", back_populates="activity_points")
    
class ReferralPoint(Base):
    __tablename__ = "referral_points"

    id = Column(Integer, primary_key=True, index=True)
    Referer = Column(String(36), ForeignKey("users.UserId", ondelete="CASCADE"), nullable=False)
    Referee = Column(String(36), ForeignKey("users.UserId", ondelete="CASCADE"), nullable=False)
    PointsEarned = Column(Integer, nullable=False)
    CreatedAt = Column(DateTime, default=datetime.now())
    UpdatedAt = Column(DateTime, default=datetime.now()) 
    referrer = relationship("User", back_populates="referrals_made", foreign_keys=[Referer])
    referee = relationship("User", back_populates="referrals_received", foreign_keys=[Referee])