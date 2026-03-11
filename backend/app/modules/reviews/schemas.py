from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class ORMBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class ReviewBase(BaseModel):
    contract_id: UUID
    reviewer_id: UUID
    reviewee_id: UUID
    rating: Optional[int] = Field(None, ge=1, le=5)
    comment: Optional[str] = None


class ReviewCreate(ReviewBase):
    pass


class ReviewUpdate(BaseModel):
    contract_id: Optional[UUID] = None
    reviewer_id: Optional[UUID] = None
    reviewee_id: Optional[UUID] = None
    rating: Optional[int] = Field(None, ge=1, le=5)
    comment: Optional[str] = None


class ReviewOut(ORMBase, ReviewBase):
    id: UUID
    created_at: datetime
