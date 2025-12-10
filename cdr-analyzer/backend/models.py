"""
Pydantic models for CDR Analyzer
"""
from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Optional

class CallRecord(BaseModel):
    """Model for a single call record"""
    unique_id: str = Field(..., description="Unique identifier from CDR system")
    timestamp: datetime = Field(..., description="Call timestamp in ISO format")
    caller_number: Optional[str] = Field(None, description="Phone number of caller")
    extension: Optional[str] = Field(None, description="Extension that answered")
    status: str = Field(..., description="ANSWERED or MISSED")
    duration: int = Field(0, description="Call duration in seconds")
    
    class Config:
        json_schema_extra = {
            "example": {
                "unique_id": "1765268086.31589",
                "timestamp": "2024-12-09T14:30:00",
                "caller_number": "09121234567",
                "extension": "209",
                "status": "ANSWERED",
                "duration": 145
            }
        }

class UploadResponse(BaseModel):
    """Response model for file upload"""
    processed: int = Field(..., description="Total records processed")
    unique_calls: int = Field(..., description="Unique calls added to database")
    skipped: int = Field(0, description="Duplicate records skipped")
    message: str = Field(..., description="Status message")

class CallListResponse(BaseModel):
    """Response model for call list"""
    calls: List[CallRecord]
    total: int
    page: int
    limit: int

class DailyStats(BaseModel):
    """Daily statistics model"""
    date: str
    answered: int
    missed: int
    total: int

class ExtensionStats(BaseModel):
    """Extension performance model"""
    extension: str
    call_count: int
    total_duration: int
    avg_duration: float

class UniqueCallersStats(BaseModel):
    """Unique callers statistics model"""
    date: str = Field(..., description="Date in ISO format (YYYY-MM-DD)")
    unique_callers: int = Field(..., description="Count of distinct caller numbers")
    total_calls: int = Field(..., description="Total number of calls for comparison")

class StatsResponse(BaseModel):
    """Response model for statistics"""
    daily_stats: Optional[List[DailyStats]] = None
    extension_stats: Optional[List[ExtensionStats]] = None
