from datetime import datetime
from typing import Optional
from uuid import UUID
from pydantic import BaseModel, ConfigDict, EmailStr, Field, IPvAnyAddress


class ORMBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class UserCredentialBase(BaseModel):
    user_id: UUID
    email: EmailStr
    ip_address: Optional[IPvAnyAddress] = None
    user_agent: Optional[str] = Field(None, max_length=500)
    device_fingerprint: Optional[str] = Field(None, max_length=255)
    is_verified: bool = False
    is_active: bool = True


class UserCredentialCreate(UserCredentialBase):
    password: str = Field(..., min_length=8, max_length=255)


class UserCredentialUpdate(BaseModel):
    email: Optional[EmailStr] = None
    password: Optional[str] = Field(None, min_length=8, max_length=255)
    ip_address: Optional[IPvAnyAddress] = None
    user_agent: Optional[str] = Field(None, max_length=500)
    device_fingerprint: Optional[str] = Field(None, max_length=255)
    is_verified: Optional[bool] = None
    is_active: Optional[bool] = None
    last_login_at: Optional[datetime] = None


class UserCredentialOut(ORMBase):
    id: UUID
    user_id: UUID
    email: EmailStr
    ip_address: Optional[IPvAnyAddress] = None
    user_agent: Optional[str] = None
    device_fingerprint: Optional[str] = None
    is_verified: bool
    is_active: bool
    last_login_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime


class RefreshTokenBase(BaseModel):
    user_id: UUID
    expires_at: datetime
    revoked: bool = False


class RefreshTokenCreate(RefreshTokenBase):
    token: str = Field(..., min_length=16, max_length=1024)


class RefreshTokenUpdate(BaseModel):
    revoked: Optional[bool] = None
    expires_at: Optional[datetime] = None


class RefreshTokenOut(ORMBase):
    id: UUID
    user_id: UUID
    expires_at: datetime
    revoked: bool
    revoked_at: Optional[datetime] = None
    created_at: datetime
