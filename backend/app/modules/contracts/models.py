from uuid import uuid4
from sqlalchemy import (
    Column,
    String,
    DateTime,
    ForeignKey,
    Index,
    func,
    Numeric,
    Enum as SAEnum,
    CheckConstraint,
)
from sqlalchemy.dialects.postgresql import UUID
from core.database import Base


class Contract(Base):
    __tablename__ = "contracts"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    client_id = Column(UUID(as_uuid=True), nullable=False, index=True)
    provider_id = Column(UUID(as_uuid=True), nullable=False, index=True)
    listing_id = Column(UUID(as_uuid=True), nullable=False, index=True)
    total_amount = Column(Numeric(12, 2), nullable=False)
    currency = Column(String(10), nullable=False)

    status = Column(
        SAEnum(
            "PENDING_PAYMENT",
            "ACTIVE",
            "DELIVERED",
            "COMPLETED",
            "CANCELLED",
            "DISPUTED",
            name="contract_status",
        ),
        nullable=False,
        server_default="PENDING_PAYMENT",
    )

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    __table_args__ = (
        CheckConstraint("total_amount >= 0", name="ck_contract_total_amount_non_negative"),
        CheckConstraint("client_id <> provider_id", name="ck_contract_client_provider_different"),
        Index("idx_contracts_status_created_at", "status", "created_at"),
    )


class Milestone(Base):
    __tablename__ = "contract_milestones"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    contract_id = Column(
        UUID(as_uuid=True),
        ForeignKey("contracts.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    title = Column(String(255), nullable=False)
    amount = Column(Numeric(12, 2), nullable=False)

    status = Column(
        SAEnum(
            "PENDING",
            "FUNDED",
            "DELIVERED",
            "APPROVED",
            "RELEASED",
            name="milestone_status",
        ),
        nullable=False,
        server_default="PENDING",
    )

    due_date = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    __table_args__ = (
        CheckConstraint("amount >= 0", name="ck_milestone_amount_non_negative"),
    )
