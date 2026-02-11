from datetime import datetime
from decimal import Decimal
from typing import Optional, List

from pydantic import BaseModel, Field

from app.models import SearchStatus, MatchType, MatchStatus


# Search Request Schemas
class SearchCreate(BaseModel):
    """Schema for creating a new search request."""
    input_source: str = Field(..., max_length=500, description="Source of input data")
    object_name: str = Field(..., max_length=500, description="Name of the object being searched")
    ktru_code: Optional[str] = Field(None, max_length=100, description="KTRU code")
    nmc_value: Optional[Decimal] = Field(None, description="NMC value")
    limit_contracts: Optional[int] = Field(None, ge=1, description="Limit on number of contracts to process")


class SearchResponse(BaseModel):
    """Schema for search request response."""
    id: str
    input_source: str
    object_name: str
    ktru_code: Optional[str]
    status: SearchStatus
    found_total: int
    processed_count: int
    nmc_value: Optional[Decimal]
    limit_contracts: Optional[int]
    created_at: datetime

    class Config:
        from_attributes = True


# Contract Result Schemas
class ContractResultBase(BaseModel):
    """Base schema for contract result."""
    reestr_number: str = Field(..., max_length=100, description="Registry number")
    contract_url: Optional[str] = Field(None, max_length=1000, description="Contract URL")
    sign_date: Optional[datetime] = Field(None, description="Sign date")
    unit_price: Optional[Decimal] = Field(None, description="Unit price")
    match_type: MatchType
    ai_score: Optional[int] = Field(None, ge=0, le=100, description="AI score (0-100)")
    manufacturer_target: Optional[str] = Field(None, max_length=500, description="Target manufacturer")
    manufacturer_found: Optional[str] = Field(None, max_length=500, description="Found manufacturer")
    raw_data_json: Optional[dict] = Field(None, description="Raw JSON data")


class ContractResultCreate(ContractResultBase):
    """Schema for creating a contract result."""
    search_id: str


class ContractResultResponse(ContractResultBase):
    """Schema for contract result response."""
    id: str
    search_id: str

    class Config:
        from_attributes = True


# Specification Comparison Row Schemas
class SpecComparisonRowBase(BaseModel):
    """Base schema for specification comparison row."""
    name: str = Field(..., max_length=500, description="Specification name")
    target_value: Optional[str] = Field(None, description="Target value")
    actual_value: Optional[str] = Field(None, description="Actual value")
    match_status: MatchStatus
    weight: Optional[int] = Field(None, ge=0, description="Weight")


class SpecComparisonRowCreate(SpecComparisonRowBase):
    """Schema for creating a specification comparison row."""
    contract_result_id: str


class SpecComparisonRowResponse(SpecComparisonRowBase):
    """Schema for specification comparison row response."""
    id: str
    contract_result_id: str

    class Config:
        from_attributes = True


# Search Detail Response with relationships
class SearchDetailResponse(SearchResponse):
    """Schema for search detail with contract results."""
    contract_results: List[ContractResultResponse] = []


# Event schemas for SSE
class SearchEvent(BaseModel):
    """Schema for search event (SSE)."""
    event: str = Field(..., description="Event type")
    data: dict = Field(..., description="Event data")
    id: Optional[str] = Field(None, description="Event ID")
    retry: Optional[int] = Field(None, description="Retry interval in milliseconds")


# Status update schemas
class SearchStatusUpdate(BaseModel):
    """Schema for updating search status."""
    status: SearchStatus