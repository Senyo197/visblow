from uuid import uuid4
from sqlalchemy import (
    Column,
    String,
    Boolean,
    DateTime,
    ForeignKey,
    Integer,
    Table,
    Index,
    Text,
    func
)
from sqlalchemy.dialects.postgresql import UUID, TSVECTOR
from core.database import Base

"""
Association table for the many-to-many relationship between roles and permissions.
"""
role_permissions = Table(
    "auth_role_permissions",
    Base.metadata,
    Column("role_id", UUID, ForeignKey("auth_roles.id", ondelete="CASCADE"), primary_key=True),
    Column("permission_id", UUID, ForeignKey("auth_permissions.id", ondelete="CASCADE"), primary_key=True),
)



class Role(Base):
    """System role table meant for RBAC, with a unique name and privilege hierarchy."""

    __tablename__ = "auth_roles"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    name = Column(String(50), unique=True, nullable=False)
    privilege_level = Column(Integer, nullable=False)
    is_system = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)


class Permission(Base):
    """Atomic permission that can be assigned to roles."""

    __tablename__ = "auth_permissions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    code = Column(String(100), unique=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)


class User(Base):
    """Core user account storing lifecycle state and assigned role."""

    __tablename__ = "accounts_users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    role_id = role_id = Column(UUID(as_uuid=True), nullable=False)
    role_assigned_at = Column(DateTime(timezone=True), server_default=func.now())
    is_verified = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)


class Profile(Base):
    """One-to-one user profile containing personal, location, and searchable fields."""

    __tablename__ = "accounts_profiles"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    user_id = Column(
        UUID,
        ForeignKey("accounts_users.id", ondelete="CASCADE"),
        unique=True, nullable=False
    )
    full_name = Column(String(255))
    profile_image_url = Column(String(500))
    bio = Column(Text)
    address_line1 = Column(String(255))
    address_line2 = Column(String(255))
    town = Column(String(150))
    district = Column(String(150))
    region = Column(String(150))
    country = Column(String(100))
    timezone = Column(String(100))
    profession_qualification = Column(String(255))
    academic_qualification = Column(String(255))
    is_offer_service = Column(Boolean, default=False, nullable=False)
    search_vector = Column(TSVECTOR)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    __table_args__ = (
        # GIN full-text search index
        Index("idx_profiles_search_vector", "search_vector", postgresql_using="gin"),
        # Trigram search indexes
        Index(
            "idx_profiles_full_name_trgm",
            "full_name",
            postgresql_using="gin",
            postgresql_ops={"full_name": "gin_trgm_ops"},
        ),
        Index(
            "idx_profiles_profession_trgm",
            "profession_qualification",
            postgresql_using="gin",
            postgresql_ops={"profession_qualification": "gin_trgm_ops"},
        ),
        Index(
            "idx_profiles_academic_trgm",
            "academic_qualification",
            postgresql_using="gin",
            postgresql_ops={"academic_qualification": "gin_trgm_ops"},
        ),
    )


class Company(Base):
    """Company record owned by a user, with searchable name/description fields."""

    __tablename__ = "accounts_companies"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    owner_id = Column(UUID, ForeignKey("accounts_users.id", ondelete="RESTRICT"), nullable=False)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    search_vector = Column(TSVECTOR)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    __table_args__ = (
        Index("idx_companies_search_vector", "search_vector", postgresql_using="gin"),
        Index(
            "idx_companies_name_trgm",
            "name",
            postgresql_using="gin",
            postgresql_ops={"name": "gin_trgm_ops"},
        ),
    )

