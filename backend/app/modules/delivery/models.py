from uuid import uuid4
from sqlalchemy import (
    Column,
    String,
    DateTime,
    func,
    Text,
    Enum
)
from sqlalchemy.dialects.postgresql import UUID
from core.database import Base


class Delivery(Base):
    __tablename__ = "deliveries"

    id = Column(UUID, primary_key=True, default=uuid4)
    milestone_id = Column(UUID(as_uuid=True), nullable=False, index=True)
    submitted_by = Column(UUID(as_uuid=True), nullable=False, index=True)
    notes = Column(Text)
    file_url = Column(String)
    status = Column(
        Enum("SUBMITTED", "APPROVED", "REJECTED", name="delivery_status"),
        default="SUBMITTED"
    )
    submitted_at = Column(DateTime(timezone=True), server_default=func.now())
