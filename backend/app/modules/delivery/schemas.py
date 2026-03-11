from datetime import datetime
from enum import Enum
from typing import Optional
from uuid import UUID
from pydantic import BaseModel, ConfigDict, Field


class ORMBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class DeliveryStatus(str, Enum):
    SUBMITTED = "SUBMITTED"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"


class DeliveryBase(BaseModel):
    milestone_id: UUID
    submitted_by: UUID
    notes: Optional[str] = None
    file_url: Optional[str] = Field(None, max_length=500)
    status: DeliveryStatus = DeliveryStatus.SUBMITTED


class DeliveryCreate(DeliveryBase):
    pass


class DeliveryUpdate(BaseModel):
    milestone_id: Optional[UUID] = None
    submitted_by: Optional[UUID] = None
    notes: Optional[str] = None
    file_url: Optional[str] = None
    status: Optional[DeliveryStatus] = None


class DeliveryOut(ORMBase, DeliveryBase):
    id: UUID
    submitted_at: datetime
