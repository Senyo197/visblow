from uuid import uuid4
from sqlalchemy import (
    Column,
    DateTime,
    Index,
    func,
    Text,
    Integer
)
from sqlalchemy.dialects.postgresql import UUID, TSVECTOR
from core.database import Base


class Review(Base):
    """
    Contract review from one user to another.
    Captures rating and comment data tied to a contract, plus
    full-text/trigram indexes for fast search.
    """
    __tablename__ = "reviews"

    id = Column(UUID, primary_key=True, default=uuid4)
    contract_id = Column(UUID(as_uuid=True), nullable=False, index=True)
    reviewer_id = Column(UUID(as_uuid=True), nullable=False, index=True)
    reviewee_id = Column(UUID(as_uuid=True), nullable=False, index=True)
    rating = Column(Integer)
    comment = Column(Text)
    search_vector = Column(TSVECTOR)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    __table_args__ = (
        Index(
            "idx_reviews_search_vector",
            "search_vector",
            postgresql_using="gin"
        ),
        Index(
            "idx_reviews_comment_trgm",
            "comment",
            postgresql_using="gin",
            postgresql_ops={"comment": "gin_trgm_ops"}
        ),
    )
