from uuid import uuid4
from sqlalchemy import (
    Column,
    String,
    DateTime,
    func,
    Text,
    Enum,
    Numeric,
    Float,
    Integer
)
from sqlalchemy.dialects.postgresql import UUID
from core.database import Base


class ServiceCategory(Base):
    __tablename__ = "marketplace_categories"

    id = Column(UUID, primary_key=True, default=uuid4)
    name = Column(String(150), unique=True)
    parent_id = Column(UUID(as_uuid=True), nullable=False, index=True)


class ServiceListing(Base):
    __tablename__ = "marketplace_listings"

    id = Column(UUID, primary_key=True, default=uuid4)
    provider_id = Column(UUID(as_uuid=True), nullable=False, index=True)
    category_id = Column(UUID(as_uuid=True), nullable=False, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    base_price = Column(Numeric(12, 2), nullable=False)
    currency = Column(String(10), default="USD")
    status = Column(
        Enum("DRAFT", "PUBLISHED", "ARCHIVED", name="listing_status"),
        default="DRAFT"
    )
    rating_avg = Column(Float, default=0)
    rating_count = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


