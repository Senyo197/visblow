from datetime import datetime
from decimal import Decimal
from enum import Enum
from typing import Optional
from uuid import UUID
from pydantic import BaseModel, ConfigDict, Field


class ORMBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class ContractStatus(str, Enum):
    PENDING_PAYMENT = "PENDING_PAYMENT"
    ACTIVE = "ACTIVE"
    DELIVERED = "DELIVERED"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"
    DISPUTED = "DISPUTED"


class MilestoneStatus(str, Enum):
    PENDING = "PENDING"
    FUNDED = "FUNDED"
    DELIVERED = "DELIVERED"
    APPROVED = "APPROVED"
    RELEASED = "RELEASED"


class ContractBase(BaseModel):
    client_id: UUID
    provider_id: UUID
    listing_id: UUID
    total_amount: Decimal = Field(..., ge=0, max_digits=12, decimal_places=2)
    currency: str = Field(..., min_length=3, max_length=10)
    status: ContractStatus = ContractStatus.PENDING_PAYMENT


class ContractCreate(ContractBase):
    pass


class ContractUpdate(BaseModel):
    client_id: Optional[UUID] = None
    provider_id: Optional[UUID] = None
    listing_id: Optional[UUID] = None
    total_amount: Optional[Decimal] = Field(None, ge=0, max_digits=12, decimal_places=2)
    currency: Optional[str] = Field(None, min_length=3, max_length=10)
    status: Optional[ContractStatus] = None


class ContractOut(ORMBase, ContractBase):
    id: UUID
    created_at: datetime
    updated_at: datetime


class MilestoneBase(BaseModel):
    contract_id: UUID
    title: str = Field(..., max_length=255)
    amount: Decimal = Field(..., ge=0, max_digits=12, decimal_places=2)
    status: MilestoneStatus = MilestoneStatus.PENDING
    due_date: Optional[datetime] = None


class MilestoneCreate(MilestoneBase):
    pass


class MilestoneUpdate(BaseModel):
    contract_id: Optional[UUID] = None
    title: Optional[str] = Field(None, max_length=255)
    amount: Optional[Decimal] = Field(None, ge=0, max_digits=12, decimal_places=2)
    status: Optional[MilestoneStatus] = None
    due_date: Optional[datetime] = None


class MilestoneOut(ORMBase, MilestoneBase):
    id: UUID
    created_at: datetime
    updated_at: datetime
