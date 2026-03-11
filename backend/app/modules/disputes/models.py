from uuid import uuid4
from sqlalchemy import (
    Column,
    DateTime,
    func,
    Text,
    Enum
)
from sqlalchemy.dialects.postgresql import UUID
from core.database import Base


class Dispute(Base):
    __tablename__ = "disputes"

    id = Column(UUID, primary_key=True, default=uuid4)
    contract_id = Column(UUID(as_uuid=True), nullable=False, index=True)
    raised_by = Column(UUID(as_uuid=True), nullable=False, index=True)
    reason = Column(Text)
    status = Column(
        Enum("OPEN", "UNDER_REVIEW", "RESOLVED", name="dispute_status"),
        default="OPEN"
    )
    resolution_notes = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
