from datetime import datetime
from decimal import Decimal
from enum import Enum
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class ORMBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class ListingStatus(str, Enum):
    DRAFT = "DRAFT"
    PUBLISHED = "PUBLISHED"
    ARCHIVED = "ARCHIVED"


# ---------- ServiceCategory ----------
class ServiceCategoryBase(BaseModel):
    name: Optional[str] = Field(None, max_length=150)
    parent_id: Optional[UUID] = None


class ServiceCategoryCreate(ServiceCategoryBase):
    pass


class ServiceCategoryUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=150)
    parent_id: Optional[UUID] = None


class ServiceCategoryOut(ORMBase, ServiceCategoryBase):
    id: UUID


# ---------- ServiceListing ----------
class ServiceListingBase(BaseModel):
    provider_id: UUID
    category_id: UUID
    title: str = Field(..., max_length=255)
    description: str
    base_price: Decimal = Field(..., max_digits=12, decimal_places=2)
    currency: str = Field(default="USD", max_length=10)
    status: ListingStatus = ListingStatus.DRAFT
    rating_avg: float = 0
    rating_count: int = 0


class ServiceListingCreate(ServiceListingBase):
    pass


class ServiceListingUpdate(BaseModel):
    provider_id: Optional[UUID] = None
    category_id: Optional[UUID] = None
    title: Optional[str] = Field(None, max_length=255)
    description: Optional[str] = None
    base_price: Optional[Decimal] = Field(None, max_digits=12, decimal_places=2)
    currency: Optional[str] = Field(None, max_length=10)
    status: Optional[ListingStatus] = None
    rating_avg: Optional[float] = None
    rating_count: Optional[int] = None


class ServiceListingOut(ORMBase, ServiceListingBase):
    id: UUID
    created_at: datetime
