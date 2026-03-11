from datetime import datetime
from enum import Enum
from typing import Optional
from uuid import UUID
from pydantic import BaseModel, ConfigDict


class ORMBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class DisputeStatus(str, Enum):
    OPEN = "OPEN"
    UNDER_REVIEW = "UNDER_REVIEW"
    RESOLVED = "RESOLVED"


class DisputeBase(BaseModel):
    contract_id: UUID
    raised_by: UUID
    reason: Optional[str] = None
    status: DisputeStatus = DisputeStatus.OPEN
    resolution_notes: Optional[str] = None


class DisputeCreate(DisputeBase):
    pass


class DisputeUpdate(BaseModel):
    contract_id: Optional[UUID] = None
    raised_by: Optional[UUID] = None
    reason: Optional[str] = None
    status: Optional[DisputeStatus] = None
    resolution_notes: Optional[str] = None


class DisputeOut(ORMBase, DisputeBase):
    id: UUID
    created_at: datetime
