from uuid import uuid4
from sqlalchemy import (
    Column,
    String,
    Boolean,
    DateTime,
    func,
    Index,
    Integer,
    UniqueConstraint
)
from sqlalchemy.dialects.postgresql import UUID, JSONB
from core.database import Base


class UserCredential(Base):
    """
    Credential record for a single user.

    Stores login identity and account security state.
    Passwords are stored only as hashes.
    Enforces one credential row per user and case-insensitive unique email.
    """
    __tablename__ = "user_credentials"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    user_id = Column(UUID(as_uuid=True), nullable=False, index=True)
    email = Column(String(255), nullable=False)
    password_hash = Column(String(255), nullable=False)
    ip_address = Column(String(45), nullable=True)
    user_agent = Column(String(500))
    device_fingerprint = Column(String(255))
    is_verified = Column(Boolean, default=False, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    last_login_at = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    __table_args__ = (
        Index("uq_user_credentials_user_id", "user_id", unique=True),
        Index("uq_user_credentials_email_lower", func.lower(email), unique=True),
    )


class RefreshToken(Base):
    """
    Issued refresh-token record.

    Stores a hashed token, expiry time, and revocation state for a user session.
    Raw refresh tokens are never stored.
    """
    __tablename__ = "auth_refresh_tokens"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    user_id = Column(UUID(as_uuid=True), nullable=False, index=True)
    token_hash = Column(String(255), nullable=False, unique=True, index=True)
    expires_at = Column(DateTime(timezone=True), nullable=False)
    revoked = Column(Boolean, default=False, nullable=False)
    revoked_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    __table_args__ = (
        Index("idx_refresh_tokens_user_revoked", "user_id", "revoked"),
    )


class IdempotencyKey(Base):
    __tablename__ = "idempotency_keys"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    actor_id = Column(UUID(as_uuid=True), nullable=False, index=True)
    action = Column(String(100), nullable=False)
    key = Column(String(128), nullable=False)
    request_hash = Column(String(64), nullable=False)
    status_code = Column(Integer, nullable=False)
    #response_body = Column(JSONB, nullable=False)
    resource_type = Column(String(50))
    resource_id = Column(UUID(as_uuid=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    expires_at = Column(DateTime(timezone=True), nullable=False)

    __table_args__ = (
        UniqueConstraint("actor_id", "action", "key", name="uq_idem_actor_action_key"),
        Index("idx_idem_expires_at", "expires_at"),
    )
