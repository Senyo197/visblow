from uuid import uuid4
from sqlalchemy import (
    Column,
    String,
    DateTime,
    ForeignKey,
    func,
    Enum,
    Numeric
)
from sqlalchemy.dialects.postgresql import UUID
from core.database import Base


class EscrowAccount(Base):
    __tablename__ = "escrow_accounts"

    id = Column(UUID, primary_key=True, default=uuid4)
    contract_id = Column(UUID, ForeignKey("contracts.id"))
    balance = Column(Numeric(12, 2), default=0)
    status = Column(
        Enum("OPEN", "LOCKED", "CLOSED", name="escrow_status"),
        default="OPEN"
    )
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class EscrowTransaction(Base):
    __tablename__ = "escrow_transactions"

    id = Column(UUID, primary_key=True, default=uuid4)
    escrow_account_id = Column(UUID(as_uuid=True), nullable=False, index=True)
    type = Column(
        Enum("DEPOSIT", "RELEASE", "REFUND", name="escrow_tx_type")
    )
    amount = Column(Numeric(12, 2), nullable=False)
    reference = Column(String(255))
    created_at = Column(DateTime(timezone=True), server_default=func.now())


