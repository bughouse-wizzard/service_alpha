import uuid
from datetime import datetime
from decimal import Decimal
from enum import Enum
from typing import Optional

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Enum as SQLEnum,
    ForeignKey,
    Integer,
    Numeric,
    String,
    Text,
    JSON,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    """Base class for all SQLAlchemy models."""
    pass


class SearchStatus(str, Enum):
    """Enum for search request status."""
    PENDING = "pending"
    RUNNING = "running"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    PARTIAL = "partial"
    STOPPED = "stopped"


class MatchType(str, Enum):
    """Enum for contract match type."""
    EXACT = "exact"
    PARTIAL = "partial"
    SIMILAR = "similar"
    NO_MATCH = "no_match"


class MatchStatus(str, Enum):
    """Enum for specification comparison match status."""
    MATCH = "match"
    PARTIAL_MATCH = "partial_match"
    NO_MATCH = "no_match"
    NOT_APPLICABLE = "not_applicable"


class SearchRequest(Base):
    """Model for search requests."""
    __tablename__ = "search_requests"

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
        index=True
    )
    input_source: Mapped[str] = mapped_column(String(500), nullable=False)
    object_name: Mapped[str] = mapped_column(String(500), nullable=False)
    ktru_code: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    status: Mapped[SearchStatus] = mapped_column(
        SQLEnum(SearchStatus),
        default=SearchStatus.PENDING,
        nullable=False
    )
    found_total: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    processed_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    nmc_value: Mapped[Optional[Decimal]] = mapped_column(
        Numeric(15, 2),
        nullable=True
    )
    limit_contracts: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.utcnow,
        nullable=False
    )

    # Relationships
    contract_results: Mapped[list["ContractResult"]] = relationship(
        "ContractResult",
        back_populates="search_request",
        cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<SearchRequest(id={self.id}, object_name='{self.object_name}', status='{self.status}')>"


class ContractResult(Base):
    """Model for contract search results."""
    __tablename__ = "contract_results"

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
        index=True
    )
    search_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("search_requests.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    reestr_number: Mapped[str] = mapped_column(String(100), nullable=False)
    contract_url: Mapped[Optional[str]] = mapped_column(String(1000), nullable=True)
    sign_date: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    unit_price: Mapped[Optional[Decimal]] = mapped_column(Numeric(15, 2), nullable=True)
    match_type: Mapped[MatchType] = mapped_column(
        SQLEnum(MatchType),
        default=MatchType.NO_MATCH,
        nullable=False
    )
    ai_score: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    manufacturer_target: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    manufacturer_found: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    raw_data_json: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)

    # Relationships
    search_request: Mapped["SearchRequest"] = relationship(
        "SearchRequest",
        back_populates="contract_results"
    )
    spec_comparison_rows: Mapped[list["SpecComparisonRow"]] = relationship(
        "SpecComparisonRow",
        back_populates="contract_result",
        cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<ContractResult(id={self.id}, reestr_number='{self.reestr_number}', match_type='{self.match_type}')>"


class SpecComparisonRow(Base):
    """Model for specification comparison rows."""
    __tablename__ = "spec_comparison_rows"

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
        index=True
    )
    contract_result_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("contract_results.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    name: Mapped[str] = mapped_column(String(500), nullable=False)
    target_value: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    actual_value: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    match_status: Mapped[MatchStatus] = mapped_column(
        SQLEnum(MatchStatus),
        default=MatchStatus.NOT_APPLICABLE,
        nullable=False
    )
    weight: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)

    # Relationships
    contract_result: Mapped["ContractResult"] = relationship(
        "ContractResult",
        back_populates="spec_comparison_rows"
    )

    def __repr__(self) -> str:
        return f"<SpecComparisonRow(id={self.id}, name='{self.name}', match_status='{self.match_status}')>"