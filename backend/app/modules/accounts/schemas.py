from datetime import datetime
from typing import Optional, List
from uuid import UUID
from pydantic import BaseModel, ConfigDict, Field


# ---------- Shared ----------
class ORMBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)


# ---------- Role ----------
class RoleBase(BaseModel):
    name: str = Field(..., max_length=50)
    privilege_level: int
    is_system: bool = True


class RoleCreate(RoleBase):
    pass


class RoleUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=50)
    privilege_level: Optional[int] = None
    is_system: Optional[bool] = None


class RoleOut(ORMBase, RoleBase):
    id: UUID
    created_at: datetime


# ---------- Permission ----------
class PermissionBase(BaseModel):
    code: str = Field(..., max_length=100)


class PermissionCreate(PermissionBase):
    pass


class PermissionUpdate(BaseModel):
    code: Optional[str] = Field(None, max_length=100)


class PermissionOut(ORMBase, PermissionBase):
    id: UUID
    created_at: datetime


# ---------- User ----------
class UserBase(BaseModel):
    role_id: Optional[UUID] = None
    is_verified: bool = False


class UserCreate(UserBase):
    pass


class UserUpdate(BaseModel):
    role_id: Optional[UUID] = None
    is_verified: Optional[bool] = None


class UserOut(ORMBase, UserBase):
    id: UUID
    role_assigned_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime


# ---------- Profile ----------
class ProfileBase(BaseModel):
    full_name: Optional[str] = Field(None, max_length=255)
    profile_image_url: Optional[str] = Field(None, max_length=500)
    bio: Optional[str] = None
    address_line1: Optional[str] = Field(None, max_length=255)
    address_line2: Optional[str] = Field(None, max_length=255)
    town: Optional[str] = Field(None, max_length=150)
    district: Optional[str] = Field(None, max_length=150)
    region: Optional[str] = Field(None, max_length=150)
    country: Optional[str] = Field(None, max_length=100)
    timezone: Optional[str] = Field(None, max_length=100)
    profession_qualification: Optional[str] = Field(None, max_length=255)
    academic_qualification: Optional[str] = Field(None, max_length=255)
    is_offer_service: bool = False


class ProfileCreate(ProfileBase):
    user_id: UUID


class ProfileUpdate(ProfileBase):
    pass


class ProfileOut(ORMBase, ProfileBase):
    user_id: UUID
    created_at: datetime


# ---------- Company ----------
class CompanyBase(BaseModel):
    name: str = Field(..., max_length=255)
    description: Optional[str] = None


class CompanyCreate(CompanyBase):
    owner_id: UUID


class CompanyUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=255)
    description: Optional[str] = None


class CompanyOut(ORMBase, CompanyBase):
    id: UUID
    owner_id: UUID
    created_at: datetime


# ---------- Role-Permission mapping payloads ----------
class AssignPermissionsPayload(BaseModel):
    permission_ids: List[UUID]


class AssignRolePayload(BaseModel):
    role_id: Optional[UUID] = None
