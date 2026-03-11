from datetime import datetime
from decimal import Decimal
from enum import Enum
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class ORMBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class EscrowStatus(str, Enum):
    OPEN = "OPEN"
    LOCKED = "LOCKED"
    CLOSED = "CLOSED"


class EscrowTxType(str, Enum):
    DEPOSIT = "DEPOSIT"
    RELEASE = "RELEASE"
    REFUND = "REFUND"


# ---------- EscrowAccount ----------
class EscrowAccountBase(BaseModel):
    contract_id: UUID
    balance: Decimal = Field(default=Decimal("0.00"), max_digits=12, decimal_places=2)
    status: EscrowStatus = EscrowStatus.OPEN


class EscrowAccountCreate(EscrowAccountBase):
    pass


class EscrowAccountUpdate(BaseModel):
    contract_id: Optional[UUID] = None
    balance: Optional[Decimal] = Field(None, max_digits=12, decimal_places=2)
    status: Optional[EscrowStatus] = None


class EscrowAccountOut(ORMBase, EscrowAccountBase):
    id: UUID
    created_at: datetime


# ---------- EscrowTransaction ----------
class EscrowTransactionBase(BaseModel):
    escrow_account_id: UUID
    type: EscrowTxType
    amount: Decimal = Field(..., max_digits=12, decimal_places=2)
    reference: Optional[str] = Field(None, max_length=255)


class EscrowTransactionCreate(EscrowTransactionBase):
    pass


class EscrowTransactionUpdate(BaseModel):
    escrow_account_id: Optional[UUID] = None
    type: Optional[EscrowTxType] = None
    amount: Optional[Decimal] = Field(None, max_digits=12, decimal_places=2)
    reference: Optional[str] = Field(None, max_length=255)


class EscrowTransactionOut(ORMBase, EscrowTransactionBase):
    id: UUID
    created_at: datetime
